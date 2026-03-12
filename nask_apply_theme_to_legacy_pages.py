import os
import subprocess
import atexit
import sys
from tutor import hooks

#plugin poczatkowo zrobiony przy pomocy hijackowania komendy init jednak nie moze byc
#wykonywany na poczatku poniewaz tutor do setthemes uruchamia kontener ktory 
#rozmawia z mysql i mongodb
#a na samym poczatku komendy init serwisy te nie sa jeszcze zainicjalizowane
#dlatego uruchamiamy na koncy atexit.
#niezbyt czyste rozwiazanie ale dosyc pewne 

def nask_theme_host_atexit():
    """
    Funkcja odpali się przy zamykaniu procesu Tutora.
    Sprawdzamy, czy wywołana komenda to 'init' i jeśli tak - robimy robotę na hoście.
    """
    # Sprawdzamy, czy w argumentach wywołania było "init"
    # Szukamy kombinacji ['dev', 'do', 'init'] lub ['local', 'do', 'init']
    args = " ".join(sys.argv)
    if "do init" not in args:
        return

    THEME_NAME = "nask"
    THEME_REPO = "https://github.com/jakubklnask/nask_legacy_pages_branding"
    
    try:
        root_path = os.environ.get("TUTOR_ROOT", os.path.expanduser("~/.local/share/tutor"))
        # Ścieżka, gdzie Tutor spodziewa się motywów
        theme_dest = os.path.join(root_path, "env", "build", "openedx", "themes", THEME_NAME)

        print(f"\n++++++ [NASK-THEME] atexit: Wykryto 'init'. Przygotowuję motyw w: {theme_dest}")

        # 1. Tworzymy katalog nadrzędny, jeśli go nie ma
        os.makedirs(os.path.dirname(theme_dest), exist_ok=True)

        # 2. Jeśli folder motywu już istnieje, usuwamy go (żeby mieć świeży klon)
        if os.path.exists(theme_dest):
            subprocess.run(["rm", "-rf", theme_dest], check=True)

        # 3. Klonujemy repozytorium na hosta
        print(f"++++++ [NASK-THEME] Klonowanie repozytorium {THEME_NAME}...")
        subprocess.run(["git", "clone", THEME_REPO, theme_dest], check=True)
        
        # 4. OPCJONALNIE: Jeśli musisz odpalić 'settheme' wewnątrz kontenera, 
        # ale bez przerywania procesu (check=False)
        print("++++++ [NASK-THEME] Rejestrowanie motywu w bazie (opcjonalnie)...")
        subprocess.run(["tutor", "dev", "do", "settheme", THEME_NAME], check=False)

        print("++++++ [NASK-THEME] Gotowe!\n")

    except Exception as e:
        print(f"++++++ [NASK-THEME] BŁĄD w atexit: {e}")

# Rejestrujemy funkcję
atexit.register(nask_theme_host_atexit)