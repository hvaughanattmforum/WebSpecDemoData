import yaml
import json
from pathlib import Path

API_DOCS = Path(__file__).parents[3] / "APIS" / "api_table_docs" / "docs" / "ODA"
ODA_INDEX = Path(__file__).parents[1] / "apiIndex.json"


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
        print(f"Extracting {self.api_ref}")
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

def load_swaggers():
    with ODA_INDEX.open("r") as f:
        index = json.load(f)
    for api_ref, docs in index.items():
        swagger_name = Path(docs["swagger"]).name
        swagger_path = API_DOCS / swagger_name
        swagger = Swagger(swagger_path, api_ref)
        yield swagger


def build_index():
    operationIndex = OperationIndex()
    for swagger in load_swaggers():
        swagger.load_swagger()
        operationIndex.add_swagger(swagger)

def main():
    build_index()
    return 0

if __name__ == "__main__":
    import sys
    sys.exit(main())