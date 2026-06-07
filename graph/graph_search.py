from collections import deque


class GraphSearch:

    def search(
        self,
        graph,
        node
    ):

        return self.traverse(
            graph,
            node,
            depth=3
        )

    def traverse(

        self,

        graph,

        start,

        depth=3

    ):

        visited = set()

        result = []

        queue = deque(
            [(start, 0)]
        )

        while queue:

            node,current_depth = (
                queue.popleft()
            )

            if node in visited:
                continue

            visited.add(node)

            if current_depth >= depth:
                continue

            neighbors = (
                graph.get_neighbors(
                    node
                )
            )

            for relation in neighbors:

                target = (
                    relation["target"]
                )

                result.append(
                    {
                        "source": node,
                        "relation": relation["relation"],
                        "target": target,
                        "depth": current_depth + 1
                    }
                )

                queue.append(
                    (
                        target,
                        current_depth + 1
                    )
                )

        return result