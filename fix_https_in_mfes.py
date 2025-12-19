from tutor import hooks

def _patch_mfe_urls():
    lines = ["# --- tutor-mycors: Fix MFE URLs to HTTPS ---"]
    mfe_vars = [
        "AUTHN_MICROFRONTEND_URL",
        "AUTHN_MICROFRONTEND_DOMAIN",
        "ACCOUNT_MICROFRONTEND_URL",
        "DISCUSSIONS_MICROFRONTEND_URL",
        "WRITABLE_GRADEBOOK_URL",
        "LEARNER_HOME_MICROFRONTEND_URL",
        "LEARNING_MICROFRONTEND_URL",
        "ORA_GRADING_MICROFRONTEND_URL",
        "PROFILE_MICROFRONTEND_URL",
        "COMMUNICATIONS_MICROFRONTEND_URL",
    ]
    for var in mfe_vars:
        lines.append(f'{var} = {var}.replace("http://", "https://")')
    
    return "\n".join(lines)

hooks.Filters.ENV_PATCHES.add_item((
    "openedx-lms-production-settings",
    _patch_mfe_urls(),
))
