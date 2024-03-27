from __future__ import annotations
from models import ArgumentCodeBlock, FieldInput, ClassCodeBlock, EmptyValue, FileCodeBlock, FromImport, \
    RegularImport, load_config, ConfigArgs
from pydantic import AnyUrl as AnyUrlPy
from datetime import datetime
from typing import NewType, TypeVar, Union, List, Optional, Generic
from types import NoneType
from functools import reduce
import random
import argparse
import json
import sys


class AllObjects(list):
    def __init__(self, *args):
        super().__init__(*args)

    def append(self, code_object: ClassCodeBlock) -> None:
        if code_object not in self:
            super().append(code_object)


objects = AllObjects()


def camel_to_snake(camel_str):
    """Converts CamelCase to snake_case."""
    snake_str = ''
    for i, char in enumerate(camel_str):
        if char.isupper() and i != 0:
            snake_str += '_'
        snake_str += char

    return snake_str.lower()


def convert_args(data: dict, custom_field: FieldInput):
    mapping = {"string": str, "boolean": bool, "integer": int, "array": list, "number": float, "float": float,
               "none": NoneType}
    chars = "abcdefghijklmnopqrstuvwxyz"
    arguments = []
    for index, (key, properties) in enumerate(data["properties"].items()):
        prop_type = properties["type"]
        if prop_type == "array":
            array_items: dict = properties["items"]
            array_types = []
            if array_items is not False:
                if "type" in array_items.keys():
                    if array_items["type"] == "array":
                        continue
                    elif array_items["type"] == "object":
                        # print(array_items)
                        # print(key)
                        # rand_object_name = "".join(random.choices(chars, k=5))
                        rand_object_name: str = key
                        # print(rand_object_name)
                        # print(rand_object_name.capitalize())
                        # print(rand_object_name.title())
                        array_types.append(rand_object_name.title())
                        objects.append(convert_schema(rand_object_name.title(), array_items, custom_field))
                    else:
                        array_types.append(mapping[array_items["type"]])
                elif "anyOf" in array_items.keys():
                    for i in array_items["anyOf"]:
                        if i["type"] == "array":
                            continue
                        elif i["type"] == "object":
                            rand_object_name = "".join(random.choices(chars, k=5)).capitalize()
                            p_type = TypeVar(rand_object_name, bound=object)

                            # p_type = NewType(rand_object_name, object)
                            array_types.append(p_type.__name__)
                            objects.append(convert_schema(rand_object_name.title(), i, custom_field))
                        else:
                            array_types.append(mapping[i["type"]])
                else:
                    raise "nothing found in array"
                # array_types.append(int)
                # print(array_types)
                # python_type = List[reduce(lambda x, y: x | y, array_types)]
                python_type = List[Union[tuple(array_types)]]
                # print(python_type)
            else:
                python_type = list
        elif prop_type == "object":
            python_type = key.title()
            objects.append(convert_schema(python_type, properties, custom_field))
        else:
            if isinstance(prop_type, str):
                python_type = mapping[prop_type]
            else:
                python_type = prop_type
        snake_key = camel_to_snake(key)
        alias = key if snake_key != key else EmptyValue()
        if snake_key.startswith("_"):
            indx = 0
            for char in snake_key:
                if char == "_":
                    pass
                else:
                    break
                indx += 1
            snake_key = snake_key[indx:]
            alias = key
        prop_format = properties["format"] if "format" in properties.keys() else None
        if prop_format == "date-time":
            python_type = datetime
        elif prop_format == "uri":
            AnyUrl = NewType("AnyUrl", AnyUrlPy)
            python_type = Optional[AnyUrl.__name__]

        if isinstance(python_type, str):
            # python_type of str is an object
            field = FieldInput(default=None, validation_alias=alias, union_mode="left_to_right", repr=custom_field.repr)
        else:
            field = FieldInput(default=None, validation_alias=alias, repr=custom_field.repr)
        x = ArgumentCodeBlock(snake_key, python_type, field)
        # print(prop_format, key, type(python_type), x.__str__()) if prop_format is not None else ...
        # print(x.type_hint)
        arguments.append(x)
    return arguments


def convert_schema(object_name: str, data: dict, custom_field: FieldInput) -> ClassCodeBlock:
    # print(object_name)
    arguments = convert_args(data, custom_field)
    main_code = ClassCodeBlock(object_name, arguments)
    # print(main_code)
    return main_code


def write_file(file_name: str, data: FileCodeBlock) -> str:
    with open(f"outputs/{file_name}.py", "w") as f:
        f.write(data.__str__())
    return f"{file_name}.py"


def load_file(file: str) -> dict:
    with open(file, "r") as f:
        return json.load(f)


parser = argparse.ArgumentParser(description='Script to make pydantic dataclasses from json data')
parser.add_argument('object_name', type=str, help='Name of the object')
parser.add_argument('--file', type=str, default=None, help='JSON file')
parser.add_argument('--json', type=str, default=None, help='JSON data')
parser.add_argument('--output_file', type=str, default="testing", help='File name for outputted code')
parser.add_argument('--repr', action='store_false', default=True, help='Display arguments in repr')

if len(sys.argv) > 1:
    args = parser.parse_args()
else:
    config_dict = load_config()
    args = ConfigArgs(**config_dict)

if args.json is not None:
    json_data = json.loads(args.json)
elif args.file is not None:
    json_data = load_file(args.file)
else:
    raise "'--file' or '--json' must not be None"

imports = [FromImport("__future__", "annotations"),
           FromImport("pydantic", ["BaseModel", "Field", "model_validator", "AnyUrl"]),
           FromImport("typing", "*"), FromImport("types", "*"), FromImport("pprint", "pprint"),
           FromImport("datetime", "datetime"), RegularImport("typing")]
custom_field = FieldInput(repr=args.repr)
main_object = convert_schema(args.object_name, json_data, custom_field)
file = FileCodeBlock(imports=imports, main_object=main_object, child_objects=objects)
# print(file)

write_file(args.output_file, file)
