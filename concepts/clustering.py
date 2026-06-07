from sklearn.cluster import KMeans


class ClusteringEngine:

    def cluster(

        self,

        embeddings,

        n_clusters=3

    ):

        if len(embeddings) < n_clusters:

            return None

        model = KMeans(

            n_clusters=n_clusters,

            random_state=42,

            n_init=10

        )

        labels = model.fit_predict(
            embeddings
        )

        return labels