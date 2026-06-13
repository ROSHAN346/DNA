import json

from concepts.clustering import (
    ClusteringEngine
)

from concepts.concept_naming import (
    ConceptNaming
)


class ConceptDiscovery:

    def __init__(self, path="storage/discovered_concepts.json"):
        self.path = path
        self.clustering = ClusteringEngine()
        self.naming = ConceptNaming()

    def load(self, path=None):
        if path is None:
            path = self.path
        try:
            with open(path, "r") as f:
                return json.load(f)
        except:
            return []

    def save(self, concepts, path=None):
        if path is None:
            path = self.path
        with open(path, "w") as f:
            json.dump(concepts, f, indent=4)

    def discover(

        self,

        genes,

        n_clusters=3

    ):

        if len(genes) < n_clusters:

            return []

        embeddings = [

            gene["embedding"]

            for gene in genes

        ]

        labels = (

            self.clustering
            .cluster(

                embeddings,

                n_clusters

            )

        )

        if labels is None:

            return []

        clusters = {}

        for gene, label in zip(
            genes,
            labels
        ):

            label = int(label)

            if label not in clusters:

                clusters[label] = []

            clusters[label].append(
                gene
            )

        result = []

        for label, members in clusters.items():

            texts = [

                member["knowledge"]

                for member in members

            ]

            chromosomes = [

                member.get(

                    "chromosome",

                    "general"

                )

                for member in members

            ]

            concept_name = (

                self.naming
                .generate(
                    texts,chromosomes
                )

            )

            result.append(

                {

                    "cluster":
                        label,

                    "concept":
                        concept_name,

                    "size":
                        len(members),

                    "members":
                        texts,

                    "chromosomes":
                        chromosomes

                }

            )

        self.save(
            result
        )

        return result