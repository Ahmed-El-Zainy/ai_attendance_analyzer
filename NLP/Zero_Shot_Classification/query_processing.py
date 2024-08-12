import json
from transformers import pipeline
import pandas as pd


class QueryProcessor:
    """
    A class used to process queries using a zero-shot-classification model.

    ...

    Attributes
    ----------
    data : DataFrame
        a pandas DataFrame containing the data to be queried
    model : pipeline
        a transformers pipeline for zero-shot-classification
    intents : dict
        a dictionary mapping intent names to intent data

    Methods
    -------
    load_intents(intents_file):
        Loads intents from a JSON file.
    set_data(data):
        Sets the data to be queried.
    process_query(query):
        Processes a query and returns the result.
    most_common_visitor_type():
        Returns the most common visitor type.
    most_visitors_in_minute():
        Returns the minute with the most visitors.
    visitor_count_with_single_attribute(query):
        Returns the count of visitors with a specific attribute.
    visitors_during_peak_time(query):
        Returns the count of visitors with a specific attribute during peak time.
    """

    def __init__(self, intents_file):
        """
        Constructs all the necessary attributes for the QueryProcessor object.

        Parameters
        ----------
            intents_file : str
                a string representing the path to the JSON file containing intents
        """

        self.data = None
        self.model = pipeline(
            "zero-shot-classification", model="facebook/bart-large-mnli"
        )
        self.intents = self.load_intents(intents_file)

    def load_intents(self, intents_file):
        """
        Loads intents from a JSON file.

        Parameters
        ----------
            intents_file : str
                a string representing the path to the JSON file containing intents

        Returns
        -------
        dict
            a dictionary mapping intent names to intent data
        """

        with open(intents_file, "r") as file:
            data = json.load(file)
        return {intent["name"]: intent for intent in data["intents"]}

    def set_data(self, data):
        """
        Sets the data to be queried.

        Parameters
        ----------
            data : DataFrame
                a pandas DataFrame containing the data to be queried
        """

        self.data = data

    def process_query(self, query):
        """
        Processes a query and returns the result.

        Parameters
        ----------
            query : str
                a string representing the query

        Returns
        -------
        str
            a string representing the result of the query
        """

        # Identify intent
        result = self.model(query, list(self.intents.keys()))
        intent_name = result["labels"][0]
        intent = self.intents[intent_name]

        if intent_name == "most common visitor type":
            return self.most_common_visitor_type()

        elif intent_name == "most visitors in a minute":
            return self.most_visitors_in_minute()

        elif intent_name == "visitor count with single attribute":
            return self.visitor_count_with_single_attribute(query)

        elif "peak time" in query.lower():
            return self.visitors_during_peak_time(query)

        else:
            return "Sorry, I didn't understand your query."

    def most_common_visitor_type(self):
        """
        Returns the most common visitor type.

        Returns
        -------
        str
            a string representing the most common visitor type
        """

        visitor_types = [
            "Is Male",
            "Is Female",
            "Is Hijab",
            "Is Child",
            "Is Niqab",
            "Has Bag",
        ]
        most_common_type = self.data[visitor_types].sum().idxmax()
        occurrences = self.data[most_common_type].sum()
        return f"The most common visitor type is '{most_common_type}' with {occurrences} occurrences."

    def most_visitors_in_minute(self):
        """
        Returns the minute with the most visitors.

        Returns
        -------
        str
            a string representing the minute with the most visitors
        """

        self.data["minute"] = self.data["Time"].dt.floor("T")
        peak_time = self.data["minute"].value_counts().idxmax()
        visitors_at_peak = self.data["minute"].value_counts().max()
        return f"The minute with the most visitors is {peak_time} with {visitors_at_peak} visitors."

    def visitor_count_with_single_attribute(self, query):
        """
        Returns the count of visitors with a specific attribute.

        Parameters
        ----------
            query : str
                a string representing the query

        Returns
        -------
        str
            a string representing the count of visitors with a specific attribute
        """

        attributes = {
            "hijab": "Is Hijab",
            "female": "Is Female",
            "male": "Is Male",
            "child": "Is Child",
            "niqab": "Is Niqab",
            "bag": "Has Bag",
            "woman": "Is Female",
        }
        for key, value in attributes.items():
            if key in query.lower() or key + "s" in query.lower():
                count = self.data[self.data[value] == 1].shape[0]
                return f"The number of '{key}' visitors is {count}."
        return "Sorry, I couldn't identify the specific attribute."

    def visitors_during_peak_time(self, query):
        """
        Returns the count of visitors with a specific attribute during peak time.

        Parameters
        ----------
            query : str
                a string representing the query

        Returns
        -------
        str
            a string representing the count of visitors with a specific attribute during peak time
        """

        self.data["minute"] = self.data["Time"].dt.floor("T")
        peak_time = self.data["minute"].value_counts().idxmax()
        attribute = None
        if "female" in query.lower() or "woman" in query.lower():
            attribute = "Is Female"
        elif "male" in query.lower():
            attribute = "Is Male"
        elif "hijab" in query.lower():
            attribute = "Is Hijab"
        elif "child" in query.lower():
            attribute = "Is Child"
        elif "niqab" in query.lower():
            attribute = "Is Niqab"
        elif "bag" in query.lower():
            attribute = "Has Bag"

        if attribute:
            count = self.data[
                (self.data["minute"] == peak_time) & (self.data[attribute] == 1)
            ].shape[0]
            return f"The number of visitors with '{attribute}' during peak time ({peak_time}) is {count}."
        else:
            return f"The minute with the most visitors is {peak_time} with {self.data['minute'].value_counts().max()} visitors."
