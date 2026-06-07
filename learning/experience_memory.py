import json

from datetime import (
    datetime
)


class ExperienceMemory:

    def __init__(

        self,

        path="storage/experience_memory.json"

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

            return []

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

    def add(

        self,

        query,

        result,

        source,

        score

    ):

        data = self.load()

        data.append(

            {

                "query":
                    query,

                "result":
                    result,

                "source":
                    source,

                "score":
                    score,

                "timestamp":
                    str(
                        datetime.now()
                    )

            }

        )

        self.save(
            data
        )

    def get_all(self):

        return self.load()