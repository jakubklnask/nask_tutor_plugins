from tutor import hooks

hooks.Filters.ENV_PATCHES.add_item(
    (
        "common-env-features",
        """
"SKIP_EMAIL_VALIDATION": true
"""
    )
)

