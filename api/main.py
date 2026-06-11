import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from memory.neural_memory import NeuralMemory
from memory.dna_memory import DNAMemory
from memory.consolidation import ConsolidationEngine
from memory.reinforcement import ReinforcementEngine
from encoder.semantic_dna import SemanticDNAEncoder
from chromosomes.chromosome_classifier import ChromosomeClassifier
from retrieval.hybrid_search import HybridSearch
from evolution.fitness import FitnessEngine
from evolution.selection import SelectionEngine
from evolution.mutation import MutationEngine
from evolution.crossover import CrossoverEngine
from evolution.pruning import PruningEngine
from evolution.gene_cleanup import GeneCleanup
from evolution.mating_engine import MatingEngine
from evolution.gene_traits import GeneTraits
from attention.dynamic_attention import DynamicAttention
from graph.knowledge_graph import KnowledgeGraph
from graph.graph_search import GraphSearch
from reasoning.inference_engine import InferenceEngine
from concepts.concept_engine import ConceptEngine
from concepts.concept_discovery import ConceptDiscovery
from learning.experience_memory import ExperienceMemory
from learning.learning_engine import LearningEngine
from learning.policy_engine import PolicyEngine

app = FastAPI(title="DNA Mimic API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- shared instances ---
neural = NeuralMemory("storage/neural_memory.json")
dna = DNAMemory("storage/dna_memory.json")
encoder = SemanticDNAEncoder()
reinforcement = ReinforcementEngine()
attention = DynamicAttention()
graph = KnowledgeGraph("storage/knowledge_graph.json")
graph_search = GraphSearch()
inference_engine = InferenceEngine()
concept_engine = ConceptEngine()
concept_discovery = ConceptDiscovery()
experience_memory = ExperienceMemory()
learning_engine = LearningEngine()
policy = PolicyEngine()
fitness_engine = FitnessEngine()
selection_engine = SelectionEngine()
mutation_engine = MutationEngine()
crossover_engine = CrossoverEngine()
pruning_engine = PruningEngine()
cleanup_engine = GeneCleanup()
mating_engine = MatingEngine()


# ── Models ────────────────────────────────────────────────────────────────────

class TextIn(BaseModel):
    text: str

class QueryIn(BaseModel):
    query: str

class GraphQueryIn(BaseModel):
    node: str
    depth: int = 3

class PruneIn(BaseModel):
    threshold: float = 0.70
    max_population: int = 50


# ── Memory ────────────────────────────────────────────────────────────────────

@app.post("/memory/add")
def add_memory(body: TextIn):
    neural.add_memory(body.text)
    return {"status": "stored", "text": body.text}


@app.get("/memory/neural")
def get_neural():
    return neural.get_all()


@app.get("/memory/dna")
def get_dna():
    genes = dna.get_all()
    # strip large embedding arrays for UI speed
    return [
        {k: v for k, v in g.items() if k != "embedding"}
        for g in genes
    ]


@app.post("/memory/consolidate")
def consolidate():
    engine = ConsolidationEngine(neural, dna)
    engine.run()
    return {"status": "done", "genes": len(dna.get_all())}


# ── Search ────────────────────────────────────────────────────────────────────

@app.post("/search")
def search(body: QueryIn):
    q_emb = encoder.embedding(body.query)
    classifier = ChromosomeClassifier()
    chromosome = classifier.classify(body.query)
    neural_mems = neural.get_all()
    all_genes = dna.get_all()
    dna_genes = [g for g in all_genes if g["chromosome"] == chromosome]
    hybrid = HybridSearch()
    results = hybrid.search(q_emb, neural_mems, dna_genes)

    if results:
        score, text, source, details = results[0]
        experience_memory.add(body.query, text, source, score)
        attention.decay()
        for mem in neural_mems:
            if mem["text"] == text:
                reinforcement.reinforce_memory(mem)
                break
        for gene in dna_genes:
            if gene["knowledge"] == text:
                reinforcement.reinforce_gene(gene, dna_genes)
                policy.reward_gene(gene["knowledge"])
                policy.reward_chromosome(gene["chromosome"])
                attention.activate(gene["chromosome"])
                break
        neural.save_all(neural_mems)
        dna.save_all(all_genes)

    return {
        "chromosome": chromosome,
        "results": [
            {"score": round(s, 4), "text": t, "source": src, "details": det}
            for s, t, src, det in results
        ],
    }


# ── Evolution ─────────────────────────────────────────────────────────────────

@app.get("/evolution/fitness")
def gene_fitness():
    genes = dna.get_all()
    return [
        {
            "knowledge": g["knowledge"],
            "chromosome": g["chromosome"],
            "strength": g.get("strength", 0),
            "usage_count": g.get("usage_count", 0),
            "generation": g.get("generation", 0),
            "age": g.get("age", 0),
            "fitness": fitness_engine.calculate(g),
        }
        for g in genes
    ]


@app.get("/evolution/selected")
def selected_genes():
    genes = dna.get_all()
    selected = selection_engine.select_top(genes)
    return [
        {"fitness": round(s, 4), "knowledge": g["knowledge"], "chromosome": g["chromosome"]}
        for s, g in selected
    ]


@app.post("/evolution/mutate")
def mutate():
    genes = dna.get_all()
    selected = selection_engine.select_top(genes, 1)
    if not selected:
        raise HTTPException(400, "No genes available")
    _, parent = selected[0]
    child = mutation_engine.create_child(parent, genes)
    genes.append(child)
    dna.save_all(genes)
    return {"parent": parent["knowledge"], "child": child["knowledge"], "generation": child["generation"]}


@app.post("/evolution/crossover")
def crossover():
    genes = dna.get_all()
    experiences = experience_memory.get_all()
    pair = mating_engine.select_pair(genes, experiences)
    if pair is None:
        raise HTTPException(400, "Need at least 2 genes")
    parent_a, parent_b = pair
    child = crossover_engine.create_child(parent_a, parent_b)
    genes.append(child)
    dna.save_all(genes)
    return {
        "parent_a": parent_a["knowledge"],
        "parent_b": parent_b["knowledge"],
        "child": child["knowledge"],
    }


@app.post("/evolution/prune")
def prune(body: PruneIn):
    genes = dna.get_all()
    experiences = experience_memory.get_all()
    kept, removed = pruning_engine.prune(genes, experiences, body.threshold, body.max_population)
    dna.save_all(kept)
    return {"kept": len(kept), "removed": [g["knowledge"] for g in removed]}


@app.post("/evolution/cleanup")
def cleanup():
    genes = dna.get_all()
    before = len(genes)
    genes = cleanup_engine.cleanup(genes)
    dna.save_all(genes)
    return {"before": before, "after": len(genes), "removed": before - len(genes)}


# ── Attention ─────────────────────────────────────────────────────────────────

@app.get("/attention")
def get_attention():
    data = attention.load()
    return [{"chromosome": k, "weight": round(v, 4)} for k, v in data.items()]


# ── Graph ─────────────────────────────────────────────────────────────────────

@app.get("/graph")
def get_graph():
    return graph.load()


@app.post("/graph/search")
def graph_search_endpoint(body: GraphQueryIn):
    results = graph_search.traverse(graph, body.node, depth=body.depth)
    return results


@app.post("/graph/infer")
def run_inference():
    graph_data = graph.load()
    results = inference_engine.infer(graph_data)
    return results


@app.get("/graph/inferences")
def get_inferences():
    return inference_engine.load()


# ── Concepts ──────────────────────────────────────────────────────────────────

@app.post("/concepts/build")
def build_concepts():
    genes = dna.get_all()
    concept_engine.build(genes)
    return concept_engine.load()


@app.post("/concepts/discover")
def discover_concepts(n_clusters: int = 3):
    genes = dna.get_all()
    if len(genes) < n_clusters:
        raise HTTPException(400, f"Need at least {n_clusters} genes")
    concepts = concept_discovery.discover(genes, n_clusters=n_clusters)
    concept_discovery.save(concepts)
    return concepts


@app.get("/concepts")
def get_concepts():
    return concept_discovery.load()


# ── Learning ──────────────────────────────────────────────────────────────────

@app.get("/learning/experiences")
def get_experiences():
    return experience_memory.get_all()


@app.get("/learning/summary")
def learning_summary():
    experiences = experience_memory.get_all()
    summary = learning_engine.summarize(experiences)
    return [{"knowledge": k, "count": v} for k, v in summary.items()]


@app.get("/learning/policy")
def get_policy():
    return policy.load()


# ── Dashboard stats ───────────────────────────────────────────────────────────

@app.get("/stats")
def stats():
    genes = dna.get_all()
    neural_mems = neural.get_all()
    graph_data = graph.load()
    avg_strength = round(sum(g.get("strength", 0) for g in genes) / max(len(genes), 1), 3)
    avg_fitness = round(sum(fitness_engine.calculate(g) for g in genes) / max(len(genes), 1), 3)
    return {
        "genes": len(genes),
        "neural_memories": len(neural_mems),
        "graph_nodes": len(graph_data),
        "experiences": len(experience_memory.get_all()),
        "concepts": len(concept_discovery.load()),
        "inferences": len(inference_engine.load()),
        "chromosomes": list({g["chromosome"] for g in genes}),
        "chromosome_counts": {c: sum(1 for g in genes if g.get("chromosome") == c) for c in {g["chromosome"] for g in genes}},
        "avg_strength": avg_strength,
        "avg_fitness": avg_fitness,
        "total_usage": sum(g.get("usage_count", 0) for g in genes),
        "max_generation": max((g.get("generation", 0) for g in genes), default=0),
    }


@app.get("/stats/genome")
def genome_stats():
    """ATCG nucleotide distribution across all genes."""
    genes = dna.get_all()
    counts = {"A": 0, "T": 0, "C": 0, "G": 0}
    for g in genes:
        for ch in g.get("genome", ""):
            if ch in counts:
                counts[ch] += 1
    total = sum(counts.values()) or 1
    return {k: {"count": v, "pct": round(v / total * 100, 1)} for k, v in counts.items()}


@app.get("/stats/chromosomes")
def chromosome_stats():
    """Per-chromosome gene count, avg strength, avg fitness."""
    genes = dna.get_all()
    buckets: dict = {}
    for g in genes:
        c = g.get("chromosome", "unknown")
        buckets.setdefault(c, []).append(g)
    result = []
    for c, gs in buckets.items():
        result.append({
            "chromosome": c,
            "count": len(gs),
            "avg_strength": round(sum(x.get("strength", 0) for x in gs) / len(gs), 3),
            "avg_fitness": round(sum(fitness_engine.calculate(x) for x in gs) / len(gs), 3),
            "total_usage": sum(x.get("usage_count", 0) for x in gs),
        })
    return sorted(result, key=lambda x: x["count"], reverse=True)


@app.get("/evolution/history")
def evolution_history():
    """Return genes grouped by generation for timeline view."""
    genes = dna.get_all()
    buckets: dict = {}
    for g in genes:
        gen = g.get("generation", 0)
        buckets.setdefault(gen, []).append({
            "knowledge": g["knowledge"],
            "chromosome": g["chromosome"],
            "strength": round(g.get("strength", 0), 3),
            "fitness": round(fitness_engine.calculate(g), 3),
        })
    return [{"generation": k, "genes": v} for k, v in sorted(buckets.items())]


@app.get("/activity")
def activity_feed():
    """Recent experiences as activity log."""
    experiences = experience_memory.get_all()
    # most recent first (assume list order is chronological)
    recent = list(reversed(experiences))[:20]
    return [
        {
            "query": e.get("query", ""),
            "result": e.get("result", "")[:80],
            "source": e.get("source", ""),
            "score": round(e.get("score", 0), 3),
        }
        for e in recent
    ]




