from encoder.semantic_dna import (
    SemanticDNAEncoder
)

from chromosomes.chromosome_classifier import (
    ChromosomeClassifier
)


class ConsolidationEngine:

    def __init__(
        self,
        neural_memory,
        dna_memory
    ):

        self.encoder = (
            SemanticDNAEncoder()
        )

        self.classifier = (
            ChromosomeClassifier()
        )

        self.neural = (
            neural_memory
        )

        self.dna = (
            dna_memory
        )

    def run(self):

        memories = (
            self.neural.get_all()
        )

        print(
            f"\nFound {len(memories)} memories"
        )

        for memory in memories:

            importance = (

                memory["importance"]

                +

                0.1 *

                memory["access_count"]

            )

            print(
                "\n----------------"
            )

            print(
                "Memory:",
                memory["text"]
            )

            print(
                "Importance:",
                round(
                    importance,
                    4
                )
            )

            if importance >= 0.6:

                print(
                    "Passed Threshold"
                )

                embedding = (

                    self.encoder
                    .embedding(
                        memory["text"]
                    )

                )

                genome = (

                    self.encoder
                    .encode(
                        memory["text"]
                    )

                )

                chromosome = (

                    self.classifier
                    .classify(
                        memory["text"]
                    )

                )

                print(
                    "Chromosome:",
                    chromosome
                )

                print(
                    "Genome Length:",
                    len(genome)
                )

                if self.dna.exists(
                    memory["text"]
                ):

                    self.dna.strengthen_existing(
                        memory["text"]
                    )

                    print(
                        "Existing Gene Strengthened"
                    )

                else:

                    self.dna.add_gene(

                        chromosome,

                        genome,

                        embedding,

                        memory["text"],

                        importance

                    )

                    print(
                        "New Gene Saved"
                    )

            else:

                print(
                    "Below Threshold"
                )

        print(
            "\nConsolidation Complete"
        )