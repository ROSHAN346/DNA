import json

from evolution.gene_traits import (
    GeneTraits
)
# from torch import embedding


class DNAMemory:

    def __init__(self,path):

        self.path = path
        self.traits = (
    GeneTraits()
      )
    
    def  save_all(
            self , 
            genes
    ):
        self.save(genes)

    def exists(
    self,
    text
):

        genes = self.load()

        for gene in genes:

            if gene["knowledge"] == text:

                return True

        return False
    
    def strengthen_existing(
    self,
    text,
    amount=0.05
):

        genes = self.load()

        for gene in genes:

            if gene["knowledge"] == text:

                gene["strength"] += amount

                if gene["strength"] > 1:

                    gene["strength"] = 1

                self.save(
                    genes
                )

                return True

        return False

    def get_by_chromosome(
        self,
        chromosome
        ):

        genes = self.load()

        return [

            gene

            for gene in genes

            if gene["chromosome"]
            ==
            chromosome

        ]

    def load(self):
        try:
            with open(self.path, "r") as f:
                genes = json.load(f)
        except:
            genes = []

        modified = False
        for gene in genes:
            if "promoters" not in gene:
                gene["promoters"] = {}
                modified = True
            if "repressors" not in gene:
                gene["repressors"] = {}
                modified = True
            if "expression" not in gene:
                gene["expression"] = 0.0
                modified = True
            if "base_expression" not in gene:
                gene["base_expression"] = round(float(gene.get("strength", 0.5) * 0.1), 3)
                modified = True
        if modified and genes:
            self.save(genes)
        return genes

    def save(self,data):

        with open(
            self.path,
            "w"
        ) as f:

            json.dump(
                data,
                f,
                indent=4
            )
    
    def get_by_chromosome(
    self,
    chromosome
   ):

        genes = self.load()

        return [

            gene

            for gene in genes

            if gene["chromosome"]
            ==
            chromosome

        ]

    def add_gene(
            self,
            chromosome,
            genome,
            embedding,
            text,
            strength,
            promoters=None,
            repressors=None
        ):
        genes = self.load()

        emb_list = embedding if isinstance(embedding, list) else embedding.tolist()

        if promoters is None:
            promoters = {}
            from utils.cosine_similarity import cosine_similarity
            for other in genes:
                sim = cosine_similarity(emb_list, other["embedding"])
                if sim >= 0.7:
                    promoters[other["knowledge"]] = round(float(sim * 0.3), 3)
                    other.setdefault("promoters", {})[text] = round(float(sim * 0.3), 3)

        if repressors is None:
            repressors = {}
            from utils.cosine_similarity import cosine_similarity
            for other in genes:
                if other["chromosome"] == chromosome:
                    sim = cosine_similarity(emb_list, other["embedding"])
                    if sim < 0.4:
                        repressors[other["knowledge"]] = round(float((0.4 - sim) * 0.2), 3)
                        other.setdefault("repressors", {})[text] = round(float((0.4 - sim) * 0.2), 3)

        genes.append({
            "chromosome": chromosome,
            "genome": genome,
            "embedding": emb_list,
            "knowledge": text,
            "strength": strength,
            "expression": 0.0,
            "base_expression": round(float(strength * 0.1), 3),
            "promoters": promoters,
            "repressors": repressors,
            "usage_count": 0,
            "generation": 0,
            "age": 0,
            "traits": self.traits.create_traits()
        })

        self.save(genes)

    

    def get_all(self):

        return self.load()