import os
import yaml

CONFIG = os.path.expanduser("~/.config/archive4ml/config")
DEFAULT_STORAGE_DIR = os.path.expanduser("~/.local/archive4ml/storage")

def get_config(config:str=CONFIG):
    if not os.path.exists(config):
        print(f"Config {config} does not exists, use default config.")
        return {}
    with open(config, "r") as stream:
        try:
            c = yaml.safe_load(stream)
            if not isinstance(c, dict):
                raise ValueError(f"Can not load config {config} as dict, get {type(c)}:\n{c}")
            return c
        except yaml.YAMLError as exc:
            print(exc)
            raise ValueError(f"Read invilid config {config}.")

c:dict = get_config()

storage_dir = c.get("storage", DEFAULT_STORAGE_DIR)
# print(f"Get storage dir {storage_dir}")

# print("-"*100)
def get_storage_dir():
    return storage_dir