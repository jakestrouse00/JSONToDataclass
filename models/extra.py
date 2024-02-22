from dataclasses import dataclass, field
from typing import *
from enum import Enum

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
    default: Any = field(default_factory=EmptyValue)

    def __post_init__(self):
        if isinstance(self.default, str):
            self.default = f'"{self.default}"'


class StaticMethods(str, Enum):
    json_out = '\n    @staticmethod\n    def convert_data(input_data: dict) -> dict:\n        new_data = {}\n        for index, (key, value) in enumerate(input_data.items()):\n            '+'if key in list({}.__annotations__.keys()):\n                new_data[key] = value\n        return new_data'
    object_out = '\n    @staticmethod\n    def convert_data(input_data: dict) -> {}:\n        new_data = {}\n        for index, (key, value) in enumerate(input_data.items()):\n            if key in list({}.__annotations__.keys()):\n                new_data[key] = value\n        return {}(**new_data)'
