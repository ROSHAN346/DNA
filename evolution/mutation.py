import random


class MutationEngine:

    BASES = [

        "A",
        "T",
        "C",
        "G"

    ]

    def mutate(

        self,

        genome,

        mutation_rate=0.01

    ):

        genome = list(
            genome
        )

        for i in range(
            len(genome)
        ):

            if random.random() < mutation_rate:

                current = genome[i]

                choices = [

                    b

                    for b in self.BASES

                    if b != current

                ]

                genome[i] = (

                    random.choice(
                        choices
                    )

                )

        return "".join(
            genome
        )
    
    def create_child(

    self,

    gene

):

        child = gene.copy()

        child["genome"] = (

            self.mutate(
                gene["genome"]
            )

        )

        child["generation"] = (

            gene["generation"]
            + 1

        )

        child["strength"] *= 0.95

        child["usage_count"] = 0

        if "traits" not in gene:

            from evolution.gene_traits import (
                GeneTraits
            )

            gene["traits"] = (
                GeneTraits()
                .create_traits()
            )

        child["traits"] = (

            gene["traits"]
            .copy()

        )

        return child