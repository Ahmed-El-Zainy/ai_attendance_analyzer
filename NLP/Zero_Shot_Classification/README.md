# Query Processing Application

This Python application processes queries on a dataset using a custom query processor and a language model. The project is designed to handle various natural language queries about visitor data and provides insights based on the dataset.

## Project Structure

- **`main.py`**: The entry point of the application, where the data is loaded, the query processor is initialized, and example queries are run.
- **`utils.py`**: Handles loading and processing of the dataset.
- **`query_processor.py`**: Manages intent recognition and query processing.
- **`pipeline`**: Wraps the language model used for understanding and processing queries.
- **`main_application.py`**: Integrates the data loader, query processor, and language model to handle queries end-to-end.

## Prerequisites

- Python 3.x
- Pip

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/A7medM0sta/Tasks_infotraff.git
   ```

2. **Navigate to the project directory:**

   ```bash
   cd NLP/Zero_Shot_Classification
   ```

3. **Install the required dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Load and process the data:**

   ```python
   data_loader = DataLoader(file_path='/path/to/dataset')
   ```

   - Initializes the `DataLoader` with the specified dataset file path.

2. **Initialize the query processor:**

   ```python
   query_processor = QueryProcessor('/path/to/intents.json')
   ```

   - Sets up the `QueryProcessor` with the path to the intents JSON file.

3. **Initialize the language model (LLM):**

   ```python
   llm = LLM()
   ```

   - Prepares the language model for processing queries.

4. **Instantiate the main application:**

   ```python
   app = MainApplication(data_loader, query_processor, llm)
   ```

   - Sets up the main application with the data loader, query processor, and language model.

5. **Run queries:**

   ```python
   response = app.run_query(query)
   ```

   - Processes a query and returns the result.

## Example

```python

    # Load and process data
    data_loader = DataLoader(
        file_path="/content/Tasks_infotraff/NLP/Data/Intern NLP Dataset.xlsx"
    )
    query_processor = QueryProcessor("/content/Tasks_infotraff/NLP/Data/intents.json")

    # Initialize the language model
    llm = LLM()

    # Instantiate the main application
    app = MainApplication(data_loader, query_processor, llm)

    # Example queries
    queries = [
        "Who is my most common visitor ?",
        "What time did I get most visits ?",
        "How many females visited me ?",
        "How many females visited me in my peak time?",
        "How many males visited me in my peak time?",
        "How many children visited me in my peak time?",
    ]

    # Process and print the responses
    for query in queries:
        response = app.run_query(query)
        print(response)

# Process and print the responses
for query in queries:
    response = app.run_query(query)
    print(response)
```

## Example Output

The application processes the queries and provides the following output:

- The most common visitor is Female.
- Sorry, I couldn't identify the specific attribute.
- The number of visitors wearing a 'hijab' is 32.
- The number of 'female' visitors is 52.
- The peak visit time is at 15:12:00 on 2024-07-17, with a total of 5 visitors.
- During the peak time, the number of 'Male' visitors is 0.
- During the peak time, the number of 'Child' visitors is 0.