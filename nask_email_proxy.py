import os
import subprocess
from tutor import hooks

PLUGIN_NAME = "email_oauth2_proxy"

# ==========================================
# 0. ZMIENNE KONFIGURACJI SYSTEMU MAILOWEGO OPEN EDX
# (USTAWIAMY TAK ŻEBY GADAŁ Z NASZYM TŁUMACZEM NA OAUTH2)
# ==========================================    


hooks.Filters.CONFIG_OVERRIDES.add_items([
    ("SMTP_HOST", 'email-oauth2-proxy'),
    ("SMTP_PORT",1587),
    ("SMTP_USE_SSL",False),
    ("SMTP_USE_TLS",False),
    ("SMTP_USERNAME",'edu.technologie@nask.pl'),
    ("SMTP_PASSWORD",'ProxyPassword123')
])
# roznice miedzy unique,defaults itd.
#https://docs.tutor.edly.io/reference/api/hooks/catalog.html

# ==========================================
# 1. ZMIENNE KONFIGURACYJNE
# ==========================================
hooks.Filters.CONFIG_UNIQUE.add_items([
    ("EMAIL_PROXY_IMAGE", "email-oauth2-proxy:latest"),
    ("EMAIL_PROXY_AZURE_APP_EMAIL", "edu.technologie@nask.pl"),
    ("EMAIL_PROXY_AZURE_APP_TENANT_ID", "common"),
    ("EMAIL_PROXY_AZURE_APP_CLIENT_ID", ""),
    ("EMAIL_PROXY_AZURE_APP_CLIENT_SECRET", ""),
])

# ==========================================
# 2. SAMOGENERACJA PLIKÓW (Podejście z printroot)
# ==========================================
@hooks.Actions.CONFIG_LOADED.add()
def generate_plugin_files(config):
    # Wykorzystujemy Twój sposób na pobranie głównej ścieżki Tutora
    tutor_root = subprocess.check_output(["tutor", "config", "printroot"]).decode("utf-8").strip()
    
    # Budujemy ścieżki docelowe
    env_root = os.path.join(tutor_root, "env", "plugins", PLUGIN_NAME)
    build_dir = os.path.join(env_root, "build", "email-oauth2-proxy")
    config_dir = os.path.join(env_root, "config")

    # Tworzymy struktury katalogów (exist_ok=True zapobiega błędom, jeśli już istnieją)
    os.makedirs(build_dir, exist_ok=True)
    os.makedirs(config_dir, exist_ok=True)

    # A) Zapisujemy w locie Dockerfile
    dockerfile_content = """FROM python:3.12-slim
WORKDIR /app
RUN apt-get update && apt-get install -y git
RUN git clone https://github.com/simonrob/email-oauth2-proxy.git .
RUN pip install --no-cache-dir -r requirements-core.txt
RUN pip install prompt-toolkit
"""
    with open(os.path.join(build_dir, "Dockerfile"), "w") as f:
        f.write(dockerfile_content)

    # B) Składamy plik emailproxy.config podstawiając zmienne z config.yml
    email = config.get("EMAIL_PROXY_AZURE_APP_EMAIL", "")
    tenant = config.get("EMAIL_PROXY_AZURE_APP_TENANT_ID", "")
    client_id = config.get("EMAIL_PROXY_AZURE_APP_CLIENT_ID", "")
    secret = config.get("EMAIL_PROXY_AZURE_APP_CLIENT_SECRET", "")
    
    secret_line = f"client_secret = {secret}" if secret else ""

    proxy_config_content = f"""
[Email OAuth 2.0 Proxy configuration file]
[Server setup]
[SMTP-1587]
server_address = smtp-mail.outlook.com
server_port = 587
server_starttls = True
local_address = 0.0.0.0

[{email}]
permission_url = https://login.microsoftonline.com/{tenant}/oauth2/v2.0/authorize
token_url = https://login.microsoftonline.com/{tenant}/oauth2/v2.0/token
oauth2_scope = https://outlook.office.com/IMAP.AccessAsUser.All https://outlook.office.com/POP.AccessAsUser.All https://outlook.office.com/SMTP.Send offline_access
redirect_uri = http://localhost
client_id = {client_id}
{secret_line}

[emailproxy]
delete_account_token_on_password_error = False
encrypt_client_secret_on_first_use = False
use_login_password_as_client_credentials_secret = False
allow_catch_all_accounts = False

"""
    with open(os.path.join(config_dir, "emailproxy.config"), "w") as f:
        f.write(proxy_config_content)

# ==========================================
# 3. REJESTRACJA BUDOWANIA OBRAZU I DOCKER COMPOSE
# ==========================================
hooks.Filters.IMAGES_BUILD.add_item(
    (
        "email-oauth2-proxy",
        ("plugins", PLUGIN_NAME, "build", "email-oauth2-proxy"),
        "{{ EMAIL_PROXY_IMAGE }}",
        (),
    )
)

DOCKER_COMPOSE_PATCH = f"""
email-oauth2-proxy:
    image: {{{{ EMAIL_PROXY_IMAGE }}}}
    restart: always
    command: ["python", "emailproxy.py","--no-gui", "--config-file", "/app/config/emailproxy.config", "--cache-store", "/app/cache/tokens.json"]
    volumes:
        - ../plugins/{PLUGIN_NAME}/config/emailproxy.config:/app/config/emailproxy.config:ro
        - ../../data/email_oauth2_proxy:/app/cache:rw
"""

hooks.Filters.ENV_PATCHES.add_items([
    ("local-docker-compose-services", DOCKER_COMPOSE_PATCH),
    ("dev-docker-compose-services", DOCKER_COMPOSE_PATCH)
])
