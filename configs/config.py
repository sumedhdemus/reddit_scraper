import os
import json
import pathlib


config_dir_path = pathlib.Path(__file__).absolute().parent.absolute()
environment = os.getenv("APP_ENV", "dev")

env_file_names_map = {"dev": "dev_config.json"}


def get_config() -> dict:
    """ reads json file from config_file_path, and returns a dictionsary """

    config_file_path = os.path.join(config_dir_path, env_file_names_map[environment])

    if not os.path.exists(config_file_path):
        raise FileNotFoundError(f"config file not found in location {config_file_path}")

    with open(config_file_path, "r") as f:
        config = json.load(f)
    return config
