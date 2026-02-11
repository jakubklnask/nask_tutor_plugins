"""
Increases CMS file upload limit to 1000MB for course imports. Removes 250 MB Caddy limit
THIS PLUGIN IS ONLY PART OF THE SOLUTION - CHANGES REQUIRED IN THE AUTHORING MFE! HARDCODED VALUES TEHRE
MARKED WITH //HARD_CODED_MAX_FILE_SIZE_HERE

"""
from tutor import hooks
import os
import re
import atexit

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
    """Fix Caddyfile when Python exits (after all rendering is done)"""
    caddy_file = "/home/edutechnologie/.local/share/tutor/env/apps/caddy/Caddyfile"
    
    if os.path.exists(caddy_file):
        try:
            with open(caddy_file, 'r') as f:
                content = f.read()
            
            original = content
            content = re.sub(
                r'    handle_path /\* \{\s+        request_body \{\s+            max_size 250MB\s+        \}\s+    \}',
                '',
                content
            )
            
            if content != original:
                with open(caddy_file, 'w') as f:
                    f.write(content)
                #print("\n[NASK PLUGIN] Sukces")
        except Exception:
            pass

# Register the cleanup to run when Python exits
atexit.register(fix_caddyfile_atexit)
