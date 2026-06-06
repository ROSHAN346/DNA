from retrieval.neural_search import (
    NeuralSearch
)

from retrieval.dna_search import (
    DNASearch
)


class HybridSearch:

    def __init__(self):

        self.neural = (
            NeuralSearch()
        )

        self.dna = (
            DNASearch()
        )

    def search(

        self,

        query_embedding,

        neural_memories,

        dna_genes

    ):

        neural_results = (

            self.neural.search(

                query_embedding,

                neural_memories

            )

        )

        dna_results = (

            self.dna.search(

                query_embedding,

                dna_genes

            )

        )

        merged = []

        for score,memory in neural_results:

            merged.append(

                (
                    score,

                    memory["text"],

                    "NEURAL"

                )

            )

        for score,gene in dna_results:

            merged.append(

                (
                    score,

                    gene["knowledge"],

                    "DNA"

                )

            )

        merged.sort(

            reverse=True,

            key=lambda x:x[0]
        )

        return merged[:10]