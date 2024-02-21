from models import *
import json


@dataclass
class Person:
    name: str
    age: int
    gender: str
    hired: bool


d = FieldInput(default="Bob")
name_arg = ArgumentCodeBlock("name", str, d)
age_arg = ArgumentCodeBlock("age", int, None)