from tutor import hooks

# Dla tutor local - NIE SPRAWDZONE
hooks.Filters.ENV_PATCHES.add_item(
    (
        "openedx-dockerfile-post-python-requirements",
        """
RUN sed -i 's/response = super().dispatch(request, \\*args, \\*\\*kwargs)/response = redirect(self.target)/' \
    /openedx/edx-platform/openedx/core/djangoapps/user_authn/views/logout.py
        """
    )
)

# Dla dev - patch w settings (wykona się przy starcie) - BRUDNE ALE DLA DEV sed NIE DZIALA!
hooks.Filters.ENV_PATCHES.add_item(
    (
        "openedx-lms-development-settings",
        """
# Monkey-patch logout view at runtime
import sys
from pathlib import Path
logout_file = Path('/openedx/edx-platform/openedx/core/djangoapps/user_authn/views/logout.py')
if logout_file.exists():
    content = logout_file.read_text()
    content = content.replace(
        'response = super().dispatch(request, *args, **kwargs)',
        'response = redirect(self.target)'
    )
    logout_file.write_text(content)
        """
    )
)
