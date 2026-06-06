from evolution.mutation import (
    MutationEngine
)

from evolution.crossover import (
    CrossoverEngine
)

from evolution.fitness import (
    FitnessEngine
)


class EvolutionEngine:

    def __init__(self,dna_memory):

        self.dna_memory = dna_memory

    def evolve(self):

        genes = (
            self.dna_memory
            .get_all()
        )

        if len(genes) < 2:

            return

        genes.sort(

            key=lambda g:
            FitnessEngine.score(g),

            reverse=True

        )

        parents = genes[:2]

        child_genome = (

            CrossoverEngine
            .crossover(

                parents[0]["genome"],

                parents[1]["genome"]

            )

        )

        child_genome = (

            MutationEngine
            .mutate(
                child_genome
            )

        )

        child_text = (

            parents[0]["knowledge"]

            +

            " | "

            +

            parents[1]["knowledge"]

        )

        self.dna_memory.add_gene(

            child_genome,

            child_text,

            0.8

        )

        print(
            "Evolution Completed"
        )