"""
NASK 1GB File Upload Limit
Increases CMS file upload limit to 1000MB for course imports.
"""
from tutor import hooks

hooks.Filters.ENV_PATCHES.add_items([
    ("openedx-cms-production-settings", "MAX_ASSET_UPLOAD_FILE_SIZE_IN_MB = 1000"),
    ("openedx-cms-development-settings", "MAX_ASSET_UPLOAD_FILE_SIZE_IN_MB = 1000"),
    (
        "caddyfile-cms",
        """
        handle_path /import/* {
            request_body {
                max_size 1000MB
            }
        }
        """
    ),
])
