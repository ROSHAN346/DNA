from evolution.fitness import (
    FitnessEngine
)


class PruningEngine:

    @staticmethod
    def prune(genes):

        survivors = []

        for gene in genes:

            score = (
                FitnessEngine
                .score(gene)
            )

            if score > 0.5:

                survivors.append(
                    gene
                )

        return survivors