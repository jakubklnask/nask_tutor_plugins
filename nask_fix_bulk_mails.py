from tutor import hooks

# Nazwa i wersja pluginu
__version__ = "1.0.0"

# Używamy patcha 'openedx-lms-development-settings'
# Ten patch jest wstrzykiwany TYLKO do pliku settings/lms/development.py
hooks.Filters.ENV_PATCHES.add_item(
    (
        "openedx-lms-development-settings",
        "\n# Fix for Bulk Email session killing in dev mode\nENFORCE_SAFE_SESSIONS = False"
    )
)

# Analogicznie dla CMS (Studio), jeśli tam też wysyłasz maile
hooks.Filters.ENV_PATCHES.add_item(
    (
        "openedx-cms-development-settings",
        "\n# Fix for Bulk Email session killing in dev mode\nENFORCE_SAFE_SESSIONS = False"
    )
)