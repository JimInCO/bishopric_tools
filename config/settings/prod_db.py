import environ
from .local import *  # noqa

env = environ.Env()
ROOT_DIR = environ.Path(__file__) - 3  # (bishopric_tools/config/settings/base.py - 3 = bishopric_tools/)
env.read_env(str(ROOT_DIR.path(".env")))

DATABASES = {"default": env.db("PROD_URL")}
DATABASES["default"]["ATOMIC_REQUESTS"] = True
