
from tutor import hooks

# Dodaj tutaj wszystkie originy, które mają być dopuszczone
ORIGINS = [
    "https://edutechnologie.sp.nask.pl",
    "https://apps.edutechnologie.sp.nask.pl",
    "https://studio.edutechnologie.sp.nask.pl",
]

def _patch_block(origins):
    lines = ["# --- tutor-mycors: CORS/CSRF ---"]
    # CORS
    lines.append("try:\n    CORS_ORIGIN_WHITELIST\nexcept NameError:\n    CORS_ORIGIN_WHITELIST = []")
    for o in origins:
        lines.append(f'if "{o}" not in CORS_ORIGIN_WHITELIST:\n    CORS_ORIGIN_WHITELIST.append("{o}")')
    # CSRF (Django >= 4.0 wymaga schematu https:// w wpisach)
    lines.append("try:\n    CSRF_TRUSTED_ORIGINS\nexcept NameError:\n    CSRF_TRUSTED_ORIGINS = []")
    for o in origins:
        lines.append(f'if "{o}" not in CSRF_TRUSTED_ORIGINS:\n    CSRF_TRUSTED_ORIGINS.append("{o}")')
    # (opcjonalnie) jeśli używasz ciasteczek między domenami:
    lines.append("CORS_ALLOW_CREDENTIALS = True")
    
    return "\n".join(lines)

# Patch dla LMS (production)
hooks.Filters.ENV_PATCHES.add_item((
    "openedx-lms-production-settings",
    _patch_block(ORIGINS),
))

# Patch dla CMS/Studio (production)
hooks.Filters.ENV_PATCHES.add_item((
    "openedx-cms-production-settings",
    _patch_block(ORIGINS),
))
