from dataclasses import dataclass, field
from typing import *





@dataclass
class RegularImport:
    package_name: str

    def __str__(self):
        return f"import {self.package_name}"


@dataclass
class FromImport:
    parent_package_name: str
    packages: str | List[str]

    def __post_init__(self):
        if isinstance(self.packages, str):
            self.packages = [self.packages]

    def __str__(self):
        return f"from {self.parent_package_name} import {', '.join(self.packages)}"