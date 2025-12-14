"""
Clean Logout Plugin
Skips the legacy logout confirmation page and redirects directly.
"""
from tutor import hooks

hooks.Filters.ENV_PATCHES.add_item(
    (
        "openedx-lms-production-settings",
        """
# Monkey-patch logout view at runtime
from pathlib import Path
logout_file = Path('/openedx/edx-platform/openedx/core/djangoapps/user_authn/views/logout.py')
if logout_file.exists():
    content = logout_file.read_text()
    if 'response = super().dispatch(request, *args, **kwargs)' in content:
        content = content.replace(
            'response = super().dispatch(request, *args, **kwargs)',
            'response = redirect(self.target)'
        )
        logout_file.write_text(content)
        """
    )
)

hooks.Filters.ENV_PATCHES.add_item(
    (
        "openedx-lms-development-settings",
        """
# Monkey-patch logout view at runtime
from pathlib import Path
logout_file = Path('/openedx/edx-platform/openedx/core/djangoapps/user_authn/views/logout.py')
if logout_file.exists():
    content = logout_file.read_text()
    if 'response = super().dispatch(request, *args, **kwargs)' in content:
        content = content.replace(
            'response = super().dispatch(request, *args, **kwargs)',
            'response = redirect(self.target)'
        )
        logout_file.write_text(content)
        """
    )
)
