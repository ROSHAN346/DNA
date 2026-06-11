import json
import numpy as np
from pathlib import Path

from encoder.semantic_dna import SemanticDNAEncoder


class ChromosomeClassifier:
    """Embedding-based chromosome classifier that creates chromosomes dynamically."""

    SIMILARITY_THRESHOLD = 0.65  # Minimum similarity to assign to existing chromosome

    def __init__(self, storage_path="storage/chromosomes.json"):
        self.storage_path = Path(storage_path)
        self.encoder = SemanticDNAEncoder()
        self.chromosomes = self._load_chromosomes()

    def _load_chromosomes(self):
        """Load chromosomes with their centroid embeddings."""
        if self.storage_path.exists():
            with open(self.storage_path, "r") as f:
                return json.load(f)
        return {"chromosomes": []}

    def _save_chromosomes(self):
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.storage_path, "w") as f:
            json.dump(self.chromosomes, f, indent=2)

    def _cosine_similarity(self, a, b):
        """Compute cosine similarity between two vectors."""
        a = np.array(a)
        b = np.array(b)
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-9)

    def _generate_name(self, text):
        """Generate a name from text keywords."""
        words = text.lower().split()
        # Filter short words and take first 3 meaningful ones
        keywords = [w for w in words if len(w) > 3][:3]
        if keywords:
            return "_".join(keywords)
        return f"topic_{len(self.chromosomes['chromosomes']) + 1}"

    def classify(self, text):
        """Classify text into existing chromosome or create new one."""
        embedding = self.encoder.embedding(text).tolist()
        chromosomes = self.chromosomes.get("chromosomes", [])

        # Find best matching chromosome
        best_match = None
        best_score = -1

        for chrom in chromosomes:
            sim = self._cosine_similarity(embedding, chrom["centroid"])
            if sim > best_score:
                best_score = sim
                best_match = chrom

        # Assign to existing chromosome if similar enough
        if best_score >= self.SIMILARITY_THRESHOLD:
            return best_match["name"]

        # Create new chromosome
        new_name = self._generate_name(text)
        new_chrom = {
            "name": new_name,
            "centroid": embedding,
            "sample_text": text,
            "gene_count": 1
        }
        chromosomes.append(new_chrom)
        self.chromosomes["chromosomes"] = chromosomes
        self._save_chromosomes()
        print(f"Created new chromosome: {new_name}")
        return new_name

    def update_centroid(self, chromosome_name, new_embedding):
        """Update centroid after adding a new gene."""
        chromosomes = self.chromosomes.get("chromosomes", [])
        for chrom in chromosomes:
            if chrom["name"] == chromosome_name:
                # Running average update
                old_centroid = np.array(chrom["centroid"])
                new_centroid = (old_centroid + np.array(new_embedding)) / 2
                chrom["centroid"] = new_centroid.tolist()
                chrom["gene_count"] = chrom.get("gene_count", 0) + 1
                break
        self._save_chromosomes()

    def get_all(self):
        """Return all chromosomes."""
        return self.chromosomes.get("chromosomes", [])