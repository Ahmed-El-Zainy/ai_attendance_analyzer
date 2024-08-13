import pandas as pd
import spacy
from spacy.matcher import Matcher

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
        Parses a user query and returns the matched pattern name.
    execute_query(pattern_name: str) -> str:
        Executes the query based on the matched pattern name and returns the result.
    answer_query(query: str) -> str:
        Processes the query and returns the corresponding answer.
    """

    def __init__(self, file_path: str):
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

    def load_data(self, file_path: str) -> pd.DataFrame:
        """
        Loads the dataset from the specified file path.

        Parameters:
        -----------
        file_path : str
            The path to the CSV file containing visitor data.

        Returns:
        --------
        pd.DataFrame
            The loaded dataframe.
        """
        df = pd.read_csv(file_path)
        print("Dataframe Structure:\n", df.head())  # Display the first few rows for understanding
        return df

    def define_patterns(self) -> None:
        """
        Defines the query patterns for matching user queries.
        Patterns are added to the matcher for recognizing specific queries.
        """
        patterns = [
            [{"LOWER": "minute"}, {"LOWER": "did"}, {"LOWER": "i"}, {"LOWER": "get"}, {"LOWER": "the"}, {"LOWER": "most"}, {"LOWER": "visitors"}],
            [{"LOWER": "who"}, {"LOWER": "is"}, {"LOWER": "my"}, {"LOWER": "most"}, {"LOWER": "common"}, {"LOWER": "visitor"}],
            [{"LOWER": "how"}, {"LOWER": "many"}, {"LOWER": "females"}, {"LOWER": "visited"}, {"LOWER": "me"}],
            [{"LOWER": "how"}, {"LOWER": "many"}, {"LOWER": "females"}, {"LOWER": "visited"}, {"LOWER": "me"}, {"LOWER": "in"}, {"LOWER": "my"}, {"LOWER": "peak"}, {"LOWER": "time"}],
            [{"LOWER": "how"}, {"LOWER": "many"}, {"LOWER": "males"}, {"LOWER": "visited"}, {"LOWER": "me"}, {"LOWER": "in"}, {"LOWER": "my"}, {"LOWER": "peak"}, {"LOWER": "time"}],
            [{"LOWER": "how"}, {"LOWER": "many"}, {"LOWER": "children"}, {"LOWER": "visited"}, {"LOWER": "me"}, {"LOWER": "in"}, {"LOWER": "my"}, {"LOWER": "peak"}, {"LOWER": "time"}],
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

    def parse_query(self, query: str) -> str:
        """
        Parses a user query and returns the matched pattern name.

        Parameters:
        -----------
        query : str
            The user's query as a string.

        Returns:
        --------
        str
            The name of the matched pattern or None if no match is found.
        """
        doc = self.nlp(query)
        matches = self.matcher(doc)
        if matches:
            match_id, start, end = matches[0]
            pattern_name = self.nlp.vocab.strings[match_id]  # Get the pattern name
            return pattern_name
        return None

    def execute_query(self, pattern_name: str) -> str:
        """
        Executes the query based on the matched pattern name and returns the result.

        Parameters:
        -----------
        pattern_name : str
            The name of the matched pattern.

        Returns:
        --------
        str
            The result of the query execution.
        """
        print("Matched Query:", pattern_name)  # Debugging line to see matched query

        if pattern_name == "most_visitors_minute":
            result = self.df.groupby(["Minute"]).size().idxmax()
            return f"The minute with the most visitors is: {result}"

        if pattern_name == "most_common_visitor":
            result = self.df["Total_Visitors"].mode()[0]
            return f"The most common visitor is: {result}"

        if pattern_name == "females_visited":
            result = self.df["Is Female"].sum()
            return f"The number of females who visited is: {result}"

        if pattern_name == "females_peak_time":
            peak_time = self.df.groupby("Hour")["Total_Visitors"].sum().idxmax()
            result = self.df[(self.df["Hour"] == peak_time) & (self.df["Is Female"] == 1)].shape[0]
            return f"The number of females who visited during peak time is: {result}"

        if pattern_name == "males_peak_time":
            peak_time = self.df.groupby("Hour")["Total_Visitors"].sum().idxmax()
            result = self.df[(self.df["Hour"] == peak_time) & (self.df["Is Male"] == 1)].shape[0]
            return f"The number of males who visited during peak time is: {result}"

        if pattern_name == "children_peak_time":
            peak_time = self.df.groupby("Hour")["Total_Visitors"].sum().idxmax()
            result = self.df[(self.df["Hour"] == peak_time) & (self.df["Is Child"] == 1)].shape[0]
            return f"The number of children who visited during peak time is: {result}"

        return "Query not recognized. Please ask another question."

    def answer_query(self, query: str) -> str:
        """
        Processes the query by parsing it and executing the appropriate logic.

        Parameters:
        -----------
        query : str
            The user's query as a string.

        Returns:
        --------
        str
            The answer to the user's query.
        """
        pattern_name = self.parse_query(query)
        if pattern_name:
            return self.execute_query(pattern_name)
        else:
            return "Query not recognized. Please ask another question."

def main():
    """
    Main function to initialize the QueryProcessor and process a set of example queries.
    """
    # Initialize QueryProcessor with the dataset file path
    file_path = "/Users/ahmedmostafa/Downloads/Tasks_infotraff-1/NLP/Data/Data.csv"
    processor = QueryProcessor(file_path)

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
        answer = processor.answer_query(query)
        print(answer)

if __name__ == "__main__":
    main()