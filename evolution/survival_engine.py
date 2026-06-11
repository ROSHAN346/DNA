from evolution.fitness import (
    FitnessEngine
)


class SurvivalEngine:

    def __init__(self):

        self.fitness = (
            FitnessEngine()
        )

    def survive(

        self,

        genes,

        max_population=100

    ):

        scored = []

        for gene in genes:

            score = (

                self.fitness
                .calculate(
                    gene
                )

            )

            scored.append(

                (
                    score,
                    gene
                )

            )

        scored.sort(

            reverse=True,

            key=lambda x:x[0]

        )

        survivors = [

            gene

            for score,gene

            in scored[:max_population]

        ]

        return survivors