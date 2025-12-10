from tutor import hooks

hooks.Filters.ENV_PATCHES.add_item(
    (
        "openedx-cms-production-settings",
        "MAX_ASSET_UPLOAD_FILE_SIZE_IN_MB = 250"
    )
)

hooks.Filters.ENV_PATCHES.add_item(
    (
        "openedx-cms-development-settings",
        "MAX_ASSET_UPLOAD_FILE_SIZE_IN_MB = 250"
    )
)

hooks.Filters.ENV_PATCHES.add_item(
    (
        "caddyfile-cms",
        """
        handle_path /import/* {
            request_body {
                max_size 250MB
            }
        }
        """
    )
)
