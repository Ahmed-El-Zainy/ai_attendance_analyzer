# Deep Dive into PandasAI

![PandasAI](/NLP/Figures/logo.png)

==========================================================================


## Overview

Introduction to PandasAI
PandasAI is a Python library that makes it easy to ask questions to your data in natural language.
Beyond querying, PandasAI offers functionalities to visualize data through graphs, cleanse datasets by addressing missing values, and enhance data quality through feature generation, making it a comprehensive tool for data scientists and analysts.

## Train PandasAI
You can train PandasAI to understand your data better and to improve its performance. Training is as easy as calling the train method on the Agent.

There are two kinds of training:

- instructions training
- q/a training

### Instructions Training
Instructions training

Instructions training is used to teach PandasAI how you expect it to respond to certain queries. You can provide generic instructions about how you expect the model to approach certain types of queries, and PandasAI will use these instructions to generate responses to similar queries.

For example, you might want the LLM to be aware that your company’s fiscal year starts in April, or about specific ways you want to handle missing data. Or you might want to teach it about specific business rules or data analysis best practices that are specific to your organization.

To train PandasAI with instructions, you can use the train method on the Agent, as it follows:

The training uses by default the BambooVectorStore to store the training data, and it’s accessible with the API key.
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



