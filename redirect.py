from tutor import hooks

# Patch do Dockerfile - tworzy pliki middleware podczas budowy obrazu
hooks.Filters.ENV_PATCHES.add_item(
    (
        "openedx-dockerfile-post-python-requirements",
        """
RUN mkdir -p /openedx/edx-platform/openedx/core/djangoapps/homepage_redirect && \\
    echo '' > /openedx/edx-platform/openedx/core/djangoapps/homepage_redirect/__init__.py && \\
    echo 'from django.shortcuts import redirect\\n\\
from django.conf import settings\\n\\
\\n\\
class HomepageRedirectMiddleware:\\n\\
    def __init__(self, get_response):\\n\\
        self.get_response = get_response\\n\\
    \\n\\
    def __call__(self, request):\\n\\
        if request.path == "/" and request.method == "GET":\\n\\
            is_dev = getattr(settings, "DEBUG", False)\\n\\
            \\n\\
            if is_dev:\\n\\
                learner_url = "http://apps.local.openedx.io:1996/learner-dashboard/"\\n\\
                authn_url = "http://apps.local.openedx.io:1999/authn/login?next=http%3A%2F%2Flocal.openedx.io%3A8000%2F"\\n\\
            else:\\n\\
                learner_url = "https://apps.edutechnologie.sp.nask.pl/learner-dashboard/"\\n\\
                authn_url = "https://apps.edutechnologie.sp.nask.pl/authn/login?next=%2F"\\n\\
            \\n\\
            if request.user.is_authenticated:\\n\\
                return redirect(learner_url)\\n\\
            else:\\n\\
                return redirect(authn_url)\\n\\
        return self.get_response(request)' > /openedx/edx-platform/openedx/core/djangoapps/homepage_redirect/middleware.py
"""
    )
)

# Dodaje middleware do MIDDLEWARE list w production
hooks.Filters.ENV_PATCHES.add_item(
    (
        "openedx-lms-production-settings",
        """
MIDDLEWARE.append('openedx.core.djangoapps.homepage_redirect.middleware.HomepageRedirectMiddleware')
"""
    )
)

# Dodaje middleware do MIDDLEWARE list w development
hooks.Filters.ENV_PATCHES.add_item(
    (
        "openedx-lms-development-settings",
        """
MIDDLEWARE.append('openedx.core.djangoapps.homepage_redirect.middleware.HomepageRedirectMiddleware')
"""
    )
)

# Redirect PO wylogowaniu (backend setting)
hooks.Filters.ENV_PATCHES.add_items([
    (
        "openedx-lms-development-settings",
        "LOGOUT_REDIRECT_URL = 'http://apps.local.openedx.io:1999/authn/login'"
    ),
    (
        "openedx-lms-production-settings",
        "LOGOUT_REDIRECT_URL = 'https://apps.edutechnologie.sp.nask.pl/authn/login'"
    ),
])
