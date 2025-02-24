from langchain.schema import Document
from langchain_community.vectorstores import Chroma
from splitter import split_text_by_sentence
from langchain.embeddings import SentenceTransformerEmbeddings 

with open("./schemadis.txt", "r", encoding="utf-8") as f:
    text = f.read()

chunks = split_text_by_sentence(text=text)

docs = [Document(page_content=chunk) for chunk in chunks]

embedding_model = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2") 



vectordb = Chroma.from_documents(documents=docs, 
                                 embedding=embedding_model, 
                                 persist_directory="./retail_vector_db")
