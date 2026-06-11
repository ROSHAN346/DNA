"""
Genome utility functions for biologically-realistic evolution.

Hamming distance  — base-level sequence divergence
GC content        — thermodynamic stability proxy
Genome alignment  — pad shorter genome to equal length for comparison
"""


def align(genome_a, genome_b):
    """Pad shorter genome with 'A' so both are equal length."""
    diff = len(genome_a) - len(genome_b)
    if diff > 0:
        genome_b = genome_b + "A" * diff
    elif diff < 0:
        genome_a = genome_a + "A" * (-diff)
    return genome_a, genome_b


def hamming_distance(genome_a, genome_b):
    """
    Normalised Hamming distance in [0, 1].
    0 = identical, 1 = completely different.
    """
    a, b = align(genome_a, genome_b)
    mismatches = sum(x != y for x, y in zip(a, b))
    return mismatches / len(a)


def gc_content(genome):
    """
    Fraction of G+C bases.
    High GC → thermodynamically stable → lower mutation susceptibility.
    Typical biological range: 0.35 – 0.65
    """
    if not genome:
        return 0.5
    gc = sum(1 for b in genome if b in ("G", "C"))
    return gc / len(genome)


def genome_similarity(genome_a, genome_b):
    """1 - hamming_distance, so 1.0 = identical."""
    return 1.0 - hamming_distance(genome_a, genome_b)
