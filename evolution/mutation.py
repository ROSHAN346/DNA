import random

BASES = ['A','T','C','G']


class MutationEngine:

    @staticmethod
    def mutate(
        genome,
        mutation_rate=0.02
    ):

        genome = list(genome)

        for i in range(len(genome)):

            if random.random() < mutation_rate:

                genome[i] = random.choice(
                    BASES
                )

        return ''.join(genome)