import json

# from torch import embedding


class DNAMemory:

    def __init__(self,path):

        self.path = path
    
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

            with open(
                self.path,
                "r"
            ) as f:

                return json.load(f)

        except:

            return []

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
            strength
        ):

        genes = self.load()

        genes.append({

    "chromosome": chromosome,

    "genome": genome,

    "embedding": embedding.tolist(),

    "knowledge": text,

    "strength": strength,

    "usage_count": 0,

    "generation": 0
})

        self.save(genes)

    

    def get_all(self):

        return self.load()