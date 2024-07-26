import pandas as pd
from transformers import pipeline
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import torch

df = pd.read_csv('Data.csv')

# Initialize the zero-shot classification pipeline
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

# Define query types and corresponding DataFrame operations
query_types = {
    "most visitors per minute": "Which minute did I get the most visitors?",
    "most common visitor": "Who is my most common visitor?",
    "count male visitors": "How many males visited?",
    "count female visitors": "How many females visited?",
    "count hijab visitors": "How many visitors wore hijab?",
    "count child visitors": "How many children visited?",
    "count niqab visitors": "How many visitors wore niqab?",
    "count visitors with bags": "How many visitors had a bag?"
}

def classify_query(query):
    # Classify the query type using zero-shot classification
    labels = list(query_types.keys())
    result = classifier(query, labels)
    query_type = result['labels'][0]
    return query_type

def parse_query(query):
    # Classify the query
    query_type = classify_query(query)

    # Initialize empty query result
    result = None

    if query_type == "most visitors per minute":
        result = df.groupby('Minute')['Total_Visitors'].sum().idxmax()
    elif query_type == "most common visitor":
        result = df['Cluster ID'].mode()[0]
    elif query_type == "count male visitors":
        result = df['Is Male'].sum()
    elif query_type == "count female visitors":
        result = df['Is Female'].sum()
    elif query_type == "count hijab visitors":
        result = df['Is Hijab'].sum()
    elif query_type == "count child visitors":
        result = df['Is Child'].sum()
    elif query_type == "count niqab visitors":
        result = df['Is Niqab'].sum()
    elif query_type == "count visitors with bags":
        result = df['Has Bag'].sum()
    else:
        result = "Query not recognized or supported."

    return result

# Handle multiple queries
def handle_queries(queries):
    results = {}
    for query in queries:
        result = parse_query(query)
        results[query] = result
    return results

# Example queries
queries = [
    "Which minute did I get the most visitors?",
    "Who is my most common visitor?",
    "How many males visited?",
    "How many females visited?",
    "How many visitors wore hijab?",
    "How many children visited?",
    "How many visitors wore niqab?",
    "How many visitors had a bag?"
]

# Parse and execute queries
results = handle_queries(queries)
for query, result in results.items():
    print(f"Result for '{query}': {result}")