from tutor import hooks
import os
import atexit
import textwrap

def fix_superset_rls_indentation():
    """
    Finds the injected RLS code using markers and strips the erroneous 
    base indentation introduced by Jinja patching.
    """
    try:
        # Resolves path natively in Python (no subprocess deadlocks)
        root_path = os.environ.get("TUTOR_ROOT", os.path.expanduser("~/.local/share/tutor"))
        
        target_file = os.path.join(
            root_path, 
            "env", "plugins", "aspects", "apps", "superset", 
            "pythonpath", "openedx", "create_row_level_security.py"
        )

        if os.path.exists(target_file):
            with open(target_file, 'r') as file:
                content = file.read()

            if '#BEGINNING_OF_NEW_RLS' in content and '#END_OF_NEW_RLS' in content:
                # Slice the file into three parts: Before, Inside, After
                pre_marker, rest = content.split('#BEGINNING_OF_NEW_RLS', 1)
                block, post_marker = rest.split('#END_OF_NEW_RLS', 1)

                # Dedent removes the common leading whitespace cleanly
                fixed_block = textwrap.dedent(block)

                # Reassemble the file without markers
                new_content = pre_marker + fixed_block + post_marker
                
                with open(target_file, 'w') as file:
                    file.write(new_content)
                
    except Exception as e:
        # Fails silently to not disrupt the CLI exit, just like your other plugin
        pass

# Trigger this function exactly when the Tutor process cleanly exits
atexit.register(fix_superset_rls_indentation)

# 1. SSO: Przypisanie roli Gamma i SQL Lab dla analityka
hooks.Filters.ENV_PATCHES.add_item(
    ("superset-sso-assignment-rules", """
email = decoded_access_token.get("email", "").lower()
if email == "sagrodat333@gmail.com" or email == "jakubklnkwcz@gmail.com":
    return ["gamma"]
"""))

hooks.Filters.ENV_PATCHES.add_item(
    ("superset-row-level-security", """
#BEGINNING_OF_NEW_RLS
SECURITY_FILTERS.append({
    "name": "gamma_rls_event_sink",
    "schema": "event_sink",
    "exclude": ["user_pii"],
    "role_name": "Gamma",
    "group_key": "xapi_course_id",
    "clause": {% raw %}'{{ can_analyze_courses(current_username(), "course_key") }}'{% endraw %},
    "filter_type": "Regular",
})

SECURITY_FILTERS.append({
    "name": "gamma_rls_reporting",
    "schema": "reporting",
    "exclude": [],
    "role_name": "Gamma",
    "group_key": "xapi_course_id",
    "clause": {% raw %}'{{ can_analyze_courses(current_username(), "course_key") }}'{% endraw %},
    "filter_type": "Regular",
})

SECURITY_FILTERS.append({
    "name": "gamma_rls_xapi",
    "schema": "xapi",
    "exclude": [],
    "role_name": "Gamma",
    "group_key": "xapi_course_id",
    "clause": {% raw %}'{{ can_analyze_courses(current_username(), "splitByChar(\\'/\\', course_id)[-1]") }}'{% endraw %},
    "filter_type": "Regular",
})
#END_OF_NEW_RLS
""")
)

#3. CONFIG: Zmieniamy z .update() na bezpieczne przypisanie lub inicjalizację
hooks.Filters.ENV_PATCHES.add_item(
    ("superset-config-docker", """
# 1. Najpierw upewniamy się, że nasza funkcja jest zaimportowana w tym kontekście
from openedx_jinja_filters import can_analyze_courses

# 2. Bezpiecznie aktualizujemy słownik w pamięci

JINJA_CONTEXT_ADDONS.update({
    'can_analyze_courses': can_analyze_courses,
})

""")
)
# 4. JINJA: Definicja logiki filtra filtrującego po organizacji PESA
hooks.Filters.ENV_PATCHES.add_item(
    ("superset-jinja-filters", """
from superset.extensions import cache_manager
from flask import session, current_app
def get_courses_by_org(sm, username, org, next_url=None, force=False):
    # Pobiera kursy dla organizacji i zrzuca logi API.
    log.info(f"[DEBUG RLS - API] Fetching org: '{org}' for '{username}'")
    
    cache = cache_manager.cache
    cache_key = f"{username}+org+{org}"

    if not next_url and not force:
        obj = cache.get(cache_key)
        if obj is not None:
            return obj

    courses = []
    provider = session.get("oauth_provider")
    oauth_remote = sm.oauth_remotes.get(provider)
    
    if not oauth_remote:
        log.error("[DEBUG RLS - API] No OAuth remote")
        return courses

    token = sm.get_oauth_token()
    if not token:
        log.error("[DEBUG RLS - API] No token")
        return courses

    if next_url:
        url = next_url
    else:
        raw_url = current_app.config["OPENEDX_API_URLS"]["get_courses"]
        base_url = raw_url.split('?')[0]
        url = f"{base_url}?username={username}&org={org}"

    log.info(f"[DEBUG RLS - API] Calling URL: {url}")

    try:
        resp = oauth_remote.get(url, token=token)
        # TUTAJ DODAJEMY LOGOWANIE ZWROTKI Z API
        log.info(f"[DEBUG RLS - API] API Status: {resp.status_code}")
        log.info(f"[DEBUG RLS - API] API Response: {resp.text}")
        
        resp.raise_for_status()
        response = resp.json()
    except Exception as e:
        log.error(f"[DEBUG RLS - API] Request failed: {str(e)}")
        return courses

    results = response.get("results", [])
    for course in results:
        course_id = course.get("course_id")
        if course_id:
            courses.append(course_id)

    if response.get("next"):
        # Uwaga: zmienione wywolanie rekurencyjne na lokalna funkcje
        next_courses = get_courses_by_org(
            sm, username, org=org, next_url=response["next"]
        )
        courses.extend(next_courses)

    if not next_url:
        cache.set(cache_key, courses, timeout=300)

    return courses


def can_analyze_courses(username, field_name="course_id", **kwargs):
    # Zwraca klauzule RLS
    log.info(f"[DEBUG RLS - JINJA] Evaluating for '{username}'")
    
    user = security_manager.get_user_by_username(username)
    user_roles = security_manager.get_user_roles(user) if user else []

    if not user_roles:
        return NO_COURSES

    for role in user_roles:
        if str(role) in ["Admin", "Alpha"]:
            return ALL_COURSES

    user_org = "PESA" 
    
    try:
        # Uwaga: Zmieniono wywolanie na bezposrednie z przekazaniem security_manager
        courses = get_courses_by_org(security_manager, username, org=user_org, force=True) 
        log.info(f"[DEBUG RLS - JINJA] Found {len(courses)} courses")
    except Exception as e:
        log.error(f"[DEBUG RLS - JINJA] Error fetching courses: {str(e)}")
        courses = []

    if courses:
        course_id_list = ", ".join(f"'{course_id}'" for course_id in courses)
        return f"{field_name} in ({course_id_list})"
    else:
        log.warning("[DEBUG RLS - JINJA] Course list empty. Returning 1=0.")
        return NO_COURSES
"""))