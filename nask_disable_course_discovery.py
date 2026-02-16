from tutor import hooks

hooks.Filters.ENV_PATCHES.add_items([
    (
        "openedx-common-settings",
        """
FEATURES["ENABLE_COURSE_DISCOVERY"] = False
FEATURES["COURSES_ARE_BROWSABLE"] = False
        """
    )
])
