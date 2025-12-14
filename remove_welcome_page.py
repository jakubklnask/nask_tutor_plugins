"""
Homepage Redirect Plugin
Redirects unauthenticated users to login and authenticated users to learner dashboard.
Works dynamically with any LMS_HOST/MFE_HOST configuration.
"""
from tutor import hooks

# For production
hooks.Filters.ENV_PATCHES.add_item(
    (
        "openedx-lms-production-settings",
        """
# Create homepage redirect middleware at runtime
from pathlib import Path
middleware_dir = Path('/openedx/edx-platform/openedx/core/djangoapps/homepage_redirect')
middleware_dir.mkdir(parents=True, exist_ok=True)
(middleware_dir / '__init__.py').write_text('')

middleware_code = '''from django.shortcuts import redirect
from django.conf import settings
from urllib.parse import quote

class HomepageRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        if request.path == "/" and request.method == "GET":
            lms_base = settings.LMS_ROOT_URL
            mfe_host = settings.MFE_CONFIG.get('BASE_URL', '')
            protocol = 'https://' if lms_base.startswith('https') else 'http://'
            is_dev = getattr(settings, 'DEBUG', False)
            
            if is_dev:
                learner_url = f"{protocol}{mfe_host}:1996/learner-dashboard/"
                next_url = f"{lms_base}/"
                authn_url = f"{protocol}{mfe_host}:1999/authn/login?next={quote(next_url, safe='')}"
            else:
                mfe_base = f"{protocol}{mfe_host}"
                learner_url = f"{mfe_base}/learner-dashboard/"
                next_url = f"{lms_base}/"
                authn_url = f"{mfe_base}/authn/login?next={quote(next_url, safe='')}"
            
            if hasattr(request, 'user') and request.user.is_authenticated:
                return redirect(learner_url)
            else:
                return redirect(authn_url)
        
        return self.get_response(request)
'''
(middleware_dir / 'middleware.py').write_text(middleware_code)

auth_idx = next((i for i, m in enumerate(MIDDLEWARE) if 'CacheBackedAuthenticationMiddleware' in m), 19)
MIDDLEWARE.insert(auth_idx + 1, 'openedx.core.djangoapps.homepage_redirect.middleware.HomepageRedirectMiddleware')
        """
    )
)

# For development
hooks.Filters.ENV_PATCHES.add_item(
    (
        "openedx-lms-development-settings",
        """
# Create homepage redirect middleware at runtime
from pathlib import Path
middleware_dir = Path('/openedx/edx-platform/openedx/core/djangoapps/homepage_redirect')
middleware_dir.mkdir(parents=True, exist_ok=True)
(middleware_dir / '__init__.py').write_text('')

middleware_code = '''from django.shortcuts import redirect
from django.conf import settings
from urllib.parse import quote

class HomepageRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        if request.path == "/" and request.method == "GET":
            lms_base = settings.LMS_ROOT_URL
            mfe_host = settings.MFE_CONFIG.get('BASE_URL', '')
            protocol = 'https://' if lms_base.startswith('https') else 'http://'
            is_dev = getattr(settings, 'DEBUG', False)
            
            if is_dev:
                learner_url = f"{protocol}{mfe_host}:1996/learner-dashboard/"
                next_url = f"{lms_base}/"
                authn_url = f"{protocol}{mfe_host}:1999/authn/login?next={quote(next_url, safe='')}"
            else:
                mfe_base = f"{protocol}{mfe_host}"
                learner_url = f"{mfe_base}/learner-dashboard/"
                next_url = f"{lms_base}/"
                authn_url = f"{mfe_base}/authn/login?next={quote(next_url, safe='')}"
            
            if hasattr(request, 'user') and request.user.is_authenticated:
                return redirect(learner_url)
            else:
                return redirect(authn_url)
        
        return self.get_response(request)
'''
(middleware_dir / 'middleware.py').write_text(middleware_code)

auth_idx = next((i for i, m in enumerate(MIDDLEWARE) if 'CacheBackedAuthenticationMiddleware' in m), 19)
MIDDLEWARE.insert(auth_idx + 1, 'openedx.core.djangoapps.homepage_redirect.middleware.HomepageRedirectMiddleware')
        """
    )
)
