class ContextBuilder:

    def build(

        self,

        parent_a,

        parent_b,

        concepts,

        experiences,

        max_items=5

    ):

        context = []

        context.append(

            parent_a["knowledge"]

        )

        context.append(

            parent_b["knowledge"]

        )

        for concept in concepts:

            members = concept.get(

                "members",

                []

            )

            for member in members:

                if (

                    parent_a["knowledge"]

                    in member

                    or

                    parent_b["knowledge"]

                    in member

                ):

                    context.extend(
                        members
                    )

                    break

        for exp in experiences[-max_items:]:

            context.append(

                exp["result"]

            )

        return list(
            set(context)
        )