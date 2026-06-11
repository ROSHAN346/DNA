import random

from learning.adaptive_synthesis import (
    AdaptiveSynthesis
)

from learning.policy_engine import (
    PolicyEngine
)

from learning.context_builder import (
    ContextBuilder
)

from learning.concept_guide_synthesis import (
    ConceptGuidedSynthesis
)

from concepts.concept_discovery import (
    ConceptDiscovery
)

from learning.experience_memory import (
    ExperienceMemory
)

class CrossoverEngine:

    def __init__(self):

        self.policy = (
            PolicyEngine()
        )

        self.synthesis = (
            AdaptiveSynthesis()
        )

        self.context_builder = (
    ContextBuilder()
)

        self.guided_synthesis = (
            ConceptGuidedSynthesis()
        )

        self.concept_memory = (
        ConceptDiscovery()
    )

        self.experience_memory = (
            ExperienceMemory()
        )

    def crossover(

        self,

        genome_a,

        genome_b

    ):

        size = min(

            len(genome_a),
            len(genome_b)

        )

        point = random.randint(

            1,

            size - 1

        )

        child_genome = (

            genome_a[:point]

            +

            genome_b[point:]

        )

        return child_genome

    def crossover_network(self, parent_a, parent_b):
        """
        Recombine the promoter/repressor connections of two parents.
        """
        child_promoters = {}
        child_repressors = {}

        # 1. Combine promoters
        all_promoter_keys = set(parent_a.get("promoters", {}).keys()).union(
            parent_b.get("promoters", {}).keys()
        )
        for key in all_promoter_keys:
            weight_a = parent_a.get("promoters", {}).get(key)
            weight_b = parent_b.get("promoters", {}).get(key)
            if weight_a is not None and weight_b is not None:
                # Average weight
                child_promoters[key] = round((weight_a + weight_b) / 2, 3)
            elif weight_a is not None and random.random() < 0.5:
                child_promoters[key] = weight_a
            elif weight_b is not None and random.random() < 0.5:
                child_promoters[key] = weight_b

        # 2. Combine repressors
        all_repressor_keys = set(parent_a.get("repressors", {}).keys()).union(
            parent_b.get("repressors", {}).keys()
        )
        for key in all_repressor_keys:
            weight_a = parent_a.get("repressors", {}).get(key)
            weight_b = parent_b.get("repressors", {}).get(key)
            if weight_a is not None and weight_b is not None:
                # Average weight
                child_repressors[key] = round((weight_a + weight_b) / 2, 3)
            elif weight_a is not None and random.random() < 0.5:
                child_repressors[key] = weight_a
            elif weight_b is not None and random.random() < 0.5:
                child_repressors[key] = weight_b

        return child_promoters, child_repressors

    def create_child(
        self,
        parent_a,
        parent_b
    ):
        import numpy as np

        child = {}

        child["chromosome"] = (
            parent_a["chromosome"]
        )

        child["genome"] = (
            self.crossover(
                parent_a["genome"],
                parent_b["genome"]
            )
        )

        concepts = (
            self.concept_memory.load()
        )

        experiences = (
            self.experience_memory.get_all()
        )

        context = (
            self.context_builder
            .build(
                parent_a,
                parent_b,
                concepts,
                experiences
            )
        )

        child["knowledge"] = (
            self.guided_synthesis
            .synthesize(
                context
            )
        )

        # Average parent embeddings to represent dynamic recombination in semantic space
        emb_a = np.array(parent_a["embedding"])
        emb_b = np.array(parent_b["embedding"])
        child["embedding"] = ((emb_a + emb_b) / 2).tolist()

        child["strength"] = (parent_a["strength"] + parent_b["strength"]) / 2
        child["usage_count"] = 0
        child["expression"] = 0.0
        child["base_expression"] = round(float(child["strength"] * 0.1), 3)

        # Recombine network connections
        promoters, repressors = self.crossover_network(parent_a, parent_b)
        child["promoters"] = promoters
        child["repressors"] = repressors

        child["generation"] = (
            max(
                parent_a["generation"],
                parent_b["generation"]
            )
            + 1
        )

        child["gene_type"] = (
            "synthesized"
        )
        child["age"] = 0

        child["parents"] = [
            parent_a["knowledge"],
            parent_b["knowledge"]
        ]

        return child