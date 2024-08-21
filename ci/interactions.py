from pathlib import Path

import yaml
import json
import graphviz


COMPONENTS = Path(__file__).parents[1] / "specifications"
COMMON_APIS = ["TMF688", "TMF701"]
tmfc_list = [
    "TMFC001", "TMFC005", "TMFC028", "TMFC002", "TMFC006", "TMFC003", "TMFC027", "TMFC008", "TMFC029",
    "TMFC010", "TMFC023", "TMFC007", "TMFC036", "TMFC039", "TMFC014", "TMFC019", "TMFC020", "TMFC009",
    "TMFC012", "TMFC030", "TMFC024", "TMFC011", "TMFC037", "TMFC038", "TMFC031", "TMFC040", "TMFC035",
    "TMFC022", "TMFC017", "TMFC015", "TMFC032", "TMFC025", "TMFC016", "TMFC033", "TMFC018", "TMFC013",
    "TMFC026", "TMFC052", "TMFC041", "TMFC050", "TMFC061", "TMFC043", "TMFC057", "TMFC060", "TMFC062",
    "TMFC042", "TMFC047", "TMFC045", "TMFC056", "TMFC054", "TMFC046", "TMFC049", "TMFC051", "TMFC053",
    "TMFC055", "TMFC058", "TMFC059", "TMFC044", "TMFC048"
]


def load_components():
    for cid in tmfc_list:
        specs = list(COMPONENTS.glob(f"{cid}*/{cid}-*.yaml"))
        for spec in specs:
            with spec.open("r") as f:
                yield {
                    "component": yaml.load(f, Loader=yaml.SafeLoader),
                    "path": spec
                }

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

def generate_api_interactions_graph(nodes):
    interactions = {}
    for component in nodes:
        spec = component["component"]["spec"]
        apis = spec["coreFunction"]["exposedAPIs"]
        component_id = component["path"].parent.name[:7]
        for api in apis:
            api_id = api["id"]
            if api_id not in interactions:
                interactions[api_id] = []
            interactions[api_id].append(component_id)
    return interactions


def generate_component_graph(nodes, interactions):
    for component in nodes:
        component_id = component["path"].parent.name[:7]
        graph = ComponentGraph(f"{component_id}", "twopi")
        spec = component["component"]["spec"]
        apis = spec["coreFunction"]["dependentAPIs"]
        for api in apis:
            api_id = api["id"]
            if api_id in COMMON_APIS:
                continue
            api_interactions = interactions.get(api_id, [])
            for interaction in api_interactions:
                graph.add_edge(component_id, interaction)
        graph.add_node(component_id, component_id)
        graph.render("output")

def main():
    nodes = list(load_components())
    interactions = generate_api_interactions_graph(nodes)
    generate_component_graph(nodes, interactions)

if __name__ == "__main__":
    import sys
    sys.exit(main())