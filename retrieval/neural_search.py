from utils.cosine_similarity import (
    cosine_similarity
)


class NeuralSearch:

    def search(

        self,

        query_embedding,

        memories,

        top_k=5

    ):

        ranked = []

        for memory in memories:

            score = cosine_similarity(

                query_embedding,

                memory["embedding"]

            )

            ranked.append(

                (
                    score,
                    memory
                )

            )

        ranked.sort(

            reverse=True,

            key=lambda x:x[0]

        )

        return ranked[:top_k]