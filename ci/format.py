import yaml
from pathlib import Path

SPECS = Path(__file__).parents[1] / "specifications"

class Component:
    def __init__(self, spec_path):
        self.path = spec_path
        self.content = {}
        self.ordered = {}

    def load_yaml(self):
        with self.path.open("r") as f:
            self.content = yaml.safe_load(f)
    
    def order_fields(self):
        self.order = {
            "apiVersion": self.content["apiVersion"],
            "kind": self.content["kind"],
            "metadata": self.content["metadata"],
            "spec": {
                "name": self.content["spec"]["name"],
                "id": self.content["spec"]["id"],
                "functionalBlock": self.content["spec"]["functionalBlock"],
                "description": self.content["spec"]["description"],
                "publicationDate": self.content["spec"]["publicationDate"],
                "status": self.content["spec"]["status"],
                "version": self.content["spec"]["version"],
                "coreFunction": self.content["spec"]["coreFunction"],
                "owners": self.content["spec"]["owners"],
            }

        }

    def write_component(self):
        with self.path.open("w") as f:
            yaml.safe_dump(self.order, f)

def load_components():
    for spec in SPECS.glob("TMF*/TMF*.yaml"):
        yield Component(spec)

def main():
    for component in load_components():
        component.load_yaml()
        component.order_fields()
    return 0

if __name__ == "__main__":
    import sys
    sys.exit(main())