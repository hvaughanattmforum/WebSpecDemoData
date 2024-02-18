from pathlib import Path
import pandas as pd
import yaml
import json


COMPONENTS = Path(__file__).parents[1] / "specifications"


def load_components():
    for spec in COMPONENTS.glob("TMFC*/*.yaml"):
        with spec.open("r") as f:
            yield spec, yaml.load(f, Loader=yaml.SafeLoader)




def generate_report_data(components):
    data = []
    edges = ["dependentAPIs", "exposedAPIs"]
    functions = ["coreFunction"]
    

    for file_path, component in components:
        for block in functions:
            for  edge in edges:
                for api in component["spec"].get(block, {}).get(edge, []):
                    data.append ({
                        "component": file_path.stem,
                        "functionBlock": "coreFunction",
                        "function": edge,
                        "api": api.get("id", "NO ID AVAILABLE"),
                        "version": api.get("version", "NOT AVAILABLE"),
                        "required": api.get("required", "NOT AVAILABLE"),
                    })
               
    return data


def create_excel_report(data):
    df = pd.DataFrame(data)
    df.to_excel("component_api_report.xlsx", index=False)

def main(args):
    components = load_components()
    data = generate_report_data(components)
    create_excel_report(data)
    #print(json.dumps(data, indent=2))
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main(sys.argv))