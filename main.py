from models import *
import json



def load_file(file: str) -> dict:
    with open(file, "r") as f:
        return json.load(f)


def write_file(file_name: str, data: FileCodeBlock):
    with open(f"outputs/{file_name}.py", "w") as f:
        f.write(data.__str__())


def d1_process_json(data: dict):
    # d1 = a dict with no dict inside of it
    fields: List[ArgumentCodeBlock] = []
    for index, (key, value) in enumerate(data.items()):
        x = ArgumentCodeBlock(key, type_hint=type(value), field=None)
        fields.append(x)
    return fields


def create_object(name: str, arguments: List[ArgumentCodeBlock]) -> ClassCodeBlock:
    return ClassCodeBlock(f"{name}", arguments)


def d2_process_json(data: dict, field: FieldInput | None = None) -> Tuple[List[ArgumentCodeBlock], List[ClassCodeBlock]]:
    # d2 = a dict with 1 dict inside of it
    fields: List[ArgumentCodeBlock] = []
    child_classes = []
    for index, (key, value) in enumerate(data.items()):
        if isinstance(value, dict):
            child_object_data = d2_process_json(value, field=field)
            child_object = create_object(key, child_object_data[0])
            for obj in child_object_data[1]:
                child_classes.append(obj)
            child_classes.append(child_object)

            arg = ArgumentCodeBlock(key, child_object.name, field=field)
        else:
            arg = ArgumentCodeBlock(key, type_hint=type(value), field=field)
        fields.append(arg)

    return fields, child_classes

#
def json_to_code(data: dict, field: FieldInput | None = None) -> FileCodeBlock:
    args = d2_process_json(data, field=field)
    test_obj = ClassCodeBlock("Person", args[0])
    code = FileCodeBlock(main_object=test_obj, child_objects=args[1], imports=[FromImport("pydantic.dataclasses", ["dataclass", "Field"])])
    return code


file = load_file("test2.json")
code = json_to_code(file, FieldInput(repr=False))
write_file("testing", code)
