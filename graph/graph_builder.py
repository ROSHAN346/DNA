class GraphBuilder:

    def extract(
        self,
        text
    ):

        text = text.lower()

        relations = []

        if "dog" in text:

            relations.append(

                (
                    "Dog",
                    "is_a",
                    "Animal"
                )

            )

        elif "cat" in text:

            relations.append(

                (
                    "Cat",
                    "is_a",
                    "Animal"
                )

            )

        elif "python" in text:

            relations.append(

                (
                    "Python",
                    "is_a",
                    "ProgrammingLanguage"
                )

            )

        elif "matrix" in text:

            relations.append(

                (
                    "Matrix",
                    "belongs_to",
                    "Mathematics"
                )

            )
        else :

            relations.append(

                (
                    "ye naaya data hoga",
                    "related_to",
                    "Jello bhai ka data hoga"
                )

            )

        return relations