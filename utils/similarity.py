def dna_similarity(
    dna1,
    dna2
):

    length = min(
        len(dna1),
        len(dna2)
    )

    matches = 0

    for i in range(length):

        if dna1[i] == dna2[i]:
            matches += 1

    return matches / length