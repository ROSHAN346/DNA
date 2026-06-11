from evolution.gene_traits import (
    GeneTraits
)

from evolution.novelty_engine import (
    NoveltyEngine
)

from evolution.curiosity_engine import (
    CuriosityEngine
)


class FitnessEngine:

    def __init__(self):

        self.traits = (
            GeneTraits()
        )

        self.novelty = (
            NoveltyEngine()
        )

        self.curiosity = (
            CuriosityEngine()
        )

    def calculate(

        self,

        gene

    ):

        gene = (

            self.traits
            .ensure_traits(
                gene
            )

        )

        strength = gene.get(
            "strength",
            0
        )

        usage_count = gene.get(
            "usage_count",
            0
        )

        generation = gene.get(
            "generation",
            0
        )

        age = gene.get(
            "age",
            0
        )

        trait_bonus = (

            self.traits
            .fitness_bonus(
                gene["traits"]
            )

        )

        age_penalty = (
            age * 0.005
        )

        fitness = (

            strength

            +

            (0.02 * usage_count)

            +

            (0.01 * generation)

            +

            (0.30 * trait_bonus)

            -

            age_penalty

        )

        return round(
            fitness,
            4
        )
    
    def calculate_population(
        self,
        gene,
        population
    ):
        base = self.calculate(gene)

        novelty = self.novelty.score(gene, population)

        # Calculate network centrality / density bonus
        knowledge = gene["knowledge"]
        incoming_promoters_count = sum(
            1 for other in population if knowledge in other.get("promoters", {})
        )
        total_connections = (
            incoming_promoters_count
            + len(gene.get("promoters", {}))
            + len(gene.get("repressors", {}))
        )
        network_density = total_connections / max(1, len(population))
        network_bonus = min(0.3, network_density * 0.5)

        fitness = base + (0.5 * novelty) + network_bonus

        return round(float(fitness), 4)
    def calculate_full(

    self,

    gene,

    population,

    experiences

        ):
        base = (

       self.calculate_population(

        gene,

        population

    )

        )

        curiosity = (

            self.curiosity
            .score(

                gene,

                experiences

            )

        )

        fitness = (

            base

            +

            (0.3 * curiosity)

        )

        return round(
            fitness,
            4
        )