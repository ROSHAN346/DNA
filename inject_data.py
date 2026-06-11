import os
import json
import sys
sys.path.insert(0, os.getcwd())

from encoder.semantic_dna import SemanticDNAEncoder
from memory.neural_memory import NeuralMemory
from memory.dna_memory import DNAMemory
from memory.consolidation import ConsolidationEngine

print("--- Resetting all storage databases to clean state ---")

# Database paths
storage_files = {
    "storage/dna_memory.json": "[]",
    "storage/neural_memory.json": "[]",
    "storage/knowledge_graph.json": "{}",
    "storage/attention_memory.json": "{}",
    "storage/experience_memory.json": "[]",
    "storage/inference_memory.json": "[]",
    "storage/discovered_concepts.json": "[]",
    "storage/concept_memory.json": "[]",
    "storage/chromosomes.json": '{"chromosomes": []}',
    "storage/policy_memory.json": '{"genes": {}, "chromosomes": {}, "concepts": {}}'
}

for path, empty_val in storage_files.items():
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(empty_val)
    print(f"  Cleared: {path}")

print("\n--- Initializing framework engines ---")
encoder = SemanticDNAEncoder()
neural = NeuralMemory("storage/neural_memory.json")
dna = DNAMemory("storage/dna_memory.json")

fresh_memories = [
    # Topic 1: Artificial Intelligence (AI) and Hardware
    "Deep learning models require massive GPU parallel processing capacity to train.",
    "High bandwidth memory on GPUs accelerates tensor computations in transformer models.",
    "Tensor processing units (TPUs) provide specialized hardware acceleration for neural networks.",
    
    # Topic 2: Plant Biology and Ecology
    "Photosynthesis converts solar energy into chemical energy in green plants.",
    "Chlorophyll absorbs red and blue light to catalyze organic molecule synthesis.",
    "Ecosystems maintain carbon balance through plant respiration and carbon dioxide uptake.",
    
    # Topic 3: Human Cognitive Psychology
    "Working memory holds active concepts in consciousness for processing.",
    "Long term potentiation strengthens synaptic connections during memory consolidation."
]

print("\n--- Injecting fresh memories into neural storage ---")
for text in fresh_memories:
    neural.add_memory(text)
    print(f"  Added neural: '{text[:50]}...'")

print("\n--- Running Consolidation Engine (Neural -> DNA + GRN build) ---")
engine = ConsolidationEngine(neural, dna)
engine.run()

print("\n--- Fresh Data Injection & Consolidation Complete ---")
print(f"Total DNA Genes consolidated: {len(dna.get_all())}")
