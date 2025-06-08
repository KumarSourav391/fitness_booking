from .local import LocalConfig
from .dev import DevConfig
from .prod import ProdConfig

def get_config(env):
    config_map = {
        "local": LocalConfig,
        "dev": DevConfig,
        "prod": ProdConfig
    }
    return config_map.get(env, LocalConfig)