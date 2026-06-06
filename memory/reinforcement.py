class ReinforcementEngine:

    def reinforce_gene(
        self,
        gene
    ):

        gene["usage_count"] += 1

        gene["strength"] += 0.01

        if gene["strength"] > 1:

            gene["strength"] = 1

        return gene

    def reinforce_memory(
        self,
        memory
    ):

        memory["access_count"] += 1

        memory["importance"] += 0.01

        if memory["importance"] > 1:

            memory["importance"] = 1

        return memory