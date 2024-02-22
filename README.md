# JSONToDataclass
## Overview
JSONToDataclass is a Python tool that automates the conversion of JSON objects into Pydantic data classes. This utility aims to streamline the process of working with JSON data by providing a structured, type-safe way to access the data in Python applications. By leveraging the power of Pydantic, it ensures that the data adheres to the defined schema, offering validation, serialization, and documentation benefits out of the box.

## Features
- Automatic Conversion: Easily convert any JSON object to a Pydantic data class.
- Type Safety: Ensures that the JSON data matches the expected structure and data types.
- Customizable: Offers options to customize the resulting data classes according to your needs.
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
--file: Path to the JSON file you want to convert.
--json: JSON string to be converted.
--object_name: Name of the resulting data class.
--output_file: (Optional) Name of the output python file (excluding the `.py`) to save the generated data class code. Defaults to `testing`
## Example

```commandline
python main.py --object_name MyDataClass --file mydata.json --output_file my_data_class
```

This command will read mydata.json, convert it into a Pydantic data class named MyDataClass, and save the generated code to my_data_class.py.

Alternatively you can input the json directly from the command line instead of from a file like so:

```commandline
python main.py --object_name MyDataClass --json '{"key": "value"}' --output_file my_data_class
```

*Note: single quotes are required around the json*