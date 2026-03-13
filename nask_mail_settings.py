from tutor import hooks

hooks.Filters.CONFIG_USER.add_items([
    ("RUN_SMTP", False),
])

hooks.Filters.ENV_PATCHES.add_items([
    # Ustawienia Pythona (używamy średników, to działa w Pythonie)
    ("openedx-lms-development-settings", 'EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend" ; EMAIL_USE_COURSE_ID_FROM_FOR_BULK = False ; BULK_EMAIL_DEFAULT_FROM_EMAIL = "edu.technologie@nask.pl" ; DEFAULT_FROM_EMAIL = "edu.technologie@nask.pl"'),
    ("openedx-cms-development-settings", 'EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend" ; DEFAULT_FROM_EMAIL = "edu.technologie@nask.pl"'),

    ("openedx-lms-development-settings", 'BULK_EMAIL_SEND_USING_EDX_ACE = False'),
    ("openedx-cms-development-settings", 'BULK_EMAIL_SEND_USING_EDX_ACE = False'),

    ("openedx-lms-production-settings", 'EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend" ; EMAIL_USE_COURSE_ID_FROM_FOR_BULK = False ; BULK_EMAIL_DEFAULT_FROM_EMAIL = "edu.technologie@nask.pl" ; DEFAULT_FROM_EMAIL = "edu.technologie@nask.pl"'),
    ("openedx-cms-production-settings", 'EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend" ; DEFAULT_FROM_EMAIL = "edu.technologie@nask.pl"'),

    ("openedx-lms-production-settings", 'BULK_EMAIL_SEND_USING_EDX_ACE = False'),
    ("openedx-cms-production-settings", 'BULK_EMAIL_SEND_USING_EDX_ACE = False'),
    
    
    # Ustawienia YAML (rozbite na osobne wpisy, żeby uniknąć przecinków i \n)
    ("lms-env", "BULK_EMAIL_DEFAULT_FROM_EMAIL: edu.technologie@nask.pl"),
    ("lms-env", "EMAIL_USE_COURSE_ID_FROM_FOR_BULK: false"),
    ("lms-env", "DEFAULT_FROM_EMAIL: edu.technologie@nask.pl"),
    ("lms-env", "EMAIL_BACKEND: django.core.mail.backends.smtp.EmailBackend"),
    ("cms-env", "DEFAULT_FROM_EMAIL: edu.technologie@nask.pl"),
    ("cms-env", "EMAIL_BACKEND: django.core.mail.backends.smtp.EmailBackend"),
])