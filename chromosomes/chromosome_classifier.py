class ChromosomeClassifier:

    ANIMALS = [
        "dog",
        "cat",
        "lion",
        "tiger",
        "animal"
    ]

    PROGRAMMING = [
        "python",
        "java",
        "c++",
        "javascript"
    ]

    MATH = [
        "algebra",
        "matrix",
        "calculus"
    ]

    def classify(
        self,
        text
    ):

        t = text.lower()

        for word in self.ANIMALS:

            if word in t:
                return "animals"

        for word in self.PROGRAMMING:

            if word in t:
                return "programming"

        for word in self.MATH:

            if word in t:
                return "mathematics"

        return "general"