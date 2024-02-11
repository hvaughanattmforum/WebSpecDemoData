from pathlib import Path
import json
import yaml

INDEX = Path(__file__).parents[1] / "apiIndex.json"
COMPONENTS = Path(__file__).parents[1] / "specifications"

def load_index():
    with INDEX.open("r") as f:
        return json.load(f)

def load_components():
    for spec in COMPONENTS.glob("TMFC*/*.yaml"):
        with spec.open("r") as f:
            yield yaml.load(f, Loader=yaml.SafeLoader)

def validate_apis(index, component):
    functions = ["coreFunction", "securityFunction", "managementFunction"]
    print(type(component), component["spec"]["id"])

    for block in functions:
        function_edges = component["spec"].get(block, {})
        for edge, apis in function_edges.items():
            for api in apis:
                pass
            


def main():
    api_index = load_index()
    for component in load_components():
        validate_apis(api_index, component)   
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
