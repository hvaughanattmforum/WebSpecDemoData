import yaml
import json
from pathlib import Path

API_DOCS = Path(__file__).parents[3] / "APIS" / "api_table_docs" / "docs" / "ODA"
ODA_INDEX = Path(__file__).parents[1] / "apiIndex.json"
SPECS = Path(__file__).parents[1] / "specifications"

class Swagger:
    def __init__(self, path, api_ref) -> None:
        self.path = path
        self.api_ref = api_ref
        self.content = {}
        self.api_id = api_ref.split("_")[0]
        self.version =  api_ref.split("_")[1]
        
    def load_swagger(self):
        with self.path.open("r") as f:
            self.content = json.load(f)

    def extract_operation_ids(self):
        if "asyncapi" in self.content:
            return []
        operations = []
        for path, methods in self.content["paths"].items():
            for method, operation in methods.items():
                operation_id = operation.get("operationId")
                if operation_id:
                    operations.append(operation_id)

        return operations

class OperationIndex:
    def __init__(self) -> None:
        self.index = {}

    def add_swagger(self, swagger: Swagger):
        operations = swagger.extract_operation_ids()
        for operation in operations:
            if operation not in self.index:
                self.index[operation] = [swagger.api_ref]
            else:
                self.index[operation].append(swagger.api_ref)

class Component:
    def __init__(self, path) -> None:
        self.path = path
        self.content = {}
        self.versions = {
            4.1: "v4.1.0",
            4: "v4.0.0",
            5: "v5.0.0"
        }

    def load_component(self):
        with self.path.open("r") as f:
            self.content = yaml.load(f, Loader=yaml.FullLoader)

    def processEvents(self, operationIndex):
        coreFunction = self.content["spec"]["coreFunction"]
        events = [*coreFunction["publishedEvents"], *coreFunction["subscribedEvents"]]
        print(self.path)
        for event in events:
            target_apis = []
            #del event["port"]
            #del event["call-back"]
            #del event["implementation"]

            for resource in event["resources"]:
                opId_api = operationIndex[resource]
                target_apis.extend(opId_api)
            if len(target_apis) != 1:
                print(target_apis)
                print(self.path)



    def core_function_required_apis(self):
        apis = []
        coreFunction = self.content["spec"]["coreFunction"]
        for api in coreFunction["dependentAPIs"]:
            if api["required"]:
                apis.append(api)

        for api in coreFunction["exposedAPIs"]:
            if api["required"]:
                apis.append(api)

        for api in apis:
            api_id = api["id"]
            version = self.versions[api["version"]]
            yield f"{api_id}_{version}"


def load_swaggers():
    with ODA_INDEX.open("r") as f:
        index = json.load(f)
    for api_ref, docs in index.items():
        swagger_name = Path(docs["swagger"]).name
        swagger_path = API_DOCS / swagger_name
        swagger = Swagger(swagger_path, api_ref)
        yield swagger

def load_components():
    for component in SPECS.glob("TMFC*/TMFC*.yaml"):
        comp = Component(component)
        comp.load_component()
        yield comp
        

def build_index():
    operationIndex = OperationIndex()
    for swagger in load_swaggers():
        swagger.load_swagger()
        operationIndex.add_swagger(swagger)

def main():
    #build_index()
    with ODA_INDEX.open("r") as f:
        index = json.load(f)
    for component in load_components():
        operationIndex = OperationIndex()
        for api_ref in component.core_function_required_apis():
            if api_ref not in index:
                continue
            swagger_name = Path(index[api_ref]["swagger"]).name
            swagger_path = API_DOCS / swagger_name
            swagger = Swagger(swagger_path, api_ref)
            swagger.load_swagger()
            operationIndex.add_swagger(swagger)
            with Path("operation_index.json").open("w+") as f:
                json.dump(operationIndex.index, f,indent=4)
            print(component.path)
            return 0
        #component.processEvents(operationIndex.index)
        return

    return 0

if __name__ == "__main__":
    import sys
    sys.exit(main())