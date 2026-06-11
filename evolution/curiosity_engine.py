from collections import Counter


class CuriosityEngine:

    def score(

        self,

        gene,

        experiences

    ):

        if len(experiences) == 0:

            return 1.0

        concepts = []

        for exp in experiences:

            concepts.append(

                exp.get(

                    "result",

                    ""

                )

            )

        counts = Counter(
            concepts
        )

        usage = counts.get(

            gene["knowledge"],

            0

        )

        curiosity = (

            1.0

            /

            (usage + 1)

        )

        return curiosity