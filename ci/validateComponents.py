from pathlib import Path
from jsonschema import validate

import json
import yaml

COMPONENTS = Path(__file__).parents[1] / "specifications"
CI = Path(__file__).parents[1] / "ci"

def str_constructor(loader, node):
    return loader.construct_scalar(node)

def validate_component_file_names_and_content():
    for spec in COMPONENTS.glob("TMFC*/*"):
        if not spec.name.startswith("TMFC") or not spec.name.endswith(".yaml"):
            if spec.suffix.lower() == ".pdf":
                continue  # skip PDF files
            if "BDD" in spec.parts or "ComponentRI" in spec.parts or "ComponentConformanceProfile" in spec.parts or "Diagrams" in spec.parts:
                continue
            print(f"::group::TMFC File Naming is invalid")
            print(f"::error::{spec.name}")
            print("::endgroup::")
            return 1

        try:
            with spec.open("r") as f:
                yaml.load(f, Loader=yaml.SafeLoader)
                print(f"{spec.name} content is valid")
        except yaml.parser.ParserError as e:
            print(f"::group::Error while parsing {spec.name}  .yaml; Content is invalid")
            print(f"::error::{e}")
            print("::endgroup::")
            return 1
        except Exception as e:
            print(f"::group::{spec.name} Content is invalid")
            print(f"::error::{e}")
            print("::endgroup::")
            return 1

    for spec in COMPONENTS.rglob("*"):
        if " " in spec.name:
            print(f"::group::TMFC File Naming is invalid")
            print(f"::error::{spec.relative_to(COMPONENTS)} contains a space")
            print("::endgroup::")
            return 1

    return 0

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
    return_code |= validate_component_file_names_and_content()
    for file_path, component in load_components():
        return_code |= validate_component(component_schema, component, file_path.parent.name)

    if return_code == 0:
        print("All components are valid")
    return return_code


if __name__ == "__main__":
    import sys
    sys.exit(main())
