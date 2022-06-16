import environ

environ.Env.read_env(env_file="itests/.env")

from config.settings import *
