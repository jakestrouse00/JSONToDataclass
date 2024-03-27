from __future__ import annotations
from models import ArgumentCodeBlock, FieldInput, ClassCodeBlock, EmptyValue, FileCodeBlock, FromImport, \
    RegularImport
from pydantic import AnyUrl as AnyUrlPy
from datetime import datetime
from typing import NewType, TypeVar

raw_data = {
    "type": "object",
    "properties": {
        "id": {
            "type": "string",
            "format": "uuid"
        },
        "authoredByUser": {
            "type": "boolean"
        },
        "alias": {
            "type": "string"
        },
        "group_id": {
            "type": "string",
            "format": "uuid"
        },
        "group": {
            "type": "object",
            "properties": {
                "id": {
                    "type": "string",
                    "format": "uuid"
                },
                "name": {
                    "type": "string"
                },
                "analytics_name": {
                    "type": "string"
                },
                "membership_type": {
                    "type": "string"
                },
                "color": {
                    "type": "string"
                },
                "should_show_leaderboard": {
                    "type": "boolean"
                },
                "group_join_type": {
                    "type": "string"
                },
                "group_visibility": {
                    "type": "string"
                },
                "icon_url": {
                    "type": "string",
                    "format": "uri"
                },
                "asset_library_visibility": {
                    "type": "string"
                },
                "roles": {
                    "type": "array",
                    "items": False
                },
                "instagram": {
                    "type": "string"
                },
                "description": {
                    "type": "string"
                },
                "member_count": {
                    "type": "integer"
                }
            },
            "required": [
                "id",
                "name",
                "analytics_name",
                "membership_type",
                "color",
                "should_show_leaderboard",
                "group_join_type",
                "group_visibility",
                "icon_url",
                "asset_library_visibility",
                "roles"
            ]
        },
        "text": {
            "type": "string"
        },
        "created_at": {
            "type": "string",
            "format": "date-time"
        },
        "vote_total": {
            "type": "integer"
        },
        "comment_count": {
            "type": "integer"
        },
        "vote_status": {
            "type": "string"
        },
        "assets": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": {
                        "type": "string",
                        "format": "uuid"
                    },
                    "type": {
                        "type": "string"
                    },
                    "width": {
                        "type": "integer"
                    },
                    "height": {
                        "type": "number"
                    },
                    "url": {
                        "type": "string",
                        "format": "uri"
                    },
                    "content_type": {
                        "type": "string"
                    }
                },
                "required": [
                    "id",
                    "type",
                    "width",
                    "height",
                    "url"
                ]
            }
        },
        "attachments": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": {
                        "type": "string",
                        "format": "uuid"
                    },
                    "type": {
                        "type": "string"
                    },
                    "created_at": {
                        "type": "string",
                        "format": "date-time"
                    },
                    "link_url": {
                        "type": "string",
                        "format": "uri"
                    },
                    "display_url": {
                        "type": "string"
                    },
                    "title": {
                        "type": "string"
                    }
                },
                "required": [
                    "id",
                    "type",
                    "created_at",
                    "link_url",
                    "display_url",
                    "title"
                ]
            }
        },
        "type": {
            "type": "string"
        },
        "dms_disabled": {
            "type": "boolean"
        },
        "comments_disabled": {
            "type": "boolean"
        },
        "tags": {
            "type": "array",
            "items": {
                "type": "string"
            }
        },
        "identity": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string"
                },
                "posted_with_username": {
                    "type": "boolean"
                },
                "conversation_icon": {
                    "type": "object",
                    "properties": {
                        "is_migrated": {
                            "type": "boolean"
                        },
                        "secondary_color": {
                            "type": "string"
                        },
                        "emoji": {
                            "type": "string"
                        },
                        "color": {
                            "type": "string"
                        }
                    },
                    "required": [
                        "is_migrated",
                        "secondary_color",
                        "emoji",
                        "color"
                    ]
                }
            },
            "required": [
                "name",
                "posted_with_username"
            ]
        },
        "pinned": {
            "type": "boolean"
        },
        "is_saved": {
            "type": "boolean"
        },
        "follow_status": {
            "type": "string"
        },
        "destination": {
            "type": "string"
        },
        "poll": {
            "type": "object",
            "properties": {
                "id": {
                    "type": "string",
                    "format": "uuid"
                },
                "post_id": {
                    "type": "string",
                    "format": "uuid"
                },
                "choices": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "count": {
                                "type": "integer"
                            },
                            "text": {
                                "type": "string"
                            },
                            "selected": {
                                "type": "boolean"
                            }
                        },
                        "required": [
                            "count",
                            "text",
                            "selected"
                        ]
                    }
                },
                "allows_view_results": {
                    "type": "boolean"
                },
                "view_results_count": {
                    "type": "integer"
                },
                "participated": {
                    "type": "boolean"
                }
            },
            "required": [
                "id",
                "post_id",
                "choices",
                "allows_view_results",
                "view_results_count",
                "participated"
            ]
        }
    },
    "required": [
        "id",
        "authored_by_user",
        "alias",
        "group_id",
        "group",
        "text",
        "created_at",
        "vote_total",
        "comment_count",
        "vote_status",
        "assets",
        "attachments",
        "type",
        "dms_disabled",
        "comments_disabled",
        "tags",
        "identity",
        "pinned",
        "is_saved",
        "follow_status",
        "destination"
    ]
}

objects = []


def camel_to_snake(camel_str):
    """Converts CamelCase to snake_case."""
    snake_str = ''
    for i, char in enumerate(camel_str):
        if char.isupper() and i != 0:
            snake_str += '_'
        snake_str += char

    return snake_str.lower()


def convert_args(data: dict):
    mapping = {"string": str, "boolean": bool, "integer": int, "array": list}
    arguments = []
    for index, (key, properties) in enumerate(data["properties"].items()):
        prop_type = properties["type"]
        if prop_type == "array":
            continue
        elif prop_type == "object":
            python_type = key.title()
            objects.append(convert_schema(python_type, properties))
        else:
            python_type = mapping[prop_type]
        snake_key = camel_to_snake(key)
        alias = key if snake_key != key else EmptyValue()
        prop_format = properties["format"] if "format" in properties.keys() else None
        if prop_format == "date-time":
            python_type = datetime
        elif prop_format == "uri":
            # python_type = NewType("AnyUrl", AnyUrl)
            AnyUrl = TypeVar("AnyUrl", bound=AnyUrlPy)
            python_type = AnyUrl

        if isinstance(python_type, str):
            # python_type of str is an object
            field = FieldInput(default=None, validation_alias=alias, union_mode="left_to_right")
        else:
            field = FieldInput(default=None, validation_alias=alias)
        x = ArgumentCodeBlock(snake_key, python_type, field)
        # print(prop_format, key, type(python_type), x.__str__()) if prop_format is not None else ...
        # print(x.type_hint)
        arguments.append(x)
    return arguments


def convert_schema(object_name: str, data: dict) -> ClassCodeBlock:
    # print(object_name)
    arguments = convert_args(data)
    main_code = ClassCodeBlock(object_name, arguments)
    # print(main_code)
    return main_code


def write_file(file_name: str, data: FileCodeBlock) -> str:
    with open(f"{file_name}.py", "w") as f:
        f.write(data.__str__())
    return f"{file_name}.py"


imports = [FromImport("__future__", "annotations"), FromImport("pydantic", ["BaseModel", "Field", "model_validator", "AnyUrl"]),
           FromImport("typing", "*"), FromImport("types", "*"), FromImport("pprint", "pprint"), FromImport("datetime", "datetime")]

main_object = convert_schema("Post", raw_data)
file = FileCodeBlock(imports=imports, main_object=main_object, child_objects=objects)
# print(file)

write_file("test_output", file)
