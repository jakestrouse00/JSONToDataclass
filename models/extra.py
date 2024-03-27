from dataclasses import dataclass, field
from typing import *
from enum import Enum
import configparser

"""
needed code blocks:
Class block
argument block

"""


class EmptyValue:
    def __init__(self):
        ...



@dataclass
class FieldInput:
    repr: bool = field(default=True)
    init: bool = field(default=True)
    hash: bool = field(default=False)
    compare: bool = field(default=False)
    validation_alias: str = field(default_factory=EmptyValue)
    union_mode: str = field(default_factory=EmptyValue)
    default: Any = field(default_factory=EmptyValue)

    def __post_init__(self):
        if isinstance(self.default, str):
            self.default = f'"{self.default}"'

        if isinstance(self.validation_alias, str):
            self.validation_alias = f'"{self.validation_alias}"'

        if isinstance(self.union_mode, str):
            self.union_mode = f'"{self.union_mode}"'






def load_config():
    config = configparser.ConfigParser()
    config.read("config.ini")

    # Assuming the configuration file has a section called 'Settings'
    # and the keys correspond to your command-line arguments
    config_dict = {}
    config_dict.update({k: v for k, v in config['input'].items()})
    config_dict.update({k: v for k, v in config['output'].items()})
    config_dict.update({k: v for k, v in config['options'].items()})
    config_dict["repr"] = config.getboolean("options", "repr")
    return config_dict


@dataclass
class ConfigArgs:
    object_name: str
    file: str | None
    json: str | None

    output_file: str
    static_method: str

    repr: bool

    def __post_init__(self):
        # logic for checking if string len == 0, then set to None
        for index, (key, value) in enumerate(self.__dict__.items()):
            if isinstance(value, str):
                if len(value) == 0:
                    self.__setattr__(key, None)
        if self.output_file is None:
            self.output_file = "testing"
