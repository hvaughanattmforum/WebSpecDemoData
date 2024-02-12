from pathlib import Path
from jsonschema import validate

import json
import yaml
import jsonschema

COMPONENTS = Path(__file__).parents[1] / "specifications"
CI = Path(__file__).parents[1] / "ci"

def str_constructor(loader, node):
    return loader.construct_scalar(node)

def load_components():
    for spec in COMPONENTS.glob("TMFC*/*.yaml"):
        with spec.open("r") as f:
            yield spec, yaml.load(f, Loader=yaml.SafeLoader)


def load_json_schema():
    with CI.joinpath("component.schema.json").open("r") as f:
        return json.load(f)


def main():
    component_schema = load_json_schema()
    yaml.SafeLoader.add_constructor('tag:yaml.org,2002:timestamp', str_constructor)
    for file_path, component in load_components():
        print(file_path)
        validate(instance=component, schema=component_schema)


    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())