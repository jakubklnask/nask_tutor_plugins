# Nadawanie szablonu stronom legacy odbywa się poprzez umieszczenie plików
# reprezentujących repozytorium szablonu w odpowiedni miejscu środowiska tutor
# Robimy to podpinająć się pod komendę tutor dev/local do init wykonywaną jednorazowo
# podczas instalowania platformy

# normalnie --limit jest wykorzystywany w init do hooka CLI_DO_INIT_TASKS
# ale ten task nie jest przypisany do zadnego kontenera - sprawdzamy wiec sztucznie --limit 
# na podstawie nazwy pliku z tym pluginem

import os
import subprocess
from tutor import hooks

# 1. DYNAMICZNA NAZWA PLUGINU
PLUGIN_NAME = os.path.splitext(os.path.basename(__file__))[0]

# KONFIGURACJA
THEME_REPO_URL = "https://github.com/jakubklnask/nask_legacy_pages_branding"
THEME_NAME = "nask"

# ----------------------------------------------------------------------------
# LOGIKA NA HOŚCIE (NIE W KONTENERZE!) (DO_JOB)
# ----------------------------------------------------------------------------
@hooks.Actions.DO_JOB.add()
def nask_theme_host_logic(job, *args, **kwargs):
    if job == "init":
        # Pobieramy flagi limit (Tutor zwraca listę lub None)
        limit_flags = kwargs.get("limit") or []

        # Sprawdzamy: czy robimy full init (brak limitów) LUB czy celujemy w ten plugin
        if not limit_flags or PLUGIN_NAME in limit_flags:
            # Ścieżka do Tutora
            tutor_root = subprocess.check_output(["tutor", "config", "printroot"]).decode("utf-8").strip()
            theme_dir = os.path.join(tutor_root, "env", "build", "openedx", "themes", THEME_NAME)

            print(f"++++++ [{PLUGIN_NAME}] Przechwycono zadanie init. Host: {theme_dir}")

            # Git
            if not os.path.exists(theme_dir):
                print(f"++++++ [{PLUGIN_NAME}] Klonowanie repozytorium...")
                subprocess.run(["git", "clone", THEME_REPO_URL, theme_dir], check=True)
            else:
                print(f"++++++ [{PLUGIN_NAME}] Aktualizacja repozytorium...")
                subprocess.run(["git", "-C", theme_dir, "pull"], check=True)

            # Automatyczne zaaplikowanie motywu (wywołanie Tutora z poziomu Pythona)
            print(f"++++++ [{PLUGIN_NAME}] Odpalam settheme...")
            subprocess.run(["tutor", "dev", "do", "settheme", THEME_NAME], check=True)
