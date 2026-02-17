from tutor import hooks

__version__ = "1.2.0"

hooks.Filters.ENV_PATCHES.add_item(
    (
        "openedx-lms-common-settings",
        """
# Rejestracja aplikacji - resztę robi apps.ready()
if "nask_azure_auth" not in INSTALLED_APPS:
    INSTALLED_APPS.append("nask_azure_auth")
"""
    )
)