from encoder.semantic_dna import SemanticDNAEncoder
from memory.neural_memory import NeuralMemory
from memory.dna_memory import DNAMemory
from chromosomes.chromosome_classifier import ChromosomeClassifier
from utils.similarity import dna_similarity

from graph.graph_builder import GraphBuilder

builder = GraphBuilder()

print(
    builder.extract(
        "Dogs are loyal pets"
    )
)