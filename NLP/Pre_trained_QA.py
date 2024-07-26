import pandas as pd
from transformers import pipeline

# Load the dataset
df = pd.read_csv("Data.csv")

# Load a pre-trained question-answering pipeline
qa_pipeline = pipeline('question-answering')


# Define a function to handle the natural language query
def answer_query(query, dataframe):
    # Check for specific questions and handle them
    if "most visitors" in query:
        result = dataframe.groupby(['Minute']).size().idxmax()
        return f"The minute with the most visitors is: {result}"

    if "most common visitor" in query:
        result = dataframe['Total_Visitors'].mode()[0]
        return f"The most common visitor is: {result}"

    return "Query not recognized. Please ask another question."


# Examples of queries
queries = [
    "Which minute did I get the most visitors?",
    "Who is my most common visitor?"
]

for query in queries:
    answer = answer_query(query, df)
    print(answer)
