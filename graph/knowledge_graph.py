import json


class KnowledgeGraph:

    def __init__(self, path):

        self.path = path

    def load(self):

        try:

            with open(
                self.path,
                "r"
            ) as f:

                return json.load(f)

        except:

            return {}

    def save(self, graph):

        with open(
            self.path,
            "w"
        ) as f:

            json.dump(
                graph,
                f,
                indent=4
            )

    def add_relation(

        self,

        source,

        relation,

        target

    ):
        print(
    f"Adding relation: {source} {relation} {target}"
)

        graph = self.load()

        if source not in graph:

            graph[source] = []

        edge = {

            "relation": relation,

            "target": target

        }

        if edge not in graph[source]:

            graph[source].append(
                edge
            )

        self.save(graph)

    def get_neighbors(
        self,
        node
    ):

        graph = self.load()

        return graph.get(
            node,
            []
        )