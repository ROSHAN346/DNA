from sentence_transformers import SentenceTransformer


class SemanticDNAEncoder:

    def __init__(self):

        self.model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

    def embedding(self,text):

        return self.model.encode(text)

    def embedding_to_dna(self,embedding):

        mn = embedding.min()
        mx = embedding.max()

        normalized = (
            embedding - mn
        ) / (mx - mn + 1e-9)

        dna = ""

        for value in normalized:

            if value < 0.25:
                dna += "A"

            elif value < 0.50:
                dna += "T"

            elif value < 0.75:
                dna += "C"

            else:
                dna += "G"

        return dna

    def encode(self,text):

        emb = self.embedding(text)

        return self.embedding_to_dna(emb)