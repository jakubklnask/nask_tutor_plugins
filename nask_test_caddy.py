from tutor import hooks
import os

def force_overwrite_caddyfile(root, config):
    """
    Wykonuje się automatycznie po 'tutor config save'.
    Dostaje 'root' (ścieżkę) i 'config' (słownik ustawień) bezpośrednio od Tutora.
    """
    try:
        # Ścieżka do Caddyfile
        caddy_file = os.path.join(root, "env", "apps", "caddy", "Caddyfile")
        
        # Pobieramy hosty bezpośrednio ze słownika config, który przekazał nam Tutor
        lms_host = config.get("LMS_HOST", "")
        cms_host = config.get("CMS_HOST", "")
        mfe_host = config.get("MFE_HOST", "")
        meilisearch_host = config.get("MEILISEARCH_HOST", "")
        superset_host = config.get("SUPERSET_HOST", "")
        preview_host = config.get("PREVIEW_LMS_HOST") or f"preview.{lms_host}"

        # Generujemy treść (z podwójnymi {{ }} dla Caddy, żeby f-string ich nie zjadł)
        new_content = f"""
# Global configuration
{{
    auto_https off
}}

(proxy) {{
    log {{
        output stdout
        format filter {{
            wrap json
            fields {{
                common_log delete
                request>headers delete
                resp_headers delete
                tls delete
            }}
        }}
    }}
    encode gzip
    reverse_proxy {{args.0}} {{
        header_up X-Forwarded-Port 443
        header_up X-Forwarded-Proto https
    }}
}}

# LMS i Preview
http://{lms_host}, http://{preview_host} {{
    @favicon_matcher {{
        path_regexp ^/favicon.ico$
    }}
    rewrite @favicon_matcher /theming/asset/images/favicon.ico

    handle_path /api/profile_images/*/*/upload {{
        request_body {{
            max_size 1MB
        }}
    }}

    import proxy "lms:8000"

    handle_path /* {{
        request_body {{
            max_size 4MB
        }}
    }}
}}

# CMS (Studio)
http://{cms_host} {{
    @favicon_matcher {{
        path_regexp ^/favicon.ico$
    }}
    rewrite @favicon_matcher /theming/asset/images/favicon.ico

    import proxy "cms:8000"

    request_body {{
        max_size 1000MB
    }}
}}

# Meilisearch
http://{meilisearch_host} {{
    import proxy "meilisearch:7700"
}}

# Superset
http://{superset_host} {{
    import proxy "superset:8088"
}}

# MFE
http://{mfe_host} {{
    request_body {{
        max_size 2MB
    }}
    import proxy "mfe:8002"
}}
"""
        # Zapisujemy plik
        with open(caddy_file, 'w', encoding='utf-8') as f:
            f.write(new_content.strip())
        
        # Opcjonalnie: info w konsoli, że nadpisano
        print(f"\033[32m[OK]\033[0m Caddyfile has been overwritten with custom Azure Front Door config.")

    except Exception as e:
        print(f"\033[31m[ERROR]\033[0m Failed to overwrite Caddyfile: {e}")

# REJESTRACJA
# Zamiast atexit, używamy oficjalnego hooka Tutora
hooks.Actions.CONFIG_LOADED.add(force_overwrite_caddyfile)

# Standardowe patche dla Open edX (Python settings)
hooks.Filters.ENV_PATCHES.add_items([
    ("openedx-cms-production-settings", "MAX_ASSET_UPLOAD_FILE_SIZE_IN_MB = 1000"),
    ("openedx-cms-development-settings", "MAX_ASSET_UPLOAD_FILE_SIZE_IN_MB = 1000"),
])