import yaml

from pathlib import Path
import json
import yaml

COMPONENTS = Path(__file__).parents[1] / "specifications"


def load_components():
    for spec in COMPONENTS.glob("TMFC*/*.yaml"):
        with spec.open("r") as f:
            yield spec, yaml.load(f, Loader=yaml.SafeLoader)

def remove_arrays(component):
    functions = ["coreFunction"]
    edges = ["dependentAPIs", "exposedAPIs"]
    for block in functions:
        for edge in edges:
            for api in component["spec"][block][edge]:
                api.pop("name", "")
                api.pop("specification", "")
                api.pop("apiType", "")
                api.pop("implementation", "")
                api.pop("port", "")
                api.pop("path", "")
                api.pop("developerUI", "")
                


def save_component(file_path, component):
    with file_path.open("w+") as f:
        yaml.dump(component, f, default_flow_style=False)

def main():
    for file_path, component in load_components():
        remove_arrays(component)
        save_component(file_path, component)
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())