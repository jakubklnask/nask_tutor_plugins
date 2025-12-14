"""
NASK Custom MFE Repositories
Defines custom NASK MFE repositories from GitHub.
"""
from tutor import hooks
from tutormfe.hooks import MFE_APPS

@MFE_APPS.add()
def _add_nask_mfes(mfes):
    mfes["account"] = {
        "repository": "https://github.com/jakubklnask/frontend-app-account.git",
        "version": "nask-custom",
        "port": 1997
    }
    mfes["authn"] = {
        "repository": "https://github.com/jakubklnask/frontend-app-authn.git",
        "version": "nask-custom",
        "port": 1999
    }
    mfes["authoring"] = {
        "repository": "https://github.com/jakubklnask/frontend-app-authoring.git",
        "version": "nask-custom",
        "port": 2001
    }
    mfes["learner-dashboard"] = {
        "repository": "https://github.com/jakubklnask/frontend-app-learner-dashboard.git",
        "version": "nask-custom",
        "port": 1996
    }
    mfes["learning"] = {
        "repository": "https://github.com/jakubklnask/frontend-app-learning.git",
        "version": "nask-custom",
        "port": 2000
    }
    mfes["profile"] = {
        "repository": "https://github.com/jakubklnask/frontend-app-profile.git",
        "version": "nask-custom",
        "port": 1995
    }
    return mfes
