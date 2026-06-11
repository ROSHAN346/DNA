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

        for score, memory in neural_results:
            merged.append(
                (
                    score,
                    memory["text"],
                    "NEURAL",
                    {
                        "importance": round(float(memory.get("importance", 0.5)), 3),
                        "access_count": memory.get("access_count", 0)
                    }
                )
            )

        for score, gene in dna_results:
            merged.append(
                (
                    score,
                    gene["knowledge"],
                    "DNA",
                    {
                        "chromosome": gene["chromosome"],
                        "expression": round(float(gene.get("expression", 0.0)), 3),
                        "base_expression": round(float(gene.get("base_expression", 0.1)), 3),
                        "promoters": gene.get("promoters", {}),
                        "repressors": gene.get("repressors", {}),
                        "usage_count": gene.get("usage_count", 0)
                    }
                )
            )

        merged.sort(
            reverse=True,
            key=lambda x: x[0]
        )

        return merged[:10]