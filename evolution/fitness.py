class FitnessEngine:

    def calculate(

        self,

        gene,

        neural_memory=None

    ):

        strength = gene.get(
            "strength",
            0
        )

        usage_count = gene.get(
            "usage_count",
            0
        )

        generation = gene.get(
            "generation",
            0
        )

        importance = 0
        access_count = 0

        if neural_memory:

            importance = neural_memory.get(
                "importance",
                0
            )

            access_count = neural_memory.get(
                "access_count",
                0
            )

        fitness = (

            strength

            +

            (0.02 * usage_count)

            +

            (0.01 * generation)

            +

            (0.5 * importance)

            +

            (0.01 * access_count)

        )

        return round(
            fitness,
            4
        )