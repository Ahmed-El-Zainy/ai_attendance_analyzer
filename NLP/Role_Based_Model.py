import pandas as pd
import spacy
from spacy.matcher import Matcher

# Load Spacy model
# nlp = spacy.load('en_core_web_sm')

# Load the dataset
df = pd.read_csv('Data.csv')

# Display the first few rows of the dataframe to understand its structure
print("Dataframe Structure:\n", df.head())
def query_data(query):
    # Preprocess the query (optional): Handle synonyms, stop words, etc.
    words = query.lower().split()

    # Handle multiple questions
    questions = []
    current_question = ""
    for word in words:
        if word in ["what", "which", "how", "who"]:
            if current_question:
                questions.append(current_question)
            current_question = word
        else:
            current_question += " " + word
    if current_question:
        questions.append(current_question)

    # Process each question
    answers = []
    for question in questions:
        if "most visitors" in question:
            # minute = df['Minute'].value_counts().idxmax()
            minute = df.loc[df['Total_Visitors'] == df['Total_Visitors'].max(), 'Minute'].tolist()
            answer = f"The minute with the most visitors is {minute}."
        elif "most common visitor" in question:
            gender_counts = df[['Is Male', 'Is Female', 'Is Child']].sum()
            most_common = gender_counts.idxmax()
            answer = f"The most common visitor is {most_common.replace('_', ' ')}."
        else:
            answer = "I couldn't understand that question."
        answers.append(answer)
    return answers

if __name__ == "__main__":
    query = "Which minute did I get the most visitors? Who is my most common visitor?"
    answers = query_data(query)
    print(answers)
