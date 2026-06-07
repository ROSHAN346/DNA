import json


class DynamicAttention:

    def __init__(

        self,

        path="storage/attention_memory.json"

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

            return {}

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

    def activate(

        self,

        chromosome

    ):

        data = self.load()

        data[chromosome] = (

            data.get(
                chromosome,
                0
            )

            +

            1

        )

        self.save(data)

    def get_weight(

        self,

        chromosome

    ):

        data = self.load()

        value = data.get(
            chromosome,
            0
        )

        return min(

            value * 0.05,

            1.0

        )

    def decay(self):

        data = self.load()

        for key in data:

            data[key] *= 0.95

        self.save(data)