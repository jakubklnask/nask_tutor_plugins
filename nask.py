from tutor import hooks
from tutormfe.hooks import MFE_APPS

# Add custom NASK MFE repositories
@MFE_APPS.add()
def _add_nask_mfes(mfes):
    mfes["account"] = {"repository": "https://github.com/jakubklnask/frontend-app-account.git", "version": "nask-custom", "port": 1997}
    mfes["authn"] = {"repository": "https://github.com/jakubklnask/frontend-app-authn.git", "version": "nask-custom", "port": 1999}
    mfes["authoring"] = {"repository": "https://github.com/jakubklnask/frontend-app-authoring.git", "version": "nask-custom", "port": 2001}
    mfes["learner-dashboard"] = {"repository": "https://github.com/jakubklnask/frontend-app-learner-dashboard.git", "version": "nask-custom", "port": 1996}
    mfes["learning"] = {"repository": "https://github.com/jakubklnask/frontend-app-learning.git", "version": "nask-custom", "port": 2000}
    return mfes

# Install wget in base image
hooks.Filters.ENV_PATCHES.add_item(
    ("mfe-dockerfile-base", "RUN apt update && apt install -y wget")
)

# Download custom env.config.jsx for each MFE
hooks.Filters.ENV_PATCHES.add_items([
    ("mfe-dockerfile-pre-npm-build-learner-dashboard", "RUN wget -q https://raw.githubusercontent.com/jakubklnask/frontend-app-learner-dashboard/nask-custom/env.config.jsx -O /openedx/app/env.config.jsx || echo 'Using default'"),
    ("mfe-dockerfile-pre-npm-build-learning", "RUN wget -q https://raw.githubusercontent.com/jakubklnask/frontend-app-learning/nask-custom/env.config.jsx -O /openedx/app/env.config.jsx || echo 'Using default'"),
    ("mfe-dockerfile-pre-npm-build-account", "RUN wget -q https://raw.githubusercontent.com/jakubklnask/frontend-app-account/nask-custom/env.config.jsx -O /openedx/app/env.config.jsx || echo 'Using default'"),
    ("mfe-dockerfile-pre-npm-build-authn", "RUN wget -q https://raw.githubusercontent.com/jakubklnask/frontend-app-authn/nask-custom/env.config.jsx -O /openedx/app/env.config.jsx || echo 'Using default'"),
    ("mfe-dockerfile-pre-npm-build-authoring", "RUN wget -q https://raw.githubusercontent.com/jakubklnask/frontend-app-authoring/nask-custom/env.config.jsx -O /openedx/app/env.config.jsx || echo 'Using default'"),
])

# Override MFE_CONFIG in LMS settings
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

# Increase file upload limits (from big_file plugin)
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
