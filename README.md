# DNA Mimic Framework

A biologically-inspired cognitive AI framework that mimics the structure and adaptive behaviour of DNA to store, evolve, and reason over knowledge.

---

## What It Does

The framework treats every piece of knowledge like a **gene** in a DNA strand. Genes are encoded from raw text using semantic embeddings, classified into **chromosomes** (knowledge domains), and stored in a persistent DNA memory. Over time, genes evolve through **mutation**, **crossover**, **selection**, and **pruning** — just like biological evolution — guided by a fitness function that rewards strength, usage, novelty, and curiosity.

A separate **neural memory** holds raw episodic memories that are periodically **consolidated** into DNA genes. A **knowledge graph** captures relationships between entities and enables **transitive inference**. A **dynamic attention** system tracks which chromosomes are most recently activated, and a **policy engine** reinforces knowledge that leads to good retrieval outcomes.

---

## Project Structure

```
dna_brain/
├── app.py                        # Interactive CLI entry point
├── encoder/
│   └── semantic_dna.py           # Text → embedding → ATCG DNA string
├── chromosomes/
│   └── chromosome_classifier.py  # Classifies queries into domain chromosomes
├── memory/
│   ├── dna_memory.py             # Persistent gene storage (JSON)
│   ├── neural_memory.py          # Short-term episodic memory
│   ├── consolidation.py          # Neural → DNA consolidation engine
│   └── reinforcement.py         # Strength/usage reinforcement
├── evolution/
│   ├── fitness.py                # Multi-factor gene fitness scoring
│   ├── selection.py              # Tournament/top-k selection
│   ├── mutation.py               # Child gene creation via mutation
│   ├── crossover.py              # Two-parent gene crossover + synthesis
│   ├── mating_engine.py          # Parent pair selection
│   ├── pruning.py                # Remove low-fitness / redundant genes
│   ├── gene_cleanup.py           # Dedup and quality cleanup
│   ├── gene_traits.py            # Trait metadata per gene
│   ├── novelty_engine.py         # Novelty scoring vs population
│   ├── curiosity_engine.py       # Curiosity scoring vs experiences
│   └── survival_engine.py        # Survival filtering
├── attention/
│   ├── dynamic_attention.py      # Chromosome activation weights (with decay)
│   └── dna_attention.py          # Gene-level attention scoring
├── retrieval/
│   ├── hybrid_search.py          # Combined neural + DNA similarity search
│   ├── dna_search.py             # DNA-string based search
│   ├── neural_search.py          # Embedding cosine search
│   └── trait_retrieval.py        # Trait-filtered retrieval
├── graph/
│   ├── knowledge_graph.py        # Persistent entity-relation graph
│   ├── graph_builder.py          # Build graph from genes
│   └── graph_search.py           # BFS/DFS traversal
├── reasoning/
│   └── inference_engine.py       # Transitive inference over graph
├── concepts/
│   ├── concept_engine.py         # Build concept clusters from genes
│   ├── concept_discovery.py      # K-means concept discovery
│   ├── concept_naming.py         # Auto-name discovered clusters
│   └── clustering.py             # Embedding-based clustering
├── learning/
│   ├── experience_memory.py      # Store query→result experiences
│   ├── learning_engine.py        # Summarise experience patterns
│   ├── policy_engine.py          # Reward genes and chromosomes (RL-style)
│   ├── adaptive_synthesis.py     # Synthesise new knowledge adaptively
│   ├── context_builder.py        # Build crossover context from parents
│   └── concept_guide_synthesis.py # Concept-guided knowledge synthesis
├── utils/
│   ├── cosine_similarity.py
│   └── similarity.py
└── storage/                      # JSON persistence files
    ├── dna_memory.json
    ├── neural_memory.json
    ├── knowledge_graph.json
    ├── attention_memory.json
    ├── policy_memory.json
    ├── experience_memory.json
    ├── inference_memory.json
    └── discovered_concepts.json
```

---

## Setup

**Requirements:** Python 3.10+

```bash
# Create and activate virtual environment
python -m venv .venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # Linux/Mac

# Install dependencies
pip install sentence-transformers torch scikit-learn networkx numpy scipy
```

---

## Running

```bash
python app.py
```

You will see an interactive menu:

```
1  Add Memory              — store a raw text into neural memory
2  Consolidate             — compress neural memories into DNA genes
3  Search                  — hybrid semantic search + reinforcement
4  Exit
5  View DNA Genes          — list all genes with strength and usage
6  View Gene Fitness       — calculate fitness score for each gene
7  Prune DNA               — remove low-fitness genes
8  View Selected Genes     — top-k selection by fitness
9  View Mutated Children   — create a mutated child from best gene
10 Crossover Gene Mutation — create a child from two parent genes
11 Graph Search            — find neighbours of a node
12 Graph Traverse          — depth-limited BFS traversal
13 Graph Traits            — view trait metadata per gene
14 View Attention State    — see chromosome activation weights
15 View Concept Associations — cluster genes into concept groups
16 Run Inference Engine    — generate transitive graph inferences
17 View Discovered Concepts — k-means discovery on gene embeddings
18 View Cleaned Genes      — deduplicate and clean gene pool
19 Experience Learning     — review experiences + usage summary
```

---

## Core Concepts

| Concept | Biological analogy | What it does here |
|---|---|---|
| Gene | DNA gene | A single piece of knowledge with embedding, strength, traits |
| Chromosome | Chromosome | A knowledge domain / category |
| Genome | Base-pair sequence | ATCG string encoded from semantic embedding |
| Mutation | Point mutation | Creates a variation of a gene |
| Crossover | Recombination | Merges two parent genes into a synthesised child |
| Fitness | Natural fitness | Score based on strength, usage, novelty, curiosity, age |
| Pruning | Natural death | Removes genes below fitness threshold |
| Consolidation | Long-term potentiation | Moves neural memories into stable DNA |
| Attention | Synaptic salience | Tracks recently activated chromosomes |
| Inference | Reasoning | Derives new facts via transitive graph traversal |

---

## Dependencies

| Package | Purpose |
|---|---|
| `sentence-transformers` | Semantic embeddings (`all-MiniLM-L6-v2`) |
| `torch` | Embedding model backend |
| `scikit-learn` | K-means clustering for concept discovery |
| `networkx` | Knowledge graph structure |
| `numpy` / `scipy` | Vector math and similarity |
