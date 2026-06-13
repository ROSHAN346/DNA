import numpy as np
import logging

logger = logging.getLogger(__name__)

try:
    from sentence_transformers import SentenceTransformer
    HAS_TRANSFORMERS = True
except ImportError:
    HAS_TRANSFORMERS = False


class SemanticDNAEncoder:

    def __init__(self):
        if HAS_TRANSFORMERS:
            try:
                self.model = SentenceTransformer("all-MiniLM-L6-v2")
                logger.info("SentenceTransformer loaded successfully.")
            except Exception as e:
                logger.warning(f"Failed to load SentenceTransformer: {e}. Using fallback embedding method.")
                self.model = None
        else:
            logger.warning("sentence-transformers not installed. Using fallback embedding method.")
            self.model = None

    def embedding(self, text):
        if self.model is not None:
            try:
                return self.model.encode(text)
            except Exception as e:
                logger.warning(f"Error encoding with model: {e}. Falling back.")
        
        # Fallback: simple deterministic text hashing vectorizer to 384 dimensions
        dimensions = 384
        embedding = np.zeros(dimensions, dtype=np.float32)
        words = text.lower().split()
        if not words:
            return embedding
            
        for word_idx, word in enumerate(words):
            # Calculate a simple hash for each word
            h = 0
            for char in word:
                h = (h * 31 + ord(char)) & 0xFFFFFFFF
            
            # Map word hash to embedding dimensions
            idx = h % dimensions
            weight = 1.0 / (word_idx + 1)  # Position-based weight decay
            embedding[idx] += weight
            # Apply local smoothing
            embedding[(idx - 1) % dimensions] += weight * 0.3
            embedding[(idx + 1) % dimensions] += weight * 0.3
            
        # Add character n-grams count to catch spelling variations
        for i in range(len(text) - 2):
            ngram = text[i:i+3]
            h = 0
            for char in ngram:
                h = (h * 31 + ord(char)) & 0xFFFFFFFF
            idx = h % dimensions
            embedding[idx] += 0.1
            
        # Normalize vector
        norm = np.linalg.norm(embedding)
        if norm > 0:
            embedding = embedding / norm
            
        return embedding

    def embedding_to_dna(self, embedding):
        mn = embedding.min()
        mx = embedding.max()

        normalized = (
            embedding - mn
        ) / (mx - mn + 1e-9)

        dna = ""
        for value in normalized:
            if value < 0.25:
                dna += "A"
            elif value < 0.50:
                dna += "T"
            elif value < 0.75:
                dna += "C"
            else:
                dna += "G"

        return dna

    def encode(self, text):
        emb = self.embedding(text)
        return self.embedding_to_dna(emb)