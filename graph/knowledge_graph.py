class KnowledgeGraph:

    def __init__(self):

        self.graph = {}

    def add_relation(
        self,
        source,
        target
    ):

        if source not in self.graph:
            self.graph[source] = []

        self.graph[source].append(target)

    def neighbors(
        self,
        node
    ):

        return self.graph.get(node,[])