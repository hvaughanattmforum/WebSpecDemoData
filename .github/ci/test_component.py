from pathlib import Path

import json
import yaml
from jsonschema import validate
from jsonschema.exceptions import ValidationError


SPECIFICATIONS = Path(__file__).parents[2] / "specifications"
TEMPLATES = SPECIFICATIONS / "Template"


def load_component_schema():
    with (TEMPLATES / "component.schema.json").open("r") as f:
        return json.load(f)

    

def load_component(component):
    class CustomLoader(yaml.SafeLoader):
        pass

    # Remove the default timestamp constructor
    CustomLoader.add_constructor(u'tag:yaml.org,2002:timestamp', CustomLoader.construct_scalar)

    with open(component, 'r') as f:
        return yaml.load(f, Loader=CustomLoader)

def very_component_strucure(component, schema):
    try:
        validate(instance=component, schema=schema)
        return True
    except ValidationError as e:
        print(e)
        return False


def main(args):
    component = SPECIFICATIONS / args[1] / f"{args[1]}.yaml"
    definition = load_component(component)
    schema = load_component_schema()
    if very_component_strucure(definition, schema):
        print(f"{args[1]} is valid")
        return 0
    return 1

if __name__ == "__main__":
    import sys
    sys.exit(main(sys.argv))