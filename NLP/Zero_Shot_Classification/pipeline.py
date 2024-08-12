from transformers import pipeline


class LLM:
    """
    A class used to generate text using a text2text-generation model.

    ...

    Attributes
    ----------
    generator : pipeline
        a transformers pipeline for text2text-generation

    Methods
    -------
    ask_question(query):
        Generates text based on the given query.
    """

    def __init__(self):
        """
        Constructs all the necessary attributes for the LLM object.
        """

        self.generator = pipeline("text2text-generation", model="facebook/bart-large")

    def ask_question(self, query):
        """
        Generates text based on the given query.

        Parameters
        ----------
            query : str
                a string representing the query

        Returns
        -------
        str
            a string representing the generated text
        """

        return self.generator(query)[0]["generated_text"]
