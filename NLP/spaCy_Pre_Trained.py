import pandas as pd
import spacy
from spacy.matcher import Matcher

# Load Spacy model
nlp = spacy.load('en_core_web_sm')
# Load the dataset
df = pd.read_csv('Data.csv')

# Display the first few rows of the dataframe to understand its structure
print("Dataframe Structure:\n", df.head())

# Initialize the matcher with the shared vocabulary
matcher = Matcher(nlp.vocab)

# Define patterns for the queries
patterns = [
    [{"LOWER": "minute"}, {"LOWER": "did"}, {"LOWER": "i"}, {"LOWER": "get"}, {"LOWER": "the"}, {"LOWER": "most"},
     {"LOWER": "visitors"}],
    [{"LOWER": "who"}, {"LOWER": "is"}, {"LOWER": "my"}, {"LOWER": "most"}, {"LOWER": "common"}, {"LOWER": "visitor"}]
]

# Add patterns to the matcher
matcher.add("most_visitors_minute", [patterns[0]])
matcher.add("most_common_visitor", [patterns[1]])


def parse_query(query):
    doc = nlp(query)
    matches = matcher(doc)

    if matches:
        match_id, start, end = matches[0]
        matched_span = doc[start:end].text
        return matched_span
    return None


def execute_query(query, matched_span, dataframe):
    print("Matched Query:", matched_span)  # Debugging line to see matched query

    if matched_span == "minute did i get the most visitors":
        result = dataframe.groupby(['Minute']).size().idxmax()
        return f"The minute with the most visitors is: {result}"

    if matched_span == "who is my most common visitor":
        result = dataframe['Total_Visitors'].mode()[0]
        return f"The most common visitor is: {result}"

    return "Query not recognized. Please ask another question."


# Examples of queries
queries = [
    "Which minute did I get the most visitors?",
    "Who is my most common visitor?"
]

for query in queries:
    print(f"Processing query: '{query}'")  # Debugging line to see current query
    matched_span = parse_query(query)
    answer = execute_query(query, matched_span, df)
    print(answer)
