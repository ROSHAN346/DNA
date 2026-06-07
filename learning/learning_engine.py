from collections import (
    Counter
)


class LearningEngine:

    def summarize(

        self,

        experiences

    ):

        concepts = []

        for exp in experiences:

            concepts.append(

                exp["result"]

            )

        counts = Counter(
            concepts
        )

        return counts