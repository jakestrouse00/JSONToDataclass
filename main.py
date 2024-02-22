from models import *
import json
import argparse
import sys


def load_file(file: str) -> dict:
    with open(file, "r") as f:
        return json.load(f)


def write_file(file_name: str, data: FileCodeBlock) -> str:
    with open(f"outputs/{file_name}.py", "w") as f:
        f.write(data.__str__())
    return f"outputs/{file_name}.py"


def d1_process_json(data: dict):
    # d1 = a dict with no dict inside of it
    fields: List[ArgumentCodeBlock] = []
    for index, (key, value) in enumerate(data.items()):
        x = ArgumentCodeBlock(key, type_hint=type(value), field=None)
        fields.append(x)
    return fields


def create_object(name: str, arguments: List[ArgumentCodeBlock], static_method_type: StaticMethods) -> ClassCodeBlock:
    return ClassCodeBlock(f"{name}", arguments, static_method_type)


def d2_process_json(data: dict, static_method_type: StaticMethods, field: FieldInput | None = None) -> Tuple[
    List[ArgumentCodeBlock], List[ClassCodeBlock]]:
    # d2 = a dict with 1 dict inside of it
    fields: List[ArgumentCodeBlock] = []
    child_classes = []
    for index, (key, value) in enumerate(data.items()):
        if isinstance(value, dict):
            child_object_data = d2_process_json(value, static_method_type, field=field)
            child_object = create_object(key, child_object_data[0], static_method_type)
            for obj in child_object_data[1]:
                child_classes.append(obj)
            child_classes.append(child_object)

            arg = ArgumentCodeBlock(key, child_object.name, field=field)
        else:
            arg = ArgumentCodeBlock(key, type_hint=type(value), field=field)
        fields.append(arg)

    return fields, child_classes


def json_to_code(object_name: str, data: dict, field: FieldInput | None = None,
                 static_method_type: StaticMethods = StaticMethods.json_out) -> FileCodeBlock:
    args = d2_process_json(data, static_method_type, field=field)
    test_obj = create_object(object_name, args[0], static_method_type)
    code = FileCodeBlock(main_object=test_obj, child_objects=args[1],
                         imports=[FromImport("__future__", ["annotations"]),
                                  FromImport("pydantic.dataclasses", ["dataclass", "Field"])])
    return code





parser = argparse.ArgumentParser(description='Script to make pydantic dataclasses from json data')
parser.add_argument('object_name', type=str, help='Name of the object')
parser.add_argument('--file', type=str, default=None, help='JSON file')
parser.add_argument('--json', type=str, default=None, help='JSON data')
parser.add_argument('--output_file', type=str, default="testing", help='File name for outputted code')
parser.add_argument('--repr', action='store_false', default=True, help='Display arguments in repr')
parser.add_argument('--static_method', default="json_out", type=str,
                    help="Switches output of static methods from json to object", choices=["json_out", "object_out"])

if len(sys.argv) > 1:
    args = parser.parse_args()
else:
    config_dict = load_config()
    args = ConfigArgs(**config_dict)

if args.file is None and args.json is None:
    raise "'--file' or '--json' must not be None"

if args.json is not None:
    json_data = json.loads(args.json)
elif args.file is not None:
    json_data = load_file(args.file)
else:
    raise "'--file' or '--json' must not be None"

x = FieldInput(repr=args.repr)
code = json_to_code(args.object_name, json_data, x, static_method_type=StaticMethods[args.static_method])
# print(code)
output_file = write_file(args.output_file, code)
print(f"Objects created: {len(code.child_objects) + 1}\nSaved to: {output_file}")
