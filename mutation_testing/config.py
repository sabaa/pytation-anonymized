from dataclasses import dataclass


@dataclass
class Config:
    """
    This class is used to store user configuration for the mutation testing framework.
    """
    equivalency_check: bool = True
    mutation: bool = True
    detection: bool = True
    logging: bool = True
    subset_selection: bool = False


class ConfigManager:
    __instance = None

    @classmethod
    def get_config(cls):
        if cls.__instance is None:
            cls.__instance = Config()
        return cls.__instance

    @classmethod
    def set_config(cls, config):
        if cls.__instance is None:
            cls.__instance = config
        else:
            raise AttributeError('Config already set.')
