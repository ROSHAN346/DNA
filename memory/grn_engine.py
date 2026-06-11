from utils.cosine_similarity import cosine_similarity


class GRNEngine:
    """
    Gene Regulatory Network (GRN) Engine.
    Controls environment upregulation and dynamic activation propagation
    across promoter and repressor connections.
    """

    def __init__(self, upregulation_threshold=0.6, default_decay=0.85):
        self.upregulation_threshold = upregulation_threshold
        self.default_decay = default_decay

    def initialize_expression(self, genes, query_embedding):
        """
        Stimulate the network based on environment (query).
        Genes matching the query above upregulation_threshold are stimulated.
        """
        for gene in genes:
            sim = cosine_similarity(query_embedding, gene["embedding"])
            if sim >= self.upregulation_threshold:
                # Direct stimulus based on similarity and gene health/strength
                gene["expression"] = round(float(sim * gene.get("strength", 1.0)), 4)
            else:
                # Baseline background expression
                gene["expression"] = gene.get("base_expression", 0.0)

    def propagate(self, genes, steps=3, decay=None):
        """
        Simulate activation propagation through promoter/repressor links.
        """
        if decay is None:
            decay = self.default_decay

        # Run simulation steps
        for step in range(steps):
            # Create a lookup mapping gene knowledge string to current expression
            expr_lookup = {g["knowledge"]: g["expression"] for g in genes}
            new_expressions = {}

            for gene in genes:
                current_val = gene["expression"]
                knowledge = gene["knowledge"]

                # 1. Decay the current expression
                new_val = current_val * decay

                # 2. Add promoter signals: sum(promoter_expr * promoter_weight)
                promoter_signal = 0.0
                for promoter_name, weight in gene.get("promoters", {}).items():
                    if promoter_name in expr_lookup:
                        promoter_signal += expr_lookup[promoter_name] * weight
                new_val += promoter_signal

                # 3. Subtract repressor signals: sum(repressor_expr * repressor_weight)
                repressor_signal = 0.0
                for repressor_name, weight in gene.get("repressors", {}).items():
                    if repressor_name in expr_lookup:
                        repressor_signal += expr_lookup[repressor_name] * weight
                new_val -= repressor_signal

                # Clamp expression values to [0.0, 1.0]
                new_expressions[knowledge] = max(0.0, min(1.0, round(float(new_val), 4)))

            # Update all genes in-place for the next iteration
            for gene in genes:
                gene["expression"] = new_expressions[gene["knowledge"]]
