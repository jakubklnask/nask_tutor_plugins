from tutor import hooks

hooks.Filters.ENV_PATCHES.add_item(
    (
        "openedx-lms-common-settings",
        """
OPEN_EDX_FILTERS_CONFIG = {
    # 1. Filtr Logowania (Auto-Enroll)
    "org.openedx.learning.student.login.requested.v1": {
        "fail_silently": False,
        "pipeline": [
            "nask_filters.pipeline.AutoEnrollByCorpEmail"
        ]
    },
    
    # 2. Filtr Renderowania Dashboardu (Pieczątka)
    "org.openedx.learning.home.enrollment.api.rendered.v1": {
        "fail_silently": False,
        "pipeline": [
            "nask_filters.pipeline.StampCoursesForDashboard"
        ]
    }
}
"""
    )
)

hooks.Filters.ENV_PATCHES.add_item(
    (
        "openedx-lms-common-settings",
        "INSTALLED_APPS.append('nask_filters')"
    )
)
