"""
main.py

This script serves as the entry point for processing visitor data and handling natural language
queries. It loads the necessary data, initializes the required components, and processes
a set of example queries to demonstrate its functionality.

## Components:
1. DataLoader: Loads and preprocesses visitor data from an Excel file.
2. QueryProcessor: Handles natural language queries based on predefined intents.
3. LLM: A language model used for understanding and processing queries.
4. MainApplication: The central application that integrates all components and manages
   the query processing workflow.
"""
from data_loader import DataLoader
from query_processor import QueryProcessor
from pipeline import LLM
from main_application import MainApplication


def main():
    """
    Main function to load data, process queries and print responses.

    This function creates instances of DataLoader, QueryProcessor, LLM, and MainApplication.
    It then runs a set of example queries and prints the responses.
    """

    # Load and process data
    data_loader = DataLoader(
        file_path="/content/Tasks_infotraff/NLP/Intern NLP Dataset.xlsx"
    )
    query_processor = QueryProcessor("/content/Tasks_infotraff/NLP/intents.json")

    # Initialize the language model
    llm = LLM()

    # Instantiate the main application
    app = MainApplication(data_loader, query_processor, llm)

    # Example queries
    queries = [
        "How many females visited me in my peak time?",
        "How many males visited me in my peak time?",
        "How many children visited me in my peak time?",
    ]

    # Process and print the responses
    for query in queries:
        response = app.run_query(query)
        print(response)


if __name__ == "__main__":
    main()
