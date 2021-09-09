import os

import environ

environ.Env.read_env(env_file="tests/.env")

from config.settings import *

TEST_DATASET_DIR = os.path.join(BASE_DIR, "tests", "dataset")
