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

def validate_apis(component):
    functions = ["coreFunction", "securityFunction", "managementFunction"]
    pass


def validate_component(schema, component, name):
    errors = 0
    try:
        validate(instance=component, schema=schema)
        #validate_apis(component)
    except Exception as e:
        errors = 1
        print(f"::group::{name}")
        print(f"::error::{e}")
        print("::endgroup::")
    return errors


def main():
    component_schema = load_json_schema()
    yaml.SafeLoader.add_constructor('tag:yaml.org,2002:timestamp', str_constructor)
    return_code = 0
    for file_path, component in load_components():
        return_code |= validate_component(component_schema, component, file_path.parent.name)

    if return_code == 0:
        print("All components are valid")
    return return_code


if __name__ == "__main__":
    import sys
    sys.exit(main())