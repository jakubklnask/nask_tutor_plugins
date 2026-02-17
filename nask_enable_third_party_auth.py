from tutor import hooks

hooks.Filters.ENV_PATCHES.add_items([
    # 1. Enable the global feature flag (Equivalent to FEATURES in lms.yml)
    (
        "common-env-features",
        '"ENABLE_THIRD_PARTY_AUTH": true'
    ),
    
    # 2. Pass the secret (This targets auth.yml, the 'secure' part of lms.yml)
    (
        "openedx-auth",
        '"SOCIAL_AUTH_OAUTH_SECRETS": {"google-oauth2": "PASTE_THE_KEY_HERE_FROM_GCP"}'
    ),

])
