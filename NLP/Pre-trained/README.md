# Pre-Training

## Hugging Face Transformers

```
Model Name: distilbert-base-uncased-distilled-squad
```
### Overview
```     A class to process queries related to visitor data using a pre-trained language model.

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
```
### Required Queries
```
# Examples of queries
    queries = [
        "Which minute did I get the most visitors?",
        "Who is my most common visitor?",
        "How many females visited me?",
        "How many females visited me in my peak time?",
        "How many males visited me in my peak time?",
        "How many children visited me in my peak time?",
    ]
```

### Results
```
Processing query: 'Which minute did I get the most visitors?'
The minute with the most visitors is: 12
Processing query: 'Who is my most common visitor?'
The most common visitor is: 2
Processing query: 'How many females visited me?'
Query not recognized. Please ask another question.
Processing query: 'How many females visited me in my peak time?'
The number of females who visited during peak time is: 35
Processing query: 'How many males visited me in my peak time?'
The number of males who visited during peak time is: 3
Processing query: 'How many children visited me in my peak time?'
The number of children who visited during peak time is: 1

```

## SpaCy Library
```
Model Name: en_core_web_sm
```
### overview
```    A class to process queries related to visitor data.

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
        Parses a user query and returns the matched pattern.
    execute_query(query: str, matched_span: str) -> str:
        Executes the query based on the matched pattern and returns the result.
```

### Required Queries
```
# Examples of queries
    queries = [
        "Which minute did I get the most visitors?",
        "Who is my most common visitor?",
        "How many females visited me?",
        "How many females visited me in my peak time?",
        "How many males visited me in my peak time?",
        "How many children visited me in my peak time?",
    ]
```

### Results
```
Processing query: 'Which minute did I get the most visitors?'
Matched Query: most_visitors_minute
The minute with the most visitors is: 12
Processing query: 'Who is my most common visitor?'
Matched Query: most_common_visitor
The most common visitor is: 2
Processing query: 'How many females visited me?'
Matched Query: females_visited
The number of females who visited is: 52
Processing query: 'How many females visited me in my peak time?'
Matched Query: females_visited
The number of females who visited is: 52
Processing query: 'How many males visited me in my peak time?'
Matched Query: males_peak_time
The number of males who visited during peak time is: 3
Processing query: 'How many children visited me in my peak time?'
Matched Query: children_peak_time
The number of children who visited during peak time is: 1
```


