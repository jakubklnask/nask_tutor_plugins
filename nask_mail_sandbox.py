from tutor import hooks

# 1. Ensure the internal SMTP container is disabled to avoid conflicts
hooks.Filters.CONFIG_USER.add_items(
    [
        ("RUN_SMTP", False),
        ("EMAIL_BACKEND", "django.core.mail.backends.smtp.EmailBackend"),
    ]
)

# 2. Patch the environment to force the SMTP backend in development
# These patches append the SMTP backend at the very end to override it.
hooks.Filters.ENV_PATCHES.add_items(
    [
        # Force backend for LMS (web) and CMS (studio)
        ("openedx-lms-development-settings", 'EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"'),
        ("openedx-cms-development-settings", 'EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"'),
        
        # Ensure the environment files (lms.env.yml / cms.env.yml) also reflect the change
        ("lms-env", "EMAIL_BACKEND: django.core.mail.backends.smtp.EmailBackend"),
        ("cms-env", "EMAIL_BACKEND: django.core.mail.backends.smtp.EmailBackend"),
    ]
)
