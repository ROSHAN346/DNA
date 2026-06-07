from chromosomes.chromosome_classifier import ChromosomeClassifier
from evolution.pruning import PruningEngine
from utils.cosine_similarity import cosine_similarity
from memory.neural_memory import (
    NeuralMemory
)

from learning.experience_memory import (
    ExperienceMemory
)

from learning.learning_engine import (
    LearningEngine
)
from evolution.crossover import (
    CrossoverEngine
)

from evolution.gene_cleanup import (
    GeneCleanup
)

from concepts.concept_discovery import (
    ConceptDiscovery
)

from concepts.concept_engine import (
    ConceptEngine
)

from attention.dynamic_attention import (
    DynamicAttention
)

from evolution.selection import (
    SelectionEngine
)
from evolution.mutation import (
    MutationEngine
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

from graph.graph_search import (
    GraphSearch
)

from graph.knowledge_graph import (
    KnowledgeGraph
)

from evolution.gene_traits import (
    GeneTraits
)

from reasoning.inference_engine import (
    InferenceEngine
)


neural = NeuralMemory(
    "storage/neural_memory.json"
)

fitness_engine = (
    FitnessEngine()
)
pruning_engine = (
    PruningEngine()
)

crossover_engine = (
    CrossoverEngine()
)

selection_engine = (
    SelectionEngine()
)


mutation_engine = (
    MutationEngine()
)

graph = (
    KnowledgeGraph(
        "storage/knowledge_graph.json"
    )
)

graph_search = (
    GraphSearch()
)

dna = DNAMemory(
    "storage/dna_memory.json"
)

reinforcement = (
    ReinforcementEngine())


attention = (
    DynamicAttention()
)

concept_engine = (
    ConceptEngine()
)

inference_engine = (
    InferenceEngine()
)

concept_discovery = (
    ConceptDiscovery()
)

cleanup_engine = (
    GeneCleanup()
)

experience_memory = (
    ExperienceMemory()
)

learning_engine = (
    LearningEngine()
)

encoder = SemanticDNAEncoder()


while True:

    print("\n")

    print("1 Add Memory")

    print("2 Consolidate")

    print("3 Search")

    print("4 Exit")

    print("5 View DNA Genes")

    print("6 View Neural Memories")
    print("7 Prune DNA")

    print("8 View Selected Genes")
    print("9 View Mutated Children")
    print("10 Crossover Gene Mutation")
    print("11 Graph Search")
    print("12 Graph Traverse")
    print("13 Graph Traits")
    print("14 View Attention State")
    print("15 View Concept Associations")
    print("16 Run Inference Engine")
    print("17 View Discovered Concepts")
    print("18 View Cleaned Genes")
    print("19 Experience Learning Engine")

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

            experience_memory.add(

    query,

    text,

    source,

    score

)

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

                        attention.activate(

                            gene["chromosome"]

                        )

                        print(

                            "Attention Activated:",

                            gene["chromosome"]

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

        print("\nEnd of Genes")

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
    elif choice == "7":
        genes = (
            dna.get_all()
        )
        kept,removed = (
            pruning_engine.prune(
                genes
            )
        )
        dna.save_all(
            kept
        )

        print(
            "\nRemoved:"
        )

        for gene in removed:
            print(
                gene["knowledge"]
            )

        print(  
            "\nRemaining:",
            len(kept)
        )
    elif choice == "8":

        genes = dna.get_all()

        selected = (

            selection_engine
            .select_top(
                genes
            )

        )

        print(
            "\nSelected Genes:"
        )

        for score,gene in selected:

            print(
                "\nKnowledge:",
                gene["knowledge"]
            )

            print(
                "Fitness:",
                score
            )
    elif choice == "9":

        genes = (
            dna.get_all()
        )

        selected = (

            selection_engine
            .select_top(
                genes,
                1
            )

        )

        if len(selected) == 0:

            print(
                "No genes found"
            )

        else:

            score,parent = (
                selected[0]
            )

            child = (

                mutation_engine
                .create_child(
                    parent
                )

            )

            genes.append(
                child
            )

            dna.save_all(
                genes
            )

            print(
                "\nMutated Child Created"
            )

            print(
                "Parent:",
                parent["knowledge"]
            )

            print(
                "Generation:",
                child["generation"]
            )
    elif choice == "10":

        genes = dna.get_all()

        selected = (

            selection_engine
            .select_top(
                genes,
                2
            )

        )

        if len(selected) < 2:

            print(
                "Need at least 2 genes"
            )

        else:

            score_a,parent_a = selected[0]

            score_b,parent_b = selected[1]

            child = (

                crossover_engine
                .create_child(

                    parent_a,

                    parent_b

                )

            )

            genes.append(
                child
            )

            dna.save_all(
                genes
            )

            print(
                "\nChild Gene Created"
            )

            print(
                child["knowledge"]
            )
    elif choice == "11":

        node = input(
            "\nNode: "
        )

        neighbors = (

            graph_search.traverse(
                graph,
                node
            )

        )

        print(
            "\nRelations:"
        )

        for relation in neighbors:

            print(

                relation["relation"],

                "->",

                relation["target"]

            )
    elif choice == "12":

        node = input(
            "\nStart Node: "
        )

        path = (

            graph_search
            .traverse(

                graph,

                node,

                depth=5

            )

        )

        print(
            "\nTraversal:"
        )

        for relation in path:

            print(

                relation["source"],

                "--",

                relation["relation"],

                "-->",

                relation["target"],

                "(depth:",

                relation["depth"],

                ")"

            )
    elif choice == "13":

        genes = dna.get_all()

        for gene in genes:

            print(
                "\nKnowledge:",
                gene["knowledge"]
            )

            gene = (
                GeneTraits()
                .ensure_traits(
                    gene
                )
            )

            for k,v in gene["traits"].items():

                print(
                    k,
                    ":",
                    v
                )
    elif choice == "14":

        attention = (
            DynamicAttention()
        )

        data = (
            attention.load()
        )

        print(
            "\nAttention State:"
        )

        for key,val in data.items():

            print(

                key,

                ":",

                round(val,3)

            )
    elif choice == "15":

        concept = (

            concept_engine
            .build(
                dna.get_all()
            )

        )

        print(
            "\nConcepts Built:"
        )

        print(
            len(concept)
        )

        concepts = (
        concept_engine.load()
       )

        for concept in concepts:

            print(
                "\nConcept:",
                concept["concept"]
            )

            print(
                "Members:",
                concept["size"]
            )

            for member in concept["members"]:

                print(
                    " -",
                    member
                )
    elif choice == "16":
        
        graph_data = (
        graph.load()
        )

        results = (

                inference_engine
                .infer(
                    graph_data
                )

            )

        print(
                "\nGenerated",
                len(results),
                "inferences"
            )
        results = (
        inference_engine.load()
        )

        for item in results:

                print(

                    "\n",

                    item["from"],

                    "→",

                    item["to"],

                    "(through",

                    item["through"],

                    ")"

                )
    elif choice == "17":

        import json
        concepts = (

        concept_discovery
        .discover(

            dna.get_all(),

            n_clusters=3

        )

    )

        concept_discovery.save(
            concepts
        )

        print(

            "\nDiscovered",

            len(concepts),

            "concept groups"

        )

        with open(

            "storage/discovered_concepts.json",

            "r"

        ) as f:

            concepts = json.load(
                f
            )

        for concept in concepts:

            print(

                "\nCluster:",

                concept["cluster"]

            )

            print(

                "Members:",

                concept["size"]

            )

            for member in concept["members"]:

                print(
                    " -",
                    member
                )
    elif choice == "18":

        genes = (
            dna.get_all()
        )

        before = len(
            genes
        )

        genes = (

            cleanup_engine
            .cleanup(
                genes
            )

        )

        dna.save_all(
            genes
        )

        after = len(
            genes
        )

        print(
            "\nCleanup Complete"
        )

        print(
            "Before:",
            before
        )

        print(
            "After:",
            after
        )

        print(
            "Removed:",
            before - after
        )
    elif choice == "19":
        experiences = (

        experience_memory
        .get_all()

    )

        print(
            "\nExperiences:"
        )

        for exp in experiences:

            print(

                "\nQuery:",

                exp["query"]

            )

            print(

                "Result:",

                exp["result"]

            )

            print(

                "Source:",

                exp["source"]

            )

            print(

                "Score:",

                round(
                    exp["score"],
                    4
                )

            )

            experiences = (

            experience_memory
            .get_all()

        )

            summary = (

                learning_engine
                .summarize(
                    experiences
                )

            )

            print(
                "\nMost Used Knowledge:"
            )

            for item,count in summary.items():

                print(

                    count,

                    "->",

                    item

                )
