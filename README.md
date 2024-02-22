# JSONToDataclass
## Overview
JSONToDataclass is a Python tool that automates the conversion of JSON objects into Pydantic data classes. This utility aims to streamline the process of working with JSON data by providing a structured, type-safe way to access the data in Python applications. By leveraging the power of Pydantic, it ensures that the data adheres to the defined schema, offering validation, serialization, and documentation benefits out of the box.

## Purpose
This tool is intended to be used when creating Python wrappers around unofficial apis. Creating objects that match up to the objects returned by an api is often tedious and time-consuming. This tool helps with that headache by doing most of the busy work for you. 

## Features
- Automatic Conversion: Easily convert any JSON object to a Pydantic data class.
- Type Safety: Ensures that the JSON data matches the expected structure and data types.
- Customizable: Offers options to customize the resulting data classes according to your needs.
- Supports Nested Dictionaries: Dynamically creates additional objects if there are nested dictionaries.
- Utilities for data conversion: Created Python objects automatically are given a static method to filter json data by the object's arguments. Static method can either return a dictionary containing the filtered arguments, or an initiated instance of the object.
## Requirements
To use JSONToDataclass, you need to have Python 3.6+ installed along with the following dependencies:

- pydantic
You can install all required dependencies by running:

```commandline
pip install -r requirements.txt
```
## Usage
To convert a JSON object to a Pydantic dataclass, you can use the script from the command line with arguments or configure `config.ini` and run `main.py` directly.

Command Line Arguments
- --file: Path to the JSON file you want to convert.
- --json: JSON string to be converted.
- --object_name: Name of the resulting data class.
- --output_file: (Optional) Name of the output python file (excluding the `.py`) to save the generated data class code. Defaults to `testing`
## Run Example

```commandline
python main.py --object_name MyDataClass --file mydata.json --output_file my_data_class
```

This command will read mydata.json, convert it into a Pydantic data class named MyDataClass, and save the generated code to my_data_class.py.

Alternatively you can input the json directly from the command line instead of from a file like so:

```commandline
python main.py --object_name MyDataClass --json '{"key": "value"}' --output_file my_data_class
```

*Note: single quotes are required around the json*


## How To Use Staticmethod Utilities
The idea behind the static methods is to take possibly unclean json data *(could be from an api, a user, etc...)* that may include additional arguments that are not accepted by the datclass. The `convert_data()` function will return either *(depending on configuration)* a dictionary that includes only valid arguments or an initialized instance of the object
### Example Results

#### Convert to Dictionary
Below is an example of an object that is generated with the static method only filtering json data.
```python
@dataclass
class Person:
    name: str 
    age: int 
    gender: str 
    hired: bool 
    
    @staticmethod
    def convert_data(input_data: dict) -> dict:
        new_data = {}
        for index, (key, value) in enumerate(input_data.items()):
            if key in list(Person.__annotations__.keys()):
                new_data[key] = value
        return new_data
```

When you want to initialize an instance of Person with some json data this is how you would do it:

```python
unfiltered_data = {"name":  "bob", "age":  15, "gender":  "male", "hired":  False, "hair_color": "brown"}  # this json data contains the additional argument hair_color which will not be accepted by the dataclass and result in an exception
filtered_data = Person.convert_data(unfiltered_data)
# then just create a new instance of Person by unpacking the filtered json data
person_object = Person(**filtered_data)
```


#### Convert to Object
Below is an example of an object that is generated with a static method that filters and then returns an initialized instance of the object.
```python
@dataclass
class Person:
    name: str 
    age: int 
    gender: str 
    hired: bool 
    
    @staticmethod
    def convert_data(input_data: dict) -> Person:
        new_data = {}
        for index, (key, value) in enumerate(input_data.items()):
            if key in list(Person.__annotations__.keys()):
                new_data[key] = value
        return Person(**new_data)
```

When you want to initialize an instance of Person with some json data this is how you would do it:

```python
unfiltered_data = {"name":  "bob", "age":  15, "gender":  "male", "hired":  False, "hair_color": "brown"}  # this json data contains the additional argument hair_color which will not be accepted by the dataclass and result in an exception
# unpacking the dictionary is now unnecessary because Person.convert_data() does that for us
person_object = Person.convert_data(unfiltered_data)
```