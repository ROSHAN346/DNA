import random


class CrossoverEngine:

    @staticmethod
    def crossover(
        parent1,
        parent2
    ):

        length = min(
            len(parent1),
            len(parent2)
        )

        point = random.randint(
            1,
            length-1
        )

        child = (

            parent1[:point]

            +

            parent2[point:]

        )

        return child