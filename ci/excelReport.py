from pathlib import Path
import pandas as pd
import yaml
import json


COMPONENTS = Path(__file__).parents[1] / "specifications"


def load_components():
    for spec in COMPONENTS.glob("TMFC*/*.yaml"):
        with spec.open("r") as f:
            yield spec, yaml.load(f, Loader=yaml.SafeLoader)




def generate_api_report_data(components):
    data = []
    edges = ["dependentAPIs", "exposedAPIs"]
    functions = ["coreFunction"]
    

    for file_path, component in components:
        for block in functions:
            for  edge in edges:
                for api in component["spec"].get(block, {}).get(edge, []):
                    for resource in api.get("resources",{}):
                        for res_name, methods in resource.items():
                            if isinstance(methods, list):
                                for method in methods:
                                    data.append ({
                                        "component": file_path.stem,
                                        "functionBlock": "coreFunction",
                                        "function": edge,
                                        "api": api.get("id", "NO ID AVAILABLE"),
                                        "version": api.get("version", "NOT AVAILABLE"),
                                        "required": api.get("required", "NOT AVAILABLE"),
                                        "resource": res_name,
                                        "method": method,
                                    })
               
    return data

def generate_event_report_data(components):
    data = []
    edges = ["subscribedEvents", "publishedEvents"]
    functions = ["coreFunction"]
    

    for file_path, component in components:
        for block in functions:
            for  edge in edges:
                for event in component["spec"].get(block, {}).get(edge, []):
                    for resource in event.get("resources", []):
                        data.append ({
                            "component": file_path.stem,
                            "functionBlock": "coreFunction",
                            "function": edge,
                            "api id": event.get("id", "ID NOT AVAILABLE"),
                            "api name": event.get("name", "NAME NOT AVAILABLE"),
                            "EventId": resource,
                        })
               
    return data

def create_component_report_data(components):
    data = []
    for file_path, component in components:
        maintainers = component["spec"].get("maintainers", [])
        maintainers = ",".join([m["email"] for m in maintainers])

        owners = component["spec"].get("owners", [])
        owners = ",".join([o["email"] for o in owners])
        data.append({
            "id": component["spec"].get("id", "NO ID AVAILABLE"),
            "name": component["spec"].get("name", "NO NAME AVAILABLE"),
            "description": component["spec"].get("description", "NO DESCRIPTION AVAILABLE"),
            "publicationDate": str(component["spec"].get("publicationDate", "NO DATE AVAILABLE")),
            "status": component["spec"].get("status", "NO STATUS AVAILABLE"),
            "version": component["spec"].get("version", "NO VERSION AVAILABLE"),
            "maintainers": maintainers,
            "owners": owners,
        })
    return data

def create_excel_report(data, name):
    df = pd.DataFrame(data)
    excel_writer = pd.ExcelWriter(f"{name}.xlsx", engine='xlsxwriter')
    df.to_excel(excel_writer, index=False)
    excel_writer._save()

def main(args):
    components = list(load_components())
    api_data = generate_api_report_data(components)
    event_data = generate_event_report_data(components)
    component_data = create_component_report_data(components)
    create_excel_report(event_data, "Component-event-report")
    create_excel_report(api_data, "Component-api-report")
    create_excel_report(component_data, "Component-report")
    
    #print(json.dumps(data, indent=2))
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main(sys.argv))