"""
Tutor plugin to override ATLAS_REPOSITORY configuration.

This plugin sets a custom translations repository instead of the default
openedx/openedx-translations by overriding the config value. The config
value is then used in the Dockerfile template as {{ ATLAS_REPOSITORY }}.

HOW IT WORKS:
1. CONFIG_OVERRIDES modifies the value in config.yml
2. The Dockerfile template uses {{ ATLAS_REPOSITORY }} as a Jinja2 variable
3. When you run `tutor config save`, templates are rendered with the new value
4. When you run `tutor images build openedx`, it uses the rendered Dockerfile
"""
from tutor import hooks

# Override the ATLAS_REPOSITORY configuration
# Change this to your custom repository
hooks.Filters.CONFIG_OVERRIDES.add_item(
    ("ATLAS_REPOSITORY", "jakubklnask/openedx-translations")
)
    
# It is also possible to override ATLAS_REVISION using specific branch/tag
hooks.Filters.CONFIG_OVERRIDES.add_item(
    ("ATLAS_REVISION", "nask-custom")
)
