import pandas as pd
import spacy
from spacy.matcher import Matcher
from Preprocessing import main

class QueryProcessor:
    """
    A class to process queries related to visitor data.

    Attributes:
    -----------
    df : pd.DataFrame
        The dataframe containing visitor data.
    matcher : spacy.matcher.Matcher
        A matcher object to find specific query patterns.

    Methods:
    --------
    load_data(file_path: str) -> pd.DataFrame:
        Loads the dataset from the specified file path.
    define_patterns() -> None:
        Defines the query patterns for matching.
    parse_query(query: str) -> str:
        Parses a user query and returns the matched pattern.
    execute_query(query: str, matched_span: str) -> str:
        Executes the query based on the matched pattern and returns the result.
    """

    def __init__(self, file_path):
        """
        Initializes the QueryProcessor with the given dataset file path.

        Parameters:
        -----------
        file_path : str
            The file path to the dataset.
        """
        self.df = self.load_data(file_path)
        self.nlp = spacy.load("en_core_web_sm")
        self.matcher = Matcher(self.nlp.vocab)
        self.define_patterns()

    def load_data(self, file_path):
        """Loads the dataset from the specified file path."""
        df = pd.read_csv(file_path)
        print(
            "Dataframe Structure:\n", df.head()
        )  # Display the first few rows for understanding
        return df

    def define_patterns(self):
        """Defines the query patterns for matching."""
        patterns = [
            [
                {"LOWER": "minute"},
                {"LOWER": "did"},
                {"LOWER": "i"},
                {"LOWER": "get"},
                {"LOWER": "the"},
                {"LOWER": "most"},
                {"LOWER": "visitors"},
            ],
            [
                {"LOWER": "who"},
                {"LOWER": "is"},
                {"LOWER": "my"},
                {"LOWER": "most"},
                {"LOWER": "common"},
                {"LOWER": "visitor"},
            ],
            [
                {"LOWER": "how"},
                {"LOWER": "many"},
                {"LOWER": "females"},
                {"LOWER": "visited"},
                {"LOWER": "me"},
            ],
            [
                {"LOWER": "how"},
                {"LOWER": "many"},
                {"LOWER": "females"},
                {"LOWER": "visited"},
                {"LOWER": "me"},
                {"LOWER": "in"},
                {"LOWER": "my"},
                {"LOWER": "peak"},
                {"LOWER": "time"},
            ],
            [
                {"LOWER": "how"},
                {"LOWER": "many"},
                {"LOWER": "males"},
                {"LOWER": "visited"},
                {"LOWER": "me"},
                {"LOWER": "in"},
                {"LOWER": "my"},
                {"LOWER": "peak"},
                {"LOWER": "time"},
            ],
            [
                {"LOWER": "how"},
                {"LOWER": "many"},
                {"LOWER": "children"},
                {"LOWER": "visited"},
                {"LOWER": "me"},
                {"LOWER": "in"},
                {"LOWER": "my"},
                {"LOWER": "peak"},
                {"LOWER": "time"},
            ],
        ]
        pattern_names = [
            "most_visitors_minute",
            "most_common_visitor",
            "females_visited",
            "females_peak_time",
            "males_peak_time",
            "children_peak_time",
        ]

        for name, pattern in zip(pattern_names, patterns):
            self.matcher.add(name, [pattern])

    def parse_query(self, query):
        """Parses a user query and returns the matched pattern."""
        doc = self.nlp(query)
        matches = self.matcher(doc)
        if matches:
            match_id, start, end = matches[0]
            matched_span = doc[start:end].text
            return matched_span
        return None

    def execute_query(self, query, matched_span):
        """Executes the query based on the matched pattern and returns the result."""
        print("Matched Query:", matched_span)  # Debugging line to see matched query

        if matched_span == "minute did i get the most visitors":
            result = self.df.groupby(["Minute"]).size().idxmax()
            return f"The minute with the most visitors is: {result}"

        if matched_span == "who is my most common visitor":
            result = self.df["Total_Visitors"].mode()[0]
            return f"The most common visitor is: {result}"

        if matched_span == "how many females visited me":
            result = self.df["Is Female"].sum()
            return f"The number of females who visited is: {result}"

        if matched_span == "how many females visited me in my peak time":
            peak_time = self.df.groupby("Hour")["Total_Visitors"].sum().idxmax()
            result = self.df[
                (self.df["Hour"] == peak_time) & (self.df["Is Female"] == 1)
            ].shape[0]
            return f"The number of females who visited during peak time is: {result}"

        if matched_span == "how many males visited me in my peak time":
            peak_time = self.df.groupby("Hour")["Total_Visitors"].sum().idxmax()
            result = self.df[
                (self.df["Hour"] == peak_time) & (self.df["Is Male"] == 1)
            ].shape[0]
            return f"The number of males who visited during peak time is: {result}"

        if matched_span == "how many children visited me in my peak time":
            peak_time = self.df.groupby("Hour")["Total_Visitors"].sum().idxmax()
            result = self.df[
                (self.df["Hour"] == peak_time) & (self.df["Is Child"] == 1)
            ].shape[0]
            return f"The number of children who visited during peak time is: {result}"

        return "Query not recognized. Please ask another question."


def main():
    # Initialize QueryProcessor with the dataset
    df = main()
    processor = QueryProcessor(df)

    # Examples of queries
    queries = [
        "Which minute did I get the most visitors?",
        "Who is my most common visitor?",
        "How many females visited me?",
        "How many females visited me in my peak time?",
        "How many males visited me in my peak time?",
        "How many children visited me in my peak time?",
    ]

    for query in queries:
        print(f"Processing query: '{query}'")  # Debugging line to see current query
        matched_span = processor.parse_query(query)
        if matched_span:
            answer = processor.execute_query(query, matched_span)
        else:
            answer = "No matching pattern found for the query."
        print(answer)


if __name__ == "__main__":
    main()
