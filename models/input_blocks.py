from dataclasses import dataclass, field
from typing import *





@dataclass
class RegularImport:
    package_name: str

    def __str__(self):
        return f"import {self.package_name}\n"


@dataclass
class FromImport:
    parent_package_name: str
    packages: List[str]

    def __str__(self):
        return f"from {self.parent_package_name} import {', '.join(self.packages)}\n"