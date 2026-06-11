from collections import Counter


class ConceptGuidedSynthesis:

    def synthesize(

        self,

        context

    ):

        words = []

        stop_words = {

            "is",

            "are",

            "the",

            "a",

            "an",

            "of",

            "and",

            "to",

            "in",

            "with",

            "for"

        }

        for text in context:

            for word in (

                text.lower()
                .split()

            ):

                if (

                    word not in stop_words

                    and

                    len(word) > 3

                ):

                    words.append(
                        word
                    )

        common = (

            Counter(words)

            .most_common(10)

        )

        summary = [

            word

            for word,count

            in common

        ]

        if len(summary) == 0:

            return (
                "General Concept"
            )

        return (

            "Concept: "

            +

            " ".join(summary[:5])

        )