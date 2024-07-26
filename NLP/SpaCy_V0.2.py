import pandas as pd
import spacy
from transformers import pipeline

# Load the dataset
dataset = pd.read_csv('Data.csv')

# Initialize NLP tools
nlp = spacy.load('en_core_web_sm')
qa_pipeline = pipeline('question-answering')

# Function to process and execute queries
def process_query(query):
    doc = nlp(query)
    # Example: Extract relevant entities and map to operations
    if "most visitors" in query:
        result = dataset.loc[dataset['Total_Visitors'].idxmax(), 'Minute']
        return f"The minute with the most visitors is: {result}"
    elif "most common visitor" in query:
        result = dataset[['Is Male', 'Is Female', 'Is Hijab', 'Is Child', 'Is Niqab', 'Has Bag']].mode().iloc[0]
        return f"The most common visitor characteristics are: {result.to_dict()}"
    else:
        return "Query not recognized."

# Example Queries
print(process_query("Which minute did I get the most visitors?"))
print(process_query("Who is my most common visitor?"))
