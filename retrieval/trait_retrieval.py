from attention.dynamic_attention import (
    DynamicAttention
)

class TraitRetrieval:

    def __init__(self):

        self.attention = (
            DynamicAttention()
        )

    def score(

    self,

    semantic_score,

    gene

):

        traits = gene.get(
            "traits",
            {}
        )

        attention = traits.get(
            "attention_weight",
            0.5
        )

        retrieval = traits.get(
            "retrieval_priority",
            0.5
        )

        chromosome = gene.get(
            "chromosome",
            "general"
        )

        attention_bonus = (

            self.attention
            .get_weight(
                chromosome
            )

        )

        trait_bonus = (

            attention

            +

            retrieval

            +

            attention_bonus

        ) / 3

        return (

            semantic_score

            *

            (

                1

                +

                trait_bonus

            )

        )