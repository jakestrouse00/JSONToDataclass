from dataclasses import dataclass, field
from typing import *

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
