
from tutor import hooks

# override the config value
hooks.Filters.CONFIG_OVERRIDES.add_item(
    ("OPENEDX_EXTRA_PIP_REQUIREMENTS", [
        "git+https://github.com/jakubklnask/nask_filters@main",
        "git+https://github.com/jakubklnask/nask_azure_auth@main"
    ])
)
    

