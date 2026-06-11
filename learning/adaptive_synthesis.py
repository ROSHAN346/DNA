class AdaptiveSynthesis:

    def synthesize(

        self,

        parent_a,

        parent_b,

        policy

    ):

        text_a = (
            parent_a["knowledge"]
        )

        text_b = (
            parent_b["knowledge"]
        )

        reward_a = (

            policy
            .get_gene_reward(
                text_a
            )

        )

        reward_b = (

            policy
            .get_gene_reward(
                text_b
            )

        )

        if reward_a > reward_b:

            dominant = text_a

        else:

            dominant = text_b

        child = (

            "Generalized Insight: "

            +

            dominant

        )

        return child