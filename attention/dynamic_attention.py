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
        current = data.get(chromosome, 0.0)
        # Bounded activation between 0.0 and 1.0
        data[chromosome] = round(min(1.0, current + 0.3), 3)
        self.save(data)

    def get_weight(
        self,
        chromosome
    ):
        data = self.load()
        return data.get(chromosome, 0.0)

    def decay(self):
        data = self.load()
        for key in list(data.keys()):
            new_val = round(data[key] * 0.90, 3)
            if new_val < 0.05:
                # Prune negligible attention to clean storage
                data.pop(key, None)
            else:
                data[key] = new_val
        self.save(data)