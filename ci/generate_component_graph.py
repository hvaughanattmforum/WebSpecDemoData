from pathlib import Path

import yaml
import json
import graphviz


COMPONENTS = Path(__file__).parents[1] / "specifications"
COMMON_APIS = ["TMF688", "TMF701"]

def glob_components():
    return COMPONENTS.glob("TMFC*/*.yaml")

def load_components():
    for spec in glob_components():
        with spec.open("r") as f:
            yield spec, yaml.load(f, Loader=yaml.SafeLoader)

def load_components_pairwaise():
    component_list = list(glob_components())
    for i in range(len(component_list)):
        for j in range(i+1, len(component_list)):
            with component_list[i].open("r") as f:
                component1 = yaml.load(f, Loader=yaml.SafeLoader)
            with component_list[j].open("r") as f:
                component2 = yaml.load(f, Loader=yaml.SafeLoader)
            yield [
                {
                    "spec": component1,
                    "path": component_list[i]
                }, 
                {
                    "spec": component2,
                    "path": component_list[j]
                }
            ]

class ComponentGraph:
    def __init__(self, name, engine="circo") -> None:
        self.graph = graphviz.Graph(
            name, 
            comment='Map of ODA Components',
        )
        self.graph.engine = engine
        self.graph.attr(overlap='false')
        #dot.edges(['AB', 'AL'])


    def add_node(self, name, label):
        self.graph.node(name, label)

    def add_edge(self, start, end, **kwargs):
        self.graph.edge(start, end, **kwargs)

    def render(self, path):
        self.graph.render(
            directory=path,
        )

def generate_exposedapis_graph():
    graph = ComponentGraph("Exposed APIs Graph", "twopi")
    for file_path, component in load_components():
        node_key = file_path.parent.name
        graph.add_node(node_key, node_key)
        apis = set([api["id"] for api in component["spec"]["coreFunction"]["exposedAPIs"]])
        unique_apis = apis.difference(COMMON_APIS)
        for api in unique_apis:
            graph.add_node(api, api)
            graph.add_edge(node_key, api)

    graph.render("docs")
    return 0


def has_common_apis(component1, component2):
    apis1 = set([api["id"] for api in component1["spec"]["coreFunction"]["exposedAPIs"]])
    apis2 = set([api["id"] for api in component2["spec"]["coreFunction"]["dependentAPIs"]])
    common_apis = apis1.intersection(apis2)
    common_apis = common_apis.difference(COMMON_APIS)
    return len(common_apis) > 0

def generate_component_graph():
    graph = ComponentGraph("Component Graph", "circo")
    for nodes in load_components_pairwaise():
        key_1 = nodes[0]["path"].parent.name
        key_2 = nodes[1]["path"].parent.name

        graph.add_node(key_1, key_1)
        graph.add_node(key_2, key_2)

        if has_common_apis(nodes[0]["spec"], nodes[1]["spec"]):
            graph.add_edge(
                key_1,
                key_2,
                #label="Common APIs"
            )
    graph.render("docs")


def main(args):
    generate_exposedapis_graph()
    generate_component_graph()
    return 0

if __name__ == "__main__":
    import sys
    sys.exit(main(sys.argv))