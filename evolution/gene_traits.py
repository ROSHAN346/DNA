import random


class GeneTraits:

    def create_traits(self):

        return {

            "attention_weight":

                round(
                    random.uniform(
                        0.4,
                        0.6
                    ),
                    3
                ),

            "retrieval_priority":

                round(
                    random.uniform(
                        0.4,
                        0.6
                    ),
                    3
                ),

            "mutation_rate":

                round(
                    random.uniform(
                        0.01,
                        0.05
                    ),
                    3
                ),

            "association_strength":

                round(
                    random.uniform(
                        0.4,
                        0.6
                    ),
                    3
                )

        }

    def mutate_traits(

        self,

        traits,

        mutation_strength=0.05

    ):

        new_traits = traits.copy()

        for key in new_traits:

            delta = random.uniform(

                -mutation_strength,

                mutation_strength

            )

            new_traits[key] += delta

            new_traits[key] = max(

                0,

                min(

                    1,

                    round(
                        new_traits[key],
                        3
                    )

                )

            )

        return new_traits

    def crossover_traits(

        self,

        traits_a,

        traits_b

    ):

        child_traits = {}

        for key in traits_a:

            child_traits[key] = round(

                (

                    traits_a[key]

                    +

                    traits_b[key]

                ) / 2,

                3

            )

        return child_traits

    def fitness_bonus(

        self,

        traits

    ):

        return round(

            (

                traits["attention_weight"]

                +

                traits["retrieval_priority"]

                +

                traits["association_strength"]

            ) / 3,

            3

        )

    def ensure_traits(

        self,

        gene

    ):

        if "traits" not in gene:

            gene["traits"] = (

                self.create_traits()

            )

        return gene