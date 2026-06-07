from sklearn.cluster import KMeans
import json
from concepts.clustering import (
    ClusteringEngine
)


class ConceptDiscovery:

    def __init__(self):

        self.clustering = (
            ClusteringEngine()
        )

    def save(

    self,

    concepts,

    path="storage/discovered_concepts.json"

):

        with open(
            path,
            "w"
        ) as f:

            json.dump(
                concepts,
                f,
                indent=4
            )

    def discover(

        self,

        genes,

        n_clusters=3

    ):

        if len(genes) < n_clusters:

            return []

        embeddings = []

        for gene in genes:

            embeddings.append(

                gene["embedding"]

            )

        labels = (

    self.clustering
    .cluster(

        embeddings,

        n_clusters

    )

)

        clusters = {}

        for gene,label in zip(
            genes,
            labels
        ):

            if label not in clusters:

                clusters[label] = []

            clusters[label].append(

                gene["knowledge"]

            )

        result = []

        for label,members in clusters.items():

            result.append(

                {

                    "cluster": int(label),

                    "size": len(
                        members
                    ),

                    "members": members

                }

            )

        return result