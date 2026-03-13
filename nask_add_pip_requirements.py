from tutor import hooks

# override the config value
hooks.Filters.CONFIG_OVERRIDES.add_item(
    ("OPENEDX_EXTRA_PIP_REQUIREMENTS", [
        "git+https://github.com/jakubklnask/openedx-pip-packages@main#subdirectory=nask_azure_auth",
        "git+https://github.com/jakubklnask/openedx-pip-packages@main#subdirectory=nask_filters",
        "git+https://github.com/jakubklnask/openedx-pip-packages@main#subdirectory=tutor-mycors"
    ])
)