import json
import time
from encoder.semantic_dna import (
    SemanticDNAEncoder
)

class NeuralMemory:

    def __init__(self,path):

        self.path = path
        self.encoder = (
    SemanticDNAEncoder()
)

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

    def add_memory(self,text):

        memories = self.load()

        embedding = (self.encoder.embedding( text))

        memories.append({

            "text": text,

            "embedding":
                embedding.tolist(),

            "importance": 0.5,

            "access_count": 1,

            "timestamp":
                time.time()

        })

        self.save(memories)

    def save_all(self,memories):

        self.save(memories)

    def get_all(self):

        return self.load()