from utils.cosine_similarity import (
    cosine_similarity
)

from retrieval.trait_retrieval import (
    TraitRetrieval
)

from evolution.gene_traits import (
    GeneTraits
)


class DNASearch:

    def __init__(self):

        self.traits = (
            TraitRetrieval()
        )

        self.gene_traits = (
            GeneTraits()
        )

    def search(

        self,

        query_embedding,

        genes,

        top_k=5

    ):

        ranked = []

        for gene in genes:

            gene = (

                self.gene_traits
                .ensure_traits(
                    gene
                )

            )

            semantic_score = (

                cosine_similarity(

                    query_embedding,

                    gene["embedding"]

                )

            )

            final_score = (

                self.traits
                .score(

                    semantic_score,

                    gene

                )

            )

            ranked.append(

                (
                    final_score,

                    gene

                )

            )

        ranked.sort(

            reverse=True,

            key=lambda x: x[0]

        )

        return ranked[:top_k]