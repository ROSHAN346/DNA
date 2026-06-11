import random


class MutationEngine:

    BASES = [
        "A",
        "T",
        "C",
        "G"
    ]

    def mutate(
        self,
        genome,
        mutation_rate=0.01
    ):
        genome = list(genome)
        for i in range(len(genome)):
            if random.random() < mutation_rate:
                current = genome[i]
                choices = [
                    b
                    for b in self.BASES
                    if b != current
                ]
                genome[i] = random.choice(choices)
        return "".join(genome)

    def mutate_network(self, gene, population, mutation_rate=0.15):
        """
        Mutate the promoter and repressor connection network of a gene.
        """
        gene.setdefault("promoters", {})
        gene.setdefault("repressors", {})

        # 1. Perturb existing weights
        for conn_type in ["promoters", "repressors"]:
            connections = gene[conn_type]
            to_remove = []
            for target, weight in list(connections.items()):
                if random.random() < mutation_rate:
                    # Perturb weight by +/- 0.1
                    new_weight = weight + random.uniform(-0.1, 0.1)
                    if new_weight <= 0.01:
                        to_remove.append(target)
                    else:
                        connections[target] = round(float(new_weight), 3)
            for target in to_remove:
                connections.pop(target, None)

        # 2. Add a new random link if population is available
        if population and random.random() < mutation_rate:
            other = random.choice(population)
            if other["knowledge"] != gene["knowledge"]:
                conn_type = "promoters" if random.random() < 0.7 else "repressors"
                weight = round(random.uniform(0.1, 0.4), 3)
                gene.setdefault(conn_type, {})[other["knowledge"]] = weight

        # 3. Mutate base expression slightly
        if random.random() < mutation_rate:
            base_expr = gene.get("base_expression", 0.1)
            gene["base_expression"] = max(0.01, min(0.5, round(base_expr + random.uniform(-0.05, 0.05), 3)))

    def create_child(
        self,
        gene,
        population=None
    ):
        child = gene.copy()
        
        # Deep copy dictionary connections
        child["promoters"] = gene.get("promoters", {}).copy()
        child["repressors"] = gene.get("repressors", {}).copy()
        child["expression"] = 0.0

        child["genome"] = self.mutate(gene["genome"])
        child["generation"] = gene["generation"] + 1
        child["strength"] = round(float(gene["strength"] * 0.95), 4)
        child["usage_count"] = 0

        if "traits" not in gene:
            from evolution.gene_traits import GeneTraits
            gene["traits"] = GeneTraits().create_traits()

        child["traits"] = gene["traits"].copy()

        # Perform regulatory network mutation
        self.mutate_network(child, population or [])

        return child