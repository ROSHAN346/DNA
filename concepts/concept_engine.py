import json


class ConceptEngine:

    def __init__(

        self,

        path="storage/concept_memory.json"

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

    def build(

        self,

        genes

    ):

        concepts = {}

        for gene in genes:

            chromosome = gene.get(

                "chromosome",

                "general"

            )

            if chromosome not in concepts:

                concepts[chromosome] = []

            concepts[chromosome].append(

                gene["knowledge"]

            )

        result = []

        for name,members in concepts.items():

            result.append(

                {

                    "concept": name,

                    "members": members,

                    "size": len(
                        members
                    )

                }

            )

        self.save(
            result
        )

        return result