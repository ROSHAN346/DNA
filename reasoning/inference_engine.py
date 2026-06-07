import json


class InferenceEngine:

    def __init__(

        self,

        path="storage/inference_memory.json"

    ):

        self.path = path

    def load(self):

        try:

            with open(
                self.path,
                "r"
            ) as f:

                return json.load(f)

        except:

            return []

    def save(

        self,

        data

    ):

        with open(
            self.path,
            "w"
        ) as f:

            json.dump(
                data,
                f,
                indent=4
            )

    def infer(

        self,

        graph_data

    ):

        results = []

        for source in graph_data:

            edges = graph_data[source]

            for edge in edges:

                target = edge["target"]

                if target in graph_data:

                    for second in graph_data[target]:

                        results.append(

                            {

                                "from": source,

                                "through": target,

                                "to": second["target"],

                                "rule": "transitive"

                            }

                        )

        self.save(
            results
        )

        return results