from .extra import FieldInput, EmptyValue
from .input_blocks import *
from dataclasses import dataclass, field
from typing import *


class ArgumentCodeBlock:
    def __init__(self, name: str, type_hint: type, field: FieldInput | None):
        self.name = name
        self.type_hint = type_hint
        self.field = field

    def compose_field(self) -> str:
        temp_str = ""
        if not self.field.repr:
            temp_str += f"repr={self.field.repr},"
        if not self.field.init:
            temp_str += f"init={self.field.init},"
        if self.field.hash:
            temp_str += f"hash={self.field.hash},"
        if self.field.compare:
            temp_str += f"compare={self.field.compare},"
        if not isinstance(self.field.default, EmptyValue):
            temp_str += f"default={self.field.default},"
        if temp_str.endswith(","):
            temp_str = temp_str[:-1]
        if temp_str.startswith(","):
            temp_str = temp_str[1:]
        return f"Field({temp_str})"
        # return f"Field(repr={self.field.repr}, init={self.field.init}, hash={self.field.hash}, compare={self.field.compare}{default_str})"

    def __str__(self, indent=""):

        if isinstance(self.field, FieldInput):
            field_str = f"= {self.compose_field()}"
        else:
            field_str = ""
        if isinstance(self.type_hint, type):
            type_hint = self.type_hint.__name__
        else:
            type_hint = self.type_hint
        result = indent + self.name + f": {type_hint} {field_str}\n"
        return result


class ClassCodeBlock:
    def __init__(self, name: str, blocks: List[ArgumentCodeBlock]):
        self.name = name.capitalize()
        self.head = "@dataclass\nclass " + self.name
        self.blocks = blocks

    def __str__(self, indent=""):
        result = indent + self.head + ":\n"
        indent += "    "
        for block in self.blocks:
            if isinstance(block, ArgumentCodeBlock):
                result += block.__str__(indent)
            else:
                result += indent + block.__str__(indent) + "\n"
        return result


@dataclass
class FileCodeBlock:
    imports: List[RegularImport | FromImport]
    main_object: ClassCodeBlock
    child_objects: List[ClassCodeBlock]

    def __str__(self, indent=""):
        result = ""
        for import_statement in self.imports:
            result += import_statement.__str__() + "\n"
        for child in self.child_objects:
            result += child.__str__(indent) + "\n"

        result += self.main_object.__str__(indent) + "\n"
        return result
