from evolution.fitness import (
    FitnessEngine
)

from evolution.semantic_cleanup import (
    SemanticCleanup
)


class GeneCleanup:

    def __init__(self):

        self.fitness = (
            FitnessEngine()
        )

        self.semantic = (
        SemanticCleanup()
    )

    def remove_duplicates(

        self,

        genes

    ):

        best = {}

        for gene in genes:

            knowledge = (
                gene["knowledge"]
                .strip()
                .lower()
            )

            fitness = (

                self.fitness
                .calculate(
                    gene
                )

            )

            if knowledge not in best:

                best[knowledge] = (

                    fitness,

                    gene

                )

            else:

                old_fitness = (

                    best[knowledge][0]

                )

                if fitness > old_fitness:

                    best[knowledge] = (

                        fitness,

                        gene

                    )

        cleaned = [

            item[1]

            for item in best.values()

        ]

        return cleaned
    
    def remove_weak(

    self,

    genes,

    threshold=0.7

):

        result = []

        for gene in genes:

            fitness = (

                self.fitness
                .calculate(
                    gene
                )

            )

            if fitness >= threshold:

                result.append(
                    gene
                )

        return result
    
    def cleanup(

    self,

    genes

):

        genes = (

            self.remove_duplicates(
                genes
            )

        )

        genes = (

            self.remove_weak(
                genes
            )

        )

        genes = (

            self.semantic
            .remove_similar(
                genes
            )

        )

        return genes