from utils.cosine_similarity import (
    cosine_similarity
)

from evolution.fitness import (
    FitnessEngine
)


class MatingEngine:

    def __init__(self):

        self.fitness = (
            FitnessEngine()
        )

    def select_pair(

        self,

        genes,

        experiences

    ):

        if len(genes) < 2:

            return None

        best_pair = None

        best_score = -1

        for i in range(len(genes)):

            for j in range(i + 1, len(genes)):

                gene_a = genes[i]
                gene_b = genes[j]

                fitness_a = (

                    self.fitness
                    .calculate_full(

                        gene_a,

                        genes,

                        experiences

                    )

                )

                fitness_b = (

                    self.fitness
                    .calculate_full(

                        gene_b,

                        genes,

                        experiences

                    )

                )

                similarity = (

                    cosine_similarity(

                        gene_a["embedding"],

                        gene_b["embedding"]

                    )

                )

                diversity = (

                    1.0

                    -

                    similarity

                )

                score = (

                    fitness_a

                    +

                    fitness_b

                    +

                    diversity

                )

                if score > best_score:

                    best_score = score

                    best_pair = (

                        gene_a,

                        gene_b

                    )

        return best_pair