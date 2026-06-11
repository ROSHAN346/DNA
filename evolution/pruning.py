from evolution.fitness import (
    FitnessEngine
)


class PruningEngine:

    def __init__(self):

        self.fitness = (
            FitnessEngine()
        )

    def prune(

        self,

        genes,

        experiences,

        threshold=0.70,

        max_population=100

    ):

        kept = []

        removed = []

        for gene in genes:

            fitness = (

                self.fitness
                .calculate_full(
                    gene,
                    genes,
                    experiences
                )

            )

            gene["fitness"] = (
                fitness
            )

            if fitness >= threshold:

                kept.append(
                    gene
                )

            else:

                removed.append(
                    gene
                )

        kept.sort(

            reverse=True,

            key=lambda gene:
                gene["fitness"]

        )

        if len(kept) > max_population:

            overflow = (

                kept[
                    max_population:
                ]

            )

            removed.extend(
                overflow
            )

            kept = (

                kept[
                    :max_population
                ]
            )

        return (

            kept,

            removed

        )