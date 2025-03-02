# text2SQL-agent

Input - user query in text (eg. how many purchase we had today)

Model Outputs - SQL Query

Output query results in natural language (eg. There were 55 unique purchases today.).

## General Architecture
![General Architecture](https://github.com/user-attachments/assets/581cdcf3-d6c5-4b1e-b477-ba2a231d9150)

## Detailed-Working Architecture
![Model architecture](https://github.com/user-attachments/assets/055722f0-8c8c-4957-a1c2-7eee863cc9aa)

##Tools and methods 

###User Interface
**Streamlit** - Python-based library to build user interfaces specifically designed for machine learning engineers or data scientists.

###Large Language Model
For LLM I am using **Groq** as a model provider as it provides a fast and seamless way of running open-source models. 

###Vector Database
**Chromadb** - Enables efficient storage and retrieval of database schema embeddings, allowing quick access to relevant context for query generation.

###Embedding algorithm
**Sentence transformer**- Converts text (such as schema details and user queries) into high-dimensional vectors which encoding sentence meaning, improving semantic search accuracy.

###Similarity algorithm
**Cosine** -   Measures the similarity between vector representations of queries and database schema. It is particularly effective for text-based similarity tasks because it captures semantic relationships without being affected by the length of the vectors.

###LLM Orchestration
**LangChain **- Used to seamlessly integrate LLMs with external tools, including databases and vector stores, ensuring efficient query generation and execution.

###Database 
**MySQL** - Chosen for its reliability, structured query capabilities

