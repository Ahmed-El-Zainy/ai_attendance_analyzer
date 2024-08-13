import pandas as pd
from transformers import pipeline

class QueryProcessorWithLLM:
    """
    A class to process queries related to visitor data using a pre-trained language model.

    Attributes:
    -----------
    df : pd.DataFrame
        The dataframe containing visitor data.
    qa_pipeline : transformers.pipelines.pipeline
        A pre-trained question-answering pipeline.

    Methods:
    --------
    load_data(file_path: str) -> pd.DataFrame:
        Loads the dataset from the specified file path.
    answer_query(query: str) -> str:
        Processes a user query and returns the result.
    """

    def __init__(self, file_path):
        """
        Initializes the QueryProcessorWithLLM with the given dataset file path.

        Parameters:
        -----------
        file_path : str
            The file path to the dataset.
        """

        model_name = "distilbert-base-cased-distilled-squad"
        self.df = self.load_data(file_path)
        self.qa_pipeline = pipeline("question-answering", model=model_name)

    def load_data(self, file_path):
        """Loads the dataset from the specified file path."""
        try:
            df = pd.read_csv(file_path)
            print("Dataframe Structure:\n", df.head())  # Display the first few rows
            return df
        except FileNotFoundError:
            print(f"Error: The file at {file_path} was not found.")
            return None

    def answer_query(self, query):
        """Processes a user query and returns the result."""
        # Check if data is loaded
        if self.df is None:
            return "No data loaded."

        # Check for specific questions and handle them
        if "minute" in query and "most visitors" in query:
            result = self.df.groupby(["Minute"]).size().idxmax()
            return f"The minute with the most visitors is: {result}"

        if "common visitor" in query:
            result = self.df["Total_Visitors"].mode()[0]
            return f"The most common visitor is: {result}"

        if "how many females visited" in query and "peak time" not in query:
            result = self.df["Is Female"].sum()
            return f"The number of females who visited is: {result}"

        if "females visited" in query and "peak time" in query:
            peak_time = self.df.groupby("Hour")["Total_Visitors"].sum().idxmax()
            result = self.df[
                (self.df["Hour"] == peak_time) & (self.df["Is Female"] == 1)
            ].shape[0]
            return f"The number of females who visited during peak time is: {result}"

        if "males visited" in query and "peak time" in query:
            peak_time = self.df.groupby("Hour")["Total_Visitors"].sum().idxmax()
            result = self.df[
                (self.df["Hour"] == peak_time) & (self.df["Is Male"] == 1)
            ].shape[0]
            return f"The number of males who visited during peak time is: {result}"

        if "children visited" in query and "peak time" in query:
            peak_time = self.df.groupby("Hour")["Total_Visitors"].sum().idxmax()
            result = self.df[
                (self.df["Hour"] == peak_time) & (self.df["Is Child"] == 1)
            ].shape[0]
            return f"The number of children who visited during peak time is: {result}"

        return "Query not recognized. Please ask another question."

def main():
    # Initialize QueryProcessorWithLLM with the dataset file path
    file_path = "/Users/ahmedmostafa/Downloads/Tasks_infotraff-1/NLP/Data/Data.csv"
    processor = QueryProcessorWithLLM(file_path)

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