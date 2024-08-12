# Query Processing Application

This application is designed to process queries on a dataset using a query processor and a language model. It's built with Python and uses the transformers library for text generation and query processing.

## Prerequisites

- Python
- Pip

## Installation

1. Clone the repository
git clone
2. Navigate to the project directory
cd NLP
3. Install the required dependencies
pip install -r requirements.txt

## Usage

1. Load and process the data:

- `data_loader = DataLoader(file_path='/path/to/dataset')`
- Initializes the DataLoader with the specified dataset file path.

2. Initialize the query processor:

- `query_processor = QueryProcessor('/path/to/intents.json')`
- Sets up the QueryProcessor with the path to the intents JSON file.

3. Initialize the LLM:

- `llm = LLM()`
- Prepares the language model for processing queries.

4. Instantiate the main application:

- `app = MainApplication(data_loader, query_processor, llm)`
- Sets up the main application with the data loader, query processor, and language model.

5. Run queries:

- `response = app.run_query(query)`
- Processes a query and returns the result.

## Example

```python
# Load and process data
data_loader = DataLoader(file_path='/content/Tasks_infotraff/NLP/Intern NLP Dataset.xlsx')
query_processor = QueryProcessor('/content/Tasks_infotraff/NLP/intents.json')

llm = LLM()

# Instantiate the main application
app = MainApplication(data_loader, query_processor, llm)

# Example queries
queries = [
 "How many Famele visited me in my peak time ?",
 "How many Male visited me in my peak time ?",
 "How many Childern visited me in my peak time ?"
]

# Process and print the responses
for query in queries:
 response = app.run_query(query)
 print(response)
