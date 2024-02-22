x = """@staticmethod
def convert_data(input_data: dict) -> dict:
    new_data = {}
    for index, (key, value) in enumerate(input_data.items()):
        if key in list(Person.__annotations__.keys()):
            new_data[key] = value
    return new_data
    """

print(repr(x))