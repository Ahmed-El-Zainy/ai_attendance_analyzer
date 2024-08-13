# Question Answering for CSV file

This project provides a system for exploring and querying visitor data, answering questions like "Who is my most common visitor?" and "When did I get the most visits?" It combines data analysis and natural language processing to provide insights into visitor patterns.

## Architecture

## Overview
```
NLP/
├── cache/
│   ├── cache_db_0.11.db
│   ├── cache_db_0.11.db.wal
├── Data/
│   ├── Data.csv
│   ├── intents.json
│   ├── Intern NLP Dataset.xlsx
├── Drafts/
│   ├── Zero_Shot_Classification_method.ipynb
├── exports/
│   ├── charts/
├── Figures/
│   ├── corr.png
│   ├── logo.png
├── PandasAI/
│   ├── Fine_Tune_Agent_Pandas_AI.ipynb
│   ├── Pandas_AI_Chat.ipynb
│   ├── README.md
│   ├── pandasai.log
├── Pre-trained/
│   ├── Preprocessing.py
│   ├── README.md
│   ├── requirements.txt
│   ├── Role_Based_Model.py
├── Zero_Shot_Classification/
│   ├── main_app.py
│   ├── main.py
│   ├── pipeline.py
│   ├── QA.txt
│   ├── query_processing.py
│   ├── README.md
│   ├── requirements.txt
│   ├── utils.py
```

The application processes a dataset containing visitor information and responds to various queries using Python. It leverages libraries like pandas for data manipulation and transformers for natural language processing (NLP).

## Dataset Description

the original data:

- **Is Male**: time consist of date and hours , minutes and seconds
- **Is Male**: Indicates if the visitor is male.
- **Is Female**: Indicates if the visitor is female.
- **Is Hijab**: Indicates if the visitor is wearing a hijab.
- **Is Child**: Indicates if the visitor is a child.
- **Is Niqab**: Indicates if the visitor is wearing a niqab.
- **Has Bag**: Indicates if the visitor is carrying a bag.
- **Cluster ID**: A unique identifier for each visitor group.

### Additional Data Processing

In this project, further processing was performed on the dataset to extract valuable information from the 'Time' column. This enriched dataset now includes several columns representing various visitor attributes:

- **Is Male**: Indicates if the visitor is male.
- **Is Female**: Indicates if the visitor is female.
- **Is Hijab**: Indicates if the visitor is wearing a hijab.
- **Is Child**: Indicates if the visitor is a child.
- **Is Niqab**: Indicates if the visitor is wearing a niqab.
- **Has Bag**: Indicates if the visitor is carrying a bag.
- **Cluster ID**: A unique identifier for each visitor group.
- **Date**: The date of the visit.
- **Hour**: The hour during which the visit occurred.
- **Minute**: The minute during which the visit occurred.
- **Total Visitors**: The total number of visitors.

## Key Features

**Data Exploration**:

- The application begins by exploring the dataset, displaying its structure to understand the columns and their contents.

- It calculates summary statistics for each column, providing insights into the distribution of visitor attributes.

Plot Correlation:

<img src="Figures/corr.png" alt="Correlation Plot" width="600" height="500"/>

## Correlation Matrix Analysis

### Overview

This section provides insights derived from the correlation matrix of the dataset. Correlation values range between -1 and 1, indicating the strength and direction of the relationship between two variables.

### Key Insights

1. **Gender-Based Observations**:
   - A strong inverse relationship exists between `Is Male` and `Is Female`, as expected in a binary gender classification.
   - Female visitors have a moderate positive correlation with total visitor count, indicating a higher female presence in the dataset.

2. **Visitor Attributes**:
   - Visitors wearing a hijab have a strong positive correlation with total visitors, suggesting that a significant portion of the visitors are hijab-wearing individuals.
   - A moderate inverse relationship exists between female visitors and child visitors.

3. **Bag Presence**:
   - There is a moderate positive correlation between visitors carrying bags and the total number of visitors.

4. **Temporal and Cluster Analysis**:
   - The hour and minute values show a strong inverse relationship, which may reflect specific trends in visitor traffic over time.
   - Cluster IDs are closely tied to specific hours, indicating that visitor distribution varies significantly across different time periods.

#### Conclusion

These correlations provide a foundational understanding of the relationships between various attributes in the dataset, aiding in further analysis and decision-making.

## Getting Started

### Prerequisites

Before you start, ensure you have Python installed on your machine. You’ll also need to install the required packages.

### Installation

1. **Clone the repository**:

    ```bash
    git clone https://github.com/A7medM0sta/Tasks_infotraff.git
    ```

2. **Navigate to the project directory**:

    ```bash
    cd NLP
    ```

3. **Install the dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

### Running the Application
You have many methods to run the application, you can run it from the main.py file or from the main_app.py file or from the notebook file.

#### 1.Zero_Shot_Classification:
you can run the main.py file or the main_app.py file.

```bash
   cd Zero_Shot_Classification 
```
- **From the main.py file**:
    ```bash
    python main.py
    ```
#### 2.Pre-Trained Models:


```bash
   cd Pre-trained
```
- Method 1: spacy library

```bash
    python spaCy_Pre_Trained.py
```

- Method 2: transformers library

```bash
    python Pre_trained_QA.py
```
This will load the dataset, process some example queries, and display the results.


### Required Results
```
Q.Who is my most common visitor ?
A.The most common visitor type is 'Is Female' with 52 occurrences.

Q.What time did I get most visits ?
A.The minute with the most visitors is 2024-07-17 15:12:00 with 5 visitors.

Q.How many hijab visited me ?
A.The number of the specific visitors is 32.

Q.How many females visited me ?
A.The number of the specific visitors is 52.

Q.How many woman visited me in my peak time ?
A.The minute with the most visitors is 2024-07-17 15:12:00 with 5 visitors.

Q.What time did I get most visits with number of visits?
A.The minute with the most visitors is 2024-07-17 15:12:00 with 5 visitors.
```
### MY Results

```
Q.Who is my most common visitor ?
A.The most common visitor is Female..

Q.What time did I get most visits ?
A.'The minute with the most visitors is 15:12.'

Q.How many hijab visited me ?
A.32.

Q.How many females visited me ?
A.52.

Q.How many woman visited me in my peak time ?
A.The number of female visitors at the peak time (15:12:00) is 5

Q.What time did I get most visits with number of visits?
A.The time with the most visits is 15:12:00 with 5 visits.
```
Upon starting, the application loads the dataset and provides an overview of its structure. This step is crucial to understanding what kind of queries can be answered based on the available data.

### Extending the System

The application is designed to be extensible. You can add more patterns to handle different types of queries or improve the existing logic to provide more detailed answers.

## Example Queries

Here are some of the questions the system can answer:

- "Who is my most common visitor?"
- "What time did I get most visits?"
- "How many females visited me?"
- "How many females visited me in my peak time?"
- "How many males visited me in my peak time?"
- "How many children visited me in my peak time?"

## Contributing

Contributions are welcome! If you have suggestions for improvements or new features, feel free to fork the repository and submit a pull request.
