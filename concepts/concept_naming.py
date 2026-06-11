from collections import Counter


class ConceptNaming:

    def generate(

        self,

        members,

        chromosomes=None

    ):

        if chromosomes:

            votes = Counter(
                chromosomes
            )

            winner = (

                votes
                .most_common(1)[0][0]

            )

            return winner

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

        for text in members:

            for word in (

                text.lower()
                .split()

            ):

                word = word.strip()

                if (

                    len(word) > 2

                    and

                    word not in stop_words

                ):

                    words.append(
                        word
                    )

        if not words:

            return (
                "unknown_concept"
            )

        common = (

            Counter(words)

            .most_common(2)

        )

        return (

            "_".join(

                [

                    word

                    for word,count

                    in common

                ]

            )

        )