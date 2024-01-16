import json
from pathlib import Path

SCHEMA_PATH = Path(__file__).resolve().parent.parent/'schemas'


def load_schema(filepath):
    with (SCHEMA_PATH/filepath).open() as file:
        schema = json.load(file)
        return schema
