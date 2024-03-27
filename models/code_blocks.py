from .extra import FieldInput, EmptyValue
from .input_blocks import *
from dataclasses import dataclass, field
from typing import *
from enum import Enum


class CodeLine:
    def __init__(self, line: str, indent: int = 2):
        self.indent = indent
        self.line = line

    def __str__(self):
        indent_string = "    "
        return f"\n{indent_string * self.indent} {self.line}"


class FunctionCodeBlock:
    def __init__(self, decorator: str, def_line: str, code_lines: List[CodeLine]):
        self.def_line = def_line
        self.decorator = decorator
        self.code_lines = code_lines

    def __str__(self):
        result = f"\n    {self.decorator}\n    {self.def_line}"
        for line in self.code_lines:
            result += line.__str__()
        return result


# class StaticMethods(Enum):
#     json_out =
#     object_out = '\n    @staticmethod\n    def convert_data(input_data: dict) -> {}:\n        new_data = {}\n        for index, (key, value) in enumerate(input_data.items()):\n            if key in list({}.__annotations__.keys()):\n                new_data[key] = value\n        return {}(**new_data)', '\n    def __post_init__(self):\n        for index, (key, value) in enumerate(self.__dict__.items()):\n            if isinstance(value, dict):\n                type_hints = get_type_hints(self.__class__)\n                tt: UnionType = type_hints[key]\n                object_arg = tt.__args__[1]\n                self.__setattr__(key, object_arg.convert_data(value))'

validator_function = FunctionCodeBlock(
    '@model_validator(mode="before")',
    "def convert_data(cls, input_data: dict) -> dict:",
    [
        CodeLine("new_data = {}"),
        CodeLine(
            "all_alias = [field_info.validation_alias for index, (field_key, field_info) in enumerate(cls.model_fields.items())]"
        ),
        CodeLine("for index, (key, value) in enumerate(input_data.items()):"),
        CodeLine(
            "if key in list(cls.__annotations__.keys()) or key in all_alias:", indent=3
        ),
        CodeLine("new_data[key] = value", indent=4),
        CodeLine("return new_data"),
    ],
)


class ArgumentCodeBlock:
    def __init__(self, name: str, type_hint: type | str, field: FieldInput | None):
        self.name = name.replace(" ", "")
        self.type_hint = type_hint
        self.field = field

    def __eq__(self, other):
        if isinstance(other, ArgumentCodeBlock):
            return other.name == self.name

    def compose_field(self) -> str | None:
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
        if not isinstance(self.field.validation_alias, EmptyValue):
            temp_str += f"validation_alias={self.field.validation_alias},"
        if not isinstance(self.field.union_mode, EmptyValue):
            temp_str += f"union_mode={self.field.union_mode},"
        if temp_str.endswith(","):
            temp_str = temp_str[:-1]
        if temp_str.startswith(","):
            temp_str = temp_str[1:]
        if len(temp_str) == 0:
            return None
        else:
            return f"Field({temp_str.replace(',', ', ')})"
        # return f"Field(repr={self.field.repr}, init={self.field.init}, hash={self.field.hash}, compare={self.field.compare}{default_str})"

    def __str__(self, indent=""):

        if isinstance(self.field, FieldInput):
            composed_field = self.compose_field()
            if composed_field is not None:
                field_str = f"= {self.compose_field()}"
            else:
                field_str = ""
        else:
            field_str = ""
        if isinstance(self.type_hint, type) or isinstance(self.type_hint, TypeVar):
            type_hint = self.type_hint.__name__

        else:
            type_hint = self.type_hint
        with_dict = " | dict" if isinstance(self.type_hint, str) else ""
        result = indent + self.name + f": {type_hint}{with_dict} {field_str}\n"
        return result


class ClassCodeBlock:
    def __init__(self, name: str, blocks: List[ArgumentCodeBlock]):
        self.name = name.title().replace(" ", "") if name[0].islower() else name.capitalize().replace(" ", "")
        self.head = "class " + self.name + "(BaseModel)"
        self.blocks = blocks
        self.static_method = validator_function
        # if static_method_type.name == "json_out":
        #     self.static_method = static_method_type.value.format({}, self.name)
        # elif static_method_type.name == "object_out":
        #     self.static_method = static_method_type.value.format(self.name, {}, self.name, self.name)
        # else:
        #     raise "invalid static_method_type"

    def __eq__(self, other):
        if isinstance(other, ClassCodeBlock):
            same_blocks = True
            for block in other.blocks:
                if block not in self.blocks:
                    same_blocks = False
                    break

            return (self.name == other.name) and (same_blocks == True)

    def __str__(self, indent=""):
        result = indent + self.head + ":\n"
        indent += "    "
        for block in self.blocks:
            if isinstance(block, ArgumentCodeBlock):
                result += block.__str__(indent)
            else:
                result += indent + block.__str__(indent) + "\n"
        result += indent + self.static_method.__str__() + "\n"
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
        result += "\n\n"
        for child in self.child_objects:
            result += child.__str__(indent) + "\n\n"
        # result += "\n"
        result += self.main_object.__str__(indent) + "\n"
        return result
