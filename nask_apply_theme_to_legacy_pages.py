import os
import subprocess
import atexit
import sys
from tutor import hooks

def nask_theme_host_atexit():
    """
    Odpala się przy zamykaniu procesu Tutora.
    Obsługuje --limit <nazwa_pliku_bez_py>.
    """
    args = sys.argv
    # 1. Podstawowy warunek: czy to jest komenda 'do init'?
    if not ("do" in args and "init" in args):
        return

    # 2. Wyciągamy identyfikator pluginu z nazwy pliku (np. 'nask_apply_email_templates')
    # os.path.basename(__file__) to nazwa pliku, splitext usuwa rozszerzenie .py
    plugin_id = os.path.splitext(os.path.basename(__file__))[0]

    # 3. Logika --limit
    if "--limit" in args:
        try:
            limit_idx = args.index("--limit")
            # Sprawdzamy, czy po --limit coś jest i czy to nasza nazwa
            if len(args) <= limit_idx + 1 or args[limit_idx + 1] != plugin_id:
                # Jeśli jest --limit, ale na kogoś innego - wychodzimy po cichu
                return
        except ValueError:
            pass # Nie powinno się zdarzyć, skoro in args zwróciło True

    # ==========================================
    # TUTAJ ZACZYNA SIĘ WŁAŚCIWA ROBOTA
    # ==========================================
    THEME_NAME = "nask"
    THEME_REPO = "https://github.com/jakubklnask/nask_legacy_pages_branding"
    
    try:
        root_path = os.environ.get("TUTOR_ROOT", os.path.expanduser("~/.local/share/tutor"))
        theme_dest = os.path.join(root_path, "env", "build", "openedx", "themes", THEME_NAME)

        print(f"\n++++++ [NASK-THEME] Wykonuję zadanie dla pluginu: {plugin_id}")
        
        # Tworzenie katalogu i klonowanie
        os.makedirs(os.path.dirname(theme_dest), exist_ok=True)
        if os.path.exists(theme_dest):
            subprocess.run(["rm", "-rf", theme_dest], check=True)

        print(f"++++++ [NASK-THEME] Klonowanie repozytorium do: {theme_dest}")
        subprocess.run(["git", "clone", "--depth", "1", THEME_REPO, theme_dest], check=True)
        
        print(f"++++++ [NASK-THEME] Rejestrowanie motywu...")
        subprocess.run(["tutor", "dev", "do", "settheme", THEME_NAME], check=False)

    except Exception as e:
        print(f"++++++ [NASK-THEME] BŁĄD: {e}")

# Rejestracja
atexit.register(nask_theme_host_atexit)