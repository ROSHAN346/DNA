# DESIGN — DNA Mimic Framework

Architecture and cognitive design reference for the DNA Mimic Framework.

---

## 1. Design Philosophy

The framework is built around one central idea: **knowledge should behave like living matter**. Biological DNA does not simply store information — it evolves, competes, recombines, decays, and adapts to its environment. This framework applies the same principles to machine knowledge.

Every concept learned by the system is encoded as a **gene**. Genes live inside **chromosomes** (domain categories), compete for survival via **fitness scoring**, reproduce through **mutation and crossover**, and die through **pruning**. The result is a self-organising knowledge base that strengthens useful memories and discards weak ones automatically.

---

## 2. Cognitive Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                        INPUT TEXT                               │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
              ┌──────────────────┐
              │  Neural Memory   │  ← short-term episodic store
              └────────┬─────────┘
                       │ Consolidation
                       ▼
              ┌──────────────────┐
              │   DNA Memory     │  ← long-term gene store
              │  (chromosomes)   │
              └────────┬─────────┘
          ┌────────────┼────────────┐
          ▼            ▼            ▼
     Evolution     Retrieval     Graph &
     Engine        Engine        Reasoning
          │            │            │
          └────────────┴────────────┘
                       │
                       ▼
              ┌──────────────────┐
              │  Learning Layer  │  ← policy, experience, synthesis
              └──────────────────┘
```

---

## 3. Module Design

### 3.1 Encoder — `encoder/semantic_dna.py`

**Cognitive analogy:** DNA base-pair transcription.

Converts raw text into two representations:
- **Embedding** — a 384-dimensional float vector via `all-MiniLM-L6-v2`
- **Genome** — an ATCG string derived by bucketing each normalised embedding dimension into one of four nucleotide symbols

```
value < 0.25  →  A
value < 0.50  →  T
value < 0.75  →  C
value >= 0.75 →  G
```

This genome string enables fast symbolic comparison between genes using Hamming-distance style matching, while the embedding enables semantic cosine similarity.

---

### 3.2 Memory Layer

#### Neural Memory — `memory/neural_memory.py`
Short-term episodic store. Holds raw text memories with `importance` and `access_count` fields. Acts as the input buffer before consolidation.

#### DNA Memory — `memory/dna_memory.py`
Long-term persistent gene store backed by `storage/dna_memory.json`. Each gene carries:

| Field | Description |
|---|---|
| `chromosome` | Domain category |
| `genome` | ATCG string |
| `embedding` | Float vector (384-d) |
| `knowledge` | Raw text |
| `strength` | [0, 1] — decays and grows over use |
| `usage_count` | How many times retrieved |
| `generation` | How many crossover/mutation cycles deep |
| `age` | Increments each cycle; penalises old weak genes |
| `traits` | Metadata dict (see Gene Traits) |

#### Consolidation — `memory/consolidation.py`
Transfers neural memories into DNA genes. Duplicate detection prevents re-encoding the same text; near-duplicates strengthen an existing gene rather than creating a new one.

#### Reinforcement — `memory/reinforcement.py`
On every successful retrieval, increments `usage_count` and increases `strength` for both the matched neural memory and DNA gene.

---

### 3.3 Chromosome Classifier — `chromosomes/chromosome_classifier.py`

Maps a query string to a knowledge domain (chromosome name). Used to narrow retrieval to relevant genes before similarity scoring, reducing search space and improving precision.

---

### 3.4 Evolution Engine

The evolution subsystem governs the entire lifecycle of genes.

#### Fitness — `evolution/fitness.py`

Three-tier fitness calculation:

```
base_fitness = strength
             + (0.02 × usage_count)
             + (0.01 × generation)
             + (0.30 × trait_bonus)
             - (0.005 × age)

population_fitness = base_fitness + (0.5 × novelty_score)

full_fitness = population_fitness + (0.3 × curiosity_score)
```

- **Novelty** (`novelty_engine.py`) — how different a gene's embedding is from all others in the population (rewards diversity)
- **Curiosity** (`curiosity_engine.py`) — how often this gene appears in underexplored experience paths (rewards unexplored knowledge)

#### Selection — `evolution/selection.py`
Top-k selection by fitness score. Acts as a survival filter before mutation and crossover.

#### Mutation — `evolution/mutation.py`
Takes the fittest gene and produces a child with small random variations in strength and a bumped generation counter. Represents point mutation.

#### Crossover — `evolution/crossover.py`
Takes two parent genes selected by `mating_engine.py`:
1. Splices their genome strings at a random crossover point
2. Builds semantic context from both parents using `context_builder.py`
3. Synthesises new knowledge text via `concept_guide_synthesis.py`
4. Averages parent strengths; increments generation

This is the framework's primary knowledge synthesis mechanism — new concepts emerge from combining existing ones.

#### Gene Traits — `evolution/gene_traits.py`
Each gene carries a `traits` dict with metadata flags (e.g., `is_rare`, `is_dominant`, `is_stable`). Traits contribute a bonus to fitness and guide synthesis decisions.

#### Pruning — `evolution/pruning.py`
Removes genes that fall below a configurable fitness threshold and enforces a maximum population cap. Lower-fitness genes are culled first.

#### Gene Cleanup — `evolution/gene_cleanup.py`
Deduplication pass: removes near-identical genes (by text or embedding similarity) that would dilute the gene pool.

#### Survival Engine — `evolution/survival_engine.py`
Final survival filter applied after pruning — ensures the remaining population meets minimum viability criteria.

---

### 3.5 Retrieval Engine

#### Hybrid Search — `retrieval/hybrid_search.py`
Combines results from both stores:
- **Neural search** (`neural_search.py`) — cosine similarity over neural memory embeddings
- **DNA search** (`dna_search.py`) — genome string similarity + embedding cosine over DNA genes

Results are merged and ranked by a combined score. The top result triggers reinforcement.

#### Trait Retrieval — `retrieval/trait_retrieval.py`
Filters the gene pool by trait metadata before similarity scoring. Enables targeted retrieval (e.g., "only stable genes", "only rare genes").

---

### 3.6 Attention System

#### Dynamic Attention — `attention/dynamic_attention.py`
Tracks which chromosomes have been recently activated, persisted to `storage/attention_memory.json`.

- **activate(chromosome)** — increments activation counter
- **get_weight(chromosome)** — returns salience score (capped at 1.0), scaled by `0.05 × count`
- **decay()** — multiplies all weights by 0.95 on each cycle, implementing exponential forgetting

This gives frequently queried domains higher retrieval priority and naturally fades attention away from idle domains.

#### DNA Attention — `attention/dna_attention.py`
Gene-level attention scoring based on individual gene activity.

---

### 3.7 Knowledge Graph and Reasoning

#### Knowledge Graph — `graph/knowledge_graph.py`
Persistent directed graph of entity–relation–entity triples, stored as a JSON adjacency structure. Built from genes by `graph_builder.py`.

#### Graph Search — `graph/graph_search.py`
BFS/DFS traversal with configurable depth. Returns paths as `{source, relation, target, depth}` records.

#### Inference Engine — `reasoning/inference_engine.py`
Applies transitive inference over the graph:

```
A → B and B → C  ⟹  infer A → C  (rule: transitive)
```

Inferred facts are stored in `storage/inference_memory.json` and surface as derived knowledge during retrieval.

---

### 3.8 Concept System

#### Concept Engine — `concepts/concept_engine.py`
Clusters genes into concept groups using embedding similarity. Saves associations to `storage/concept_memory.json`.

#### Concept Discovery — `concepts/concept_discovery.py`
Runs K-means clustering directly on gene embeddings to discover emergent concept groups without predefined labels.

#### Concept Naming — `concepts/concept_naming.py`
Auto-generates a human-readable label for each cluster by extracting dominant terms from its member genes.

---

### 3.9 Learning Layer

#### Experience Memory — `learning/experience_memory.py`
Every search records a `{query, result, source, score}` experience in `storage/experience_memory.json`. This becomes the RL feedback signal.

#### Learning Engine — `learning/learning_engine.py`
Summarises experience patterns — finds which knowledge pieces appear most frequently as top results.

#### Policy Engine — `learning/policy_engine.py`
Reinforcement learning style reward tracker. On a successful retrieval:
- `reward_gene(knowledge)` — increments reward counter for that gene
- `reward_chromosome(chromosome)` — increments reward counter for that domain

Rewards are read back during mating pair selection to prefer high-performing genes.

#### Adaptive Synthesis — `learning/adaptive_synthesis.py`
Generates new knowledge text during crossover, guided by parent context and experience signals.

#### Context Builder — `learning/context_builder.py`
Assembles a synthesis prompt from two parent genes, their concept memberships, and recent experiences.

#### Concept-Guided Synthesis — `learning/concept_guide_synthesis.py`
Synthesises crossover knowledge steered toward the dominant concept cluster of the parent pair.

---

## 4. Data Flow: Add → Consolidate → Search

```
1. User inputs text
       │
       ▼
2. NeuralMemory.add_memory(text)
       │  stores: {text, importance, access_count, embedding}
       ▼
3. ConsolidationEngine.run()
       │  for each neural memory:
       │    encode → ATCG genome
       │    classify → chromosome
       │    check duplicate in DNA
       │    if new: DNAMemory.add_gene(...)
       │    if exists: strengthen existing gene
       ▼
4. User queries
       │
       ▼
5. ChromosomeClassifier.classify(query) → active chromosome
6. HybridSearch.search(embedding, neural_memories, dna_genes)
       │  returns [(score, text, source), ...]
       ▼
7. Top result triggers:
       │  ReinforcementEngine.reinforce_gene/memory(...)
       │  PolicyEngine.reward_gene/chromosome(...)
       │  DynamicAttention.activate(chromosome)
       │  ExperienceMemory.add(query, result, ...)
```

---

## 5. Data Flow: Evolution Cycle

```
1. FitnessEngine.calculate_full(gene, population, experiences)
       │  → base + novelty + curiosity score
       ▼
2. SelectionEngine.select_top(genes) → ranked survivors
       ▼
3a. MutationEngine.create_child(parent)
       │  → slight variation, generation + 1
3b. MatingEngine.select_pair(genes, experiences)
    CrossoverEngine.create_child(parent_a, parent_b)
       │  → genome splice + synthesised knowledge
       ▼
4. PruningEngine.prune(genes, threshold, max_population)
       │  → remove below-threshold and excess genes
       ▼
5. GeneCleanup.cleanup(genes)
       │  → remove near-duplicates
       ▼
6. DNAMemory.save_all(genes)
```

---

## 6. Persistence

All state is stored as plain JSON files under `storage/`:

| File | Contents |
|---|---|
| `dna_memory.json` | All DNA genes |
| `neural_memory.json` | Short-term episodic memories |
| `knowledge_graph.json` | Entity–relation graph |
| `attention_memory.json` | Chromosome activation weights |
| `policy_memory.json` | Gene and chromosome reward counts |
| `experience_memory.json` | Query–result experience log |
| `inference_memory.json` | Transitive inference results |
| `discovered_concepts.json` | K-means cluster output |
| `concept_memory.json` | Concept engine associations |

No database is required. The entire system is file-portable.

---

## 7. Cognitive Concepts Applied

| Concept | Mechanism in Framework |
|---|---|
| **Long-term potentiation** | Consolidation moves repeated neural memories into stable DNA genes |
| **Synaptic decay** | Dynamic attention weights decay by 5% each cycle |
| **Natural selection** | Fitness-based pruning removes weak genes |
| **Genetic recombination** | Crossover splices genomes and synthesises new knowledge |
| **Point mutation** | Mutation engine creates slight variations of existing genes |
| **Episodic memory** | Neural memory stores raw experiences before encoding |
| **Semantic memory** | DNA memory stores stable, structured knowledge |
| **Reinforcement learning** | Policy engine rewards genes/chromosomes that produce good retrievals |
| **Curiosity-driven exploration** | Curiosity score boosts genes linked to underexplored experience paths |
| **Concept formation** | K-means clustering discovers emergent knowledge groups |
| **Transitive reasoning** | Inference engine derives indirect facts from graph paths |
| **Working memory** | `brain/working_memory.py` holds in-session active context |

---

## 8. Extension Points

- **New chromosome domains** — add entries to the chromosome classifier vocabulary
- **Custom fitness weights** — adjust coefficients in `FitnessEngine.calculate()`
- **Alternative encoders** — swap `all-MiniLM-L6-v2` for a domain-specific model in `SemanticDNAEncoder`
- **Graph population** — feed `graph_builder.py` with entity extraction from any NLP pipeline
- **Synthesis backend** — replace `AdaptiveSynthesis` with an LLM call for richer crossover text generation
- **Persistent attention decay** — schedule `DynamicAttention.decay()` on a timer rather than per-query
