class ReinforcementEngine:

    def reinforce_gene(
        self,
        gene,
        all_genes=None
    ):
        gene["usage_count"] += 1
        gene["strength"] += 0.02
        if gene["strength"] > 1.0:
            gene["strength"] = 1.0

        # Hebbian Learning: Strengthen promoter connection weights from active nodes to this gene
        if all_genes:
            target_knowledge = gene["knowledge"]
            gene.setdefault("promoters", {})
            for other in all_genes:
                if other["knowledge"] != target_knowledge and other.get("expression", 0.0) >= 0.4:
                    current_w = gene["promoters"].get(other["knowledge"], 0.0)
                    # Strengthen promoter weight (max 1.0)
                    gene["promoters"][other["knowledge"]] = round(float(min(1.0, current_w + 0.04)), 3)

                    # Co-activation also strengthens the other direction's base promoter weight slightly
                    other.setdefault("promoters", {})
                    other_current_w = other["promoters"].get(target_knowledge, 0.0)
                    other["promoters"][target_knowledge] = round(float(min(1.0, other_current_w + 0.02)), 3)

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