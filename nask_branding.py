"""
NASK Branding (Logo & Favicon)
Sets custom NASK logos and favicon in MFE applications.
"""
from tutor import hooks

hooks.Filters.ENV_PATCHES.add_items([
    (
        "openedx-lms-development-settings",
        """
MFE_CONFIG["LOGO_URL"] = "https://raw.githubusercontent.com/jakubklnask/openedx-nask-static-assets/refs/heads/nask-custom/cyber_logo_black.svg"
MFE_CONFIG["LOGO_TRADEMARK_URL"] = "https://raw.githubusercontent.com/jakubklnask/openedx-nask-static-assets/refs/heads/nask-custom/cyber_logo_black.svg"
MFE_CONFIG["LOGO_WHITE_URL"] = "https://raw.githubusercontent.com/jakubklnask/openedx-nask-static-assets/refs/heads/nask-custom/cyber_logo_white.svg"
MFE_CONFIG["FAVICON_URL"] = "https://raw.githubusercontent.com/jakubklnask/openedx-nask-static-assets/refs/heads/nask-custom/favicon.ico"
"""
    ),
    (
        "openedx-lms-production-settings",
        """
MFE_CONFIG["LOGO_URL"] = "https://raw.githubusercontent.com/jakubklnask/openedx-nask-static-assets/refs/heads/nask-custom/cyber_logo_black.svg"
MFE_CONFIG["LOGO_TRADEMARK_URL"] = "https://raw.githubusercontent.com/jakubklnask/openedx-nask-static-assets/refs/heads/nask-custom/cyber_logo_black.svg"
MFE_CONFIG["LOGO_WHITE_URL"] = "https://raw.githubusercontent.com/jakubklnask/openedx-nask-static-assets/refs/heads/nask-custom/cyber_logo_white.svg"
MFE_CONFIG["FAVICON_URL"] = "https://raw.githubusercontent.com/jakubklnask/openedx-nask-static-assets/refs/heads/nask-custom/favicon.ico"
"""
    ),
])
