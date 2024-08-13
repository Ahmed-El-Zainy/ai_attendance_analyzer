# Deep Dive into PandasAI

![PandasAI](/NLP/Figures/logo.png)

==========================================================================


## Overview

Introduction to PandasAI
PandasAI is a Python library that makes it easy to ask questions to your data in natural language.
Beyond querying, PandasAI offers functionalities to visualize data through graphs, cleanse datasets by addressing missing values, and enhance data quality through feature generation, making it a comprehensive tool for data scientists and analysts.
## Chatting with PandasAI
Large Language Models
PandasAI supports several large language models (LLMs) that are used to generate code from natural language queries.
BambooLLM

BambooLLM is the state-of-the-art language model developed by PandasAI with data analysis in
 mind. It is designed to understand and execute natural language queries related to data analysis, data manipulation, and
 data visualization. You can get your free API key signing up at https://pandabi.ai
### SmartDataframe
SmartDataframe is a Pandas DataFrame with a BambooLLM agent attached to it. It allows you to chat with the agent to query the data in the DataFrame.
Examples:
- Example 1
```python
sdf = SmartDataframe(df)
sdf.chat("Which minute did I get the most visitors. should output the clock in datetime format ?")
```
output:
```
minute with the most visitors is 15:12.'
```
- Example 2
```python
sdf.chat("Who is my most common visitor, Male or Female?")
```
output:
```
'The most common visitor is Female.'
```
- Example 3
```python
sdf.chat("How many hijab visited me ?")
```
output:
```
32
```
- Example 4
```python
sdf.chat("How many females visited me?")
```
output:
```
52
```
- Example 5
```python
sdf.chat("What time did I get most visits ? Intent: Most Visitors in a Minute")
```
output:
```
The number of female visitors at the peak time (15:12:00) is 5.
```



## Train PandasAI
You can train PandasAI to understand your data better and to improve its performance. Training is as easy as calling the train method on the Agent.

There are two kinds of training:

- instructions training
- q/a training

### Instructions Training

Instructions training is used to teach PandasAI how you expect it to respond to certain queries. You can provide generic instructions about how you expect the model to approach certain types of queries, and PandasAI will use these instructions to generate responses to similar queries.

For example, you might want the LLM to be aware that your company’s fiscal year starts in April, or about specific ways you want to handle missing data. Or you might want to teach it about specific business rules or data analysis best practices that are specific to your organization.

To train PandasAI with instructions, you can use the train method on the Agent, as it follows:

The training uses by default the BambooVectorStore to store the training data, and it’s accessible with the API key.

#### Overview
```
 A class to handle chat operations using PandasAI.

    ...

    Attributes
    ----------
    df : DataFrame
        a pandas DataFrame containing the data to be used by the agent
    agent : Agent
        a PandasAI Agent used to train and chat

    Methods
    -------
    train(docs):
        Trains the agent using the provided documents.
    chat(query):
        Uses the agent to generate a response to the provided query.
```

Examples:
```python
chat_agent.train("Most Common Visitor gender, with number of occurrence")
response = chat_agent.chat("Who is my most common gender ?")
print(response)

```
output:
```
The most common gender is Is Female.
```


- Example 1
```python
chat_agent.train("number of visits visits be minute domain")
response = chat_agent.chat("What Time did I get most visits with numerber of visits, minute ")
print(response)
```
output:
```
The most visited minute is 12 with 5 visits.
``` 
- Example 2

```python
chat_agent.train(docs="number of visits of column Is Hijab")
response = chat_agent.chat("How many hijab visited me ?")
print(response)
```
output:
```
32
``` 
- Example 3

```python
response = agent.chat(
    "During which hour of the day did I receive the highest number of visits last week?"
)
print(response)
```
output:
```
The hour with the highest number of visits last week was 14:00.
```

### Q/A Training
Q/A training is used to teach PandasAI the desired process to answer specific questions, enhancing the model’s performance and determinism. One of the biggest challenges with LLMs is that they are not deterministic, meaning that the same question can produce different answers at different times. Q/A training can help to mitigate this issue.

#### Overview

```
A class to handle Q/A operations using PandasAI.

    ...

    Attributes
    ----------
    df : DataFrame
        a pandas DataFrame containing the data to be used by the agent
    agent : Agent
        a PandasAI Agent used to train and chat

    Methods
    -------
    train(query, response_code):
        Trains the agent using the provided query and response code.
    chat(query):
        Uses the agent to generate a response to the provided query.
```

Examples:
- Example 1
```python

qa_agent = PandasAIQA(df)
agent.train(queries=[query], codes=[response_code])

qa_agent.train(query, response_code)
response = qa_agent.chat("What time did I get most visits with number of visits?")
print(response)
```
output:
```
The minute with the most visits is 12 with 5 visits.
```
- Example 2
```python

qa_agent = PandasAIQA(df)
agent.train(queries=[query], codes=[response_code])

qa_agent.train(query, response_code)
response = qa_agent.chat("What hour did I get most visits with number of visits?")
print(response)
```
output:
```
The hour with the most visits is 14 with 39 visits.
```

- Example 3
```python
qa_agent = PandasAIQA(df)
agent.train(queries=[query], codes=[response_code])

qa_agent.train(query, response_code)
response = qa_agent.chat("What date did I get most visits with number of visits?")
print(response)
```
output:
```
The date with the most visits is 2024-07-17 with 57 visits.
```




