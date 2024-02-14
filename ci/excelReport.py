from pathlib import Path
import pandas as pd
import yaml
import json


COMPONENTS = Path(__file__).parents[1] / "specifications"


def load_components():
    for spec in COMPONENTS.glob("TMFC*/*.yaml"):
        with spec.open("r") as f:
            yield spec, yaml.load(f, Loader=yaml.SafeLoader)


def process_core_function(function):
    edges = ["dependentAPIs", "exposedAPIs"]

    for  edge in edges:
        for api in function.get(edge, []):
            yield {
                "functionBlock": "coreFunction",
                "function": edge,
                "api": api.get("id", "NO ID"),
                "version": api.get("version", "NO VERSION"),
                "required": api.get("required", "NO REQUIRED"),
            }


def generate_report_data(components):
    data = []
    functions = {
        "coreFunction": process_core_function,
    }

    for file_path, component in components:
        entry = {
            "component": file_path.stem
        }

        for block, reporter in functions.items():
            for row in reporter(component["spec"].get(block, {})):
                data.append({
                    **entry,
                    **row
                })
    return data


def main(args):
    components = load_components()
    data = generate_report_data(components)
    print(json.dumps(data, indent=2))
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main(sys.argv))