from utils.cosine_similarity import (
    cosine_similarity
)


class DNASearch:

    def search(

        self,

        query_embedding,

        genes,

        top_k=5

    ):

        ranked = []

        for gene in genes:

            score = cosine_similarity(

                query_embedding,

                gene["embedding"]

            )

            score *= gene["strength"]

            ranked.append(

                (
                    score,
                    gene
                )

            )

        ranked.sort(

            reverse=True,

            key=lambda x:x[0]
        )

        return ranked[:top_k]