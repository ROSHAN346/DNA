from evolution.fitness import (
    FitnessEngine
)


class SelectionEngine:

    def __init__(self):

        self.fitness = (
            FitnessEngine()
        )

    def select_top(

        self,

        genes,

        top_k=3

    ):

        ranked = []

        for gene in genes:

            score = (

                self.fitness
                .calculate(
                    gene
                )

            )

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