from chromosomes.chromosome_classifier import ChromosomeClassifier
from utils.cosine_similarity import cosine_similarity
from memory.neural_memory import (
    NeuralMemory
)

from evolution.fitness import (
    FitnessEngine
)

from retrieval.hybrid_search import (
    HybridSearch
)

from memory.dna_memory import (
    DNAMemory
)

from memory.reinforcement import (
    ReinforcementEngine
)

from memory.consolidation import (
    ConsolidationEngine
)

from attention.dna_attention import (
    DNAAttention
)

from encoder.semantic_dna import (
    SemanticDNAEncoder
)

from utils.similarity import (
    dna_similarity
)


neural = NeuralMemory(
    "storage/neural_memory.json"
)

fitness_engine = (
    FitnessEngine()
)

dna = DNAMemory(
    "storage/dna_memory.json"
)

reinforcement = (
    ReinforcementEngine())

encoder = SemanticDNAEncoder()


while True:

    print("\n")

    print("1 Add Memory")

    print("2 Consolidate")

    print("3 Search")

    print("4 Exit")

    print("5 View DNA Genes")

    print("6 View Neural Memories")

    choice = input(
        "\nChoice: "
    )

    if choice == "1":

        text = input(
            "\nMemory: "
        )

        neural.add_memory(text)

        print(
            "Stored in Neural Memory"
        )

    elif choice == "2":

        engine = (
            ConsolidationEngine(
                neural,
                dna
            )
        )

        engine.run()

    elif choice == "3":

        query = input(
            "\nQuery: "
        )

        query_embedding = (
            encoder.embedding(
                query
            )
        )

        classifier = (
            ChromosomeClassifier()
        )

        active_chromosome = (
            classifier.classify(
                query
            )
        )

        print(
            "\nActivated Chromosome:",
            active_chromosome
        )

        hybrid = (
            HybridSearch()
        )

        neural_memories = (
            neural.get_all()
        )

        classifier = (
            ChromosomeClassifier()
        )

        chromosome = (
            classifier.classify(query)
        )

        dna_genes = (
            dna.get_by_chromosome(
                chromosome
            )
        )

        results = hybrid.search(
            query_embedding,
            neural_memories,
            dna_genes
        )

        print(
            "\nTop Results:"
        )

        for score,text,source in results:

            print(

                f"[{source}]",

                round(score,4),

                text

            )

        if len(results) > 0:

            score,text,source = results[0]

            if len(results) > 0:

                score,text,source = results[0]

                # Reinforce Neural Memory

                for memory in neural_memories:

                    if memory["text"] == text:

                        reinforcement.reinforce_memory(
                            memory
                        )

                        break

                # Reinforce DNA Memory

                for gene in dna_genes:

                    if gene["knowledge"] == text:

                        reinforcement.reinforce_gene(
                            gene
                        )

                        break

        neural.save_all(
            neural_memories
        )

        dna.save_all(
            dna.get_all()
        )

        print(
            "\nTop Memory Reinforced"
        )
    elif choice == "4":

        break
    elif choice == "5":

        genes = dna.get_all()

        print("\nDNA Genes:")

        for gene in genes:

            print(

                gene["knowledge"],

                "#Strength:", gene["strength"],

                "#Usage Count:", gene["usage_count"]

            )

        print(
            "\nEnd of Genes"
        )

        memory = neural.get_all()
        print("\nNeural Memories:")
        for mem in memory:

            print(

                mem["text"],

                "#Importance:", mem["importance"],

                "#Access Count:", mem["access_count"]

            )
    elif choice == "6":

        genes = dna.get_all()

        print(
            "\nGene Fitness:"
        )

        for gene in genes:

            fitness = (

                fitness_engine
                .calculate(
                    gene
                )

            )

            print(

                "\nKnowledge:",

                gene["knowledge"]

            )

            print(

                "Fitness:",

                fitness

            )