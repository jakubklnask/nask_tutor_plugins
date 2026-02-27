from tutor import hooks
import os
import re
import atexit

# Rejestracja standardowych patchy Tutor
hooks.Filters.ENV_PATCHES.add_items([
    ("openedx-cms-production-settings", "MAX_ASSET_UPLOAD_FILE_SIZE_IN_MB = 1000"),
    ("openedx-cms-development-settings", "MAX_ASSET_UPLOAD_FILE_SIZE_IN_MB = 1000"),
    (
        "caddyfile-cms",
        """
        request_body {
            max_size 1000MB
        }
        """
    ),
])

def fix_caddyfile_atexit():
    """
    Usuwa hardkodowany limit 250MB z Caddyfile, wykorzystując dynamiczną 
    ścieżkę projektu Tutor.
    """
    try:
        # Dynamiczne rozwiązanie ścieżki (zgodnie ze wzorcem)
        root_path = os.environ.get("TUTOR_ROOT", os.path.expanduser("~/.local/share/tutor"))
        
        caddy_file = os.path.join(
            root_path, 
            "env", "apps", "caddy", "Caddyfile"
        )
        
        if os.path.exists(caddy_file):
            with open(caddy_file, 'r') as f:
                content = f.read()
            
            original = content
            # Usuwamy domyślny blok handle_path z limitem 250MB
            # Używamy regex, aby dopasować specyficzne formatowanie Tutor
            content = re.sub(
                r'    handle_path /\* \{\s+        request_body \{\s+            max_size 250MB\s+        \}\s+    \}',
                '',
                content
            )
            
            if content != original:
                with open(caddy_file, 'w') as f:
                    f.write(content)
                    
    except Exception:
        # Ciche niepowodzenie, aby nie blokować wyjścia z CLI
        pass

# Rejestracja funkcji przy zakończeniu procesu Pythona
atexit.register(fix_caddyfile_atexit)