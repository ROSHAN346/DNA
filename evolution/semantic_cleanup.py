from utils.cosine_similarity import (
    cosine_similarity
)

from evolution.fitness import (
    FitnessEngine
)


class SemanticCleanup:

    def __init__(self):

        self.fitness = (
            FitnessEngine()
        )

    def remove_similar(

        self,

        genes,

        threshold=0.90

    ):

        kept = []

        for gene in genes:

            is_duplicate = False

            for existing in kept:

                similarity = (

                    cosine_similarity(

                        gene["embedding"],

                        existing["embedding"]

                    )

                )

                print(

                    "\nSimilarity:",

                    round(
                        similarity,
                        4
                    )

                )
                print(

                    gene["knowledge"]
                )
                print(

                        existing["knowledge"]

                    )

                if similarity >= threshold:

                    current_fitness = (

                        self.fitness
                        .calculate(
                            gene
                        )

                    )

                    existing_fitness = (

                        self.fitness
                        .calculate(
                            existing
                        )

                    )

                    if current_fitness > existing_fitness:

                        kept.remove(
                            existing
                        )

                        kept.append(
                            gene
                        )

                    is_duplicate = True

                    break

            if not is_duplicate:

                kept.append(
                    gene
                )

        return kept