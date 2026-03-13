from tutor import hooks
hooks.Filters.CONFIG_OVERRIDES.add_items([
    ("MFE_HOST", 'apps.edu.technologie.sp.nask.pl'),
    ("LMS_HOST",'edu.technologie.sp.nask.pl'),
    ("CMS_HOST",'studio.edu.technologie.sp.nask.pl'),
    ("MEILISEARCH_HOST",'meilisearch.edu.technologie.sp.nask.pl'),
    ("SUPERSET_HOST",'superset.edu.technologie.sp.nask.pl')
])