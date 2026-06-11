from utils.cosine_similarity import (
    cosine_similarity
)


class NoveltyEngine:

    def score(

        self,

        gene,

        population

    ):

        similarities = []

        for other in population:

            if other is gene:

                continue

            try:

                sim = (

                    cosine_similarity(

                        gene["embedding"],

                        other["embedding"]

                    )

                )

                similarities.append(
                    sim
                )

            except Exception:

                continue

        if len(similarities) == 0:

            return 1.0

        avg_similarity = (

            sum(similarities)

            /

            len(similarities)

        )

        novelty = (

            1.0

            -

            avg_similarity

        )

        novelty = max(

            0.0,

            min(

                1.0,

                novelty

            )

        )

        return round(
            novelty,
            4
        )