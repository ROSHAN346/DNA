import random


class CrossoverEngine:

    def crossover(
        self,
        genome_a,
        genome_b
    ):

        size = min(
            len(genome_a),
            len(genome_b)
        )

        point = random.randint(
            1,
            size - 1
        )

        child = (

            genome_a[:point]

            +

            genome_b[point:]

        )

        return child
    
    def create_child(
    self,
    parent_a,
    parent_b
):

        child = {}

        child["chromosome"] = (
            parent_a["chromosome"]
        )

        child["genome"] = (

            self.crossover(

                parent_a["genome"],

                parent_b["genome"]

            )

        )

        child["knowledge"] = (

            parent_a["knowledge"]

            +

            " + "

            +

            parent_b["knowledge"]

        )

        child["embedding"] = (
            parent_a["embedding"]
        )

        child["strength"] = (

            (
                parent_a["strength"]

                +

                parent_b["strength"]

            ) / 2

        )

        child["usage_count"] = 0

        child["generation"] = (

            max(

                parent_a["generation"],

                parent_b["generation"]

            )

            + 1

        )

        return child