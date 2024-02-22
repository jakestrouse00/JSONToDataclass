x = """@staticmethod
    def convert_data(input_data: dict) -> Store:
        new_data = {}
        for index, (key, value) in enumerate(input_data.items()):
            if key in list(Store.__annotations__.keys()):
                new_data[key] = value
        return Store(**new_data)
    """

print(repr(x))