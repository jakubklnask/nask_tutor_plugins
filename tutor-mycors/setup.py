
from setuptools import setup

setup(
    name="tutor-mycors",
    version="0.1.0",
    description="Tutor plugin to add multiple CORS/CSRF origins for edutechnologie.sp.nask.pl, apps.edutechnologie.sp.nask.pl and studio.edutechnologie.sp.nask.pl",
    packages=["mycors"],
    entry_points={
        "tutor.plugin.v1": [
            "mycors = mycors"
        ]
    },
)
