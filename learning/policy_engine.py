import json


class PolicyEngine:

    def __init__(

        self,

        path="storage/policy_memory.json"

    ):

        self.path = path

    def load(self):

        try:

            with open(
                self.path,
                "r"
            ) as f:

                return json.load(f)

        except:

            return {

                "genes": {},

                "chromosomes": {},

                "concepts": {}

            }

    def save(

        self,

        data

    ):

        with open(
            self.path,
            "w"
        ) as f:

            json.dump(
                data,
                f,
                indent=4
            )

    def reward_gene(

        self,

        knowledge

    ):

        data = self.load()

        genes = data["genes"]

        genes[knowledge] = (

            genes.get(
                knowledge,
                0
            )

            +

            1

        )

        self.save(data)

    def reward_chromosome(

        self,

        chromosome

    ):

        data = self.load()

        chrom = data["chromosomes"]

        chrom[chromosome] = (

            chrom.get(
                chromosome,
                0
            )

            +

            1

        )

        self.save(data)

    def get_gene_reward(

        self,

        knowledge

    ):

        data = self.load()

        return (

            data["genes"]

            .get(

                knowledge,

                0

            )

        )

    def get_chromosome_reward(

        self,

        chromosome

    ):

        data = self.load()

        return (

            data["chromosomes"]

            .get(

                chromosome,

                0

            )

        )