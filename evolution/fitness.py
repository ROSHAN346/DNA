from evolution.gene_traits import (
    GeneTraits
)


class FitnessEngine:

    def __init__(self):

        self.traits = (
            GeneTraits()
        )

    def calculate(

        self,

        gene

    ):

        gene = (

            self.traits
            .ensure_traits(
                gene
            )

        )

        strength = gene.get(
            "strength",
            0
        )

        usage_count = gene.get(
            "usage_count",
            0
        )

        generation = gene.get(
            "generation",
            0
        )

        trait_bonus = (

            self.traits
            .fitness_bonus(
                gene["traits"]
            )

        )

        fitness = (

            strength

            +

            (0.02 * usage_count)

            +

            (0.01 * generation)

            +

            (0.3 * trait_bonus)

        )

        return round(
            fitness,
            4
        )