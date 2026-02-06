from tutor import hooks

hooks.Filters.ENV_PATCHES.add_item(
    (
        "openedx-common-settings",
        "FEATURE['SKIP_EMAIL_VALIDATION'] = True",
    )
)
