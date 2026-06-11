from utils.cosine_similarity import cosine_similarity
from retrieval.trait_retrieval import TraitRetrieval
from evolution.gene_traits import GeneTraits
from memory.grn_engine import GRNEngine


class DNASearch:

    def __init__(self):
        self.traits = TraitRetrieval()
        self.gene_traits = GeneTraits()
        self.grn = GRNEngine()

    def search(
        self,
        query_embedding,
        genes,
        top_k=5
    ):
        if not genes:
            return []

        # 1. Initialize gene expressions based on query embedding overlap
        self.grn.initialize_expression(genes, query_embedding)

        # 2. Run regulatory activation propagation simulation
        self.grn.propagate(genes, steps=3)

        # 3. Rank genes based on resulting expression levels combined with traits
        ranked = []
        for gene in genes:
            gene = self.gene_traits.ensure_traits(gene)
            expression_score = gene.get("expression", 0.0)
            final_score = self.traits.score(expression_score, gene)
            ranked.append((final_score, gene))

        ranked.sort(reverse=True, key=lambda x: x[0])
        return ranked[:top_k]