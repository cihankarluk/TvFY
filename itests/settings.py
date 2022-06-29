import os

import environ

environ.Env.read_env(env_file="itests/.env")

from config.settings import *  # noqa: F403, F401, E402

TEST_DATASET_DIR = os.path.join(BASE_DIR, "tests", "dataset")  # noqa: F405
