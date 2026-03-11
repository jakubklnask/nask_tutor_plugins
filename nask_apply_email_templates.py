from tutor import hooks

# ==========================================
# KONFIGURACJA REPOZYTORIUM
# ==========================================
REPO_URL = "https://github.com/jakubklnask/nask_email_templates.git" 
SUBDIR = "og_template_2013/modifying"                                                # ścieżka do katalogu wewnątrz repozytorium
HTML_FILENAME = "oneliner_out.txt"                                      # nazwa pliku z jednoliniowym html-em wygenerowanym przez skrypt
PLAIN_FILENAME = "plain-template.txt"                                      # nazwa pliku tekstowego do podmiany plain-template
# ==========================================

# Skrypt Pythona (wykonywany wewnątrz kontenera LMS)
PYTHON_SCRIPT = f'''
import os
from lms.djangoapps.bulk_email.models import CourseEmailTemplate

# Pobieramy ścieżkę do tymczasowego katalogu ze zmiennej środowiskowej Basha
temp_dir = os.environ.get("REPO_TEMP_DIR")

# Budujemy pełne ścieżki do pobranych plików
html_file_path = os.path.join(temp_dir, "{SUBDIR}", "{HTML_FILENAME}")
plain_file_path = os.path.join(temp_dir, "{SUBDIR}", "{PLAIN_FILENAME}")

print(f"Czytam plik HTML z: {{html_file_path}}")
with open(html_file_path, "r", encoding="utf-8") as f:
    html_content = f.read()

print(f"Czytam plik TXT z: {{plain_file_path}}")
with open(plain_file_path, "r", encoding="utf-8") as f:
    plain_content = f.read()

# Szukamy szablonu nr 1 i nadpisujemy go zawartością z plików
template, created = CourseEmailTemplate.objects.get_or_create(id=1)
template.html_template = html_content
template.plain_template = plain_content
template.save()

print("Szablon email NASK zaktualizowany prosto z repozytorium!")
'''

# Skrypt Bashowy (uruchamiany przez kontener lms-job)
# W pythonie 3.12.3 nie trzeba escape'ować $
BASH_COMMAND = f"""
echo "++++++ Rozpoczynam pobieranie szablonów e-mail z repozytorium..."

# 1. Tworzymy bezpieczny katalog tymczasowy i eksportujemy ścieżkę
export REPO_TEMP_DIR=$(mktemp -d)

# 2. Klonujemy repozytorium (używamy --depth 1, żeby pobrać tylko najnowsze pliki, co jest błyskawiczne)
git clone --depth 1 "{REPO_URL}" "$REPO_TEMP_DIR"

# 3. Odpalamy Django shella i wrzucamy do niego nasz skrypt Pythona
cat << 'EOF' | python manage.py lms shell
{PYTHON_SCRIPT}
EOF

# 4. Sprzątamy po sobie, usuwając pobrane pliki
rm -rf "$REPO_TEMP_DIR"
echo "++++++ Zakończono proces aktualizacji szablonów!"
"""

# Podpinamy to wszystko pod hooka inicjalizacyjnego
hooks.Filters.CLI_DO_INIT_TASKS.add_item(
    ("lms", BASH_COMMAND)
)
