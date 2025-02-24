from chromadb import PersistentClient
import numpy as np
import torch
from sentence_transformers import util
# Load embedder


from sentence_transformers import SentenceTransformer, SimilarityFunction


model = SentenceTransformer("all-MiniLM-L6-v2")
model.similarity_fn_name = SimilarityFunction.COSINE

#print(model.similarity_fn_name) 


# Connect to Chroma
vectordb = PersistentClient(path="./retail_vector_db")

# def retrieve_context(question, threshold=0.25):
#     # Embed the input question
#     question_embedding = model.encode([question])

#     # Get collection first
#     collection = vectordb.get_collection(name="langchain")

#     # Retrieve all embeddings and documents
#     all_data = collection.get(include=['embeddings', 'documents'])
    

#     stored_embeddings = np.array(all_data['embeddings'])
#     stored_documents = all_data['documents']
    
#     # Convert to PyTorch tensors
#     question_embedding = torch.tensor(question_embedding, dtype=torch.float32)
#     stored_embeddings = torch.tensor(stored_embeddings, dtype=torch.float32)

#     # Compute cosine similarity
#     # similarities = util.cos_sim(question_embedding, stored_embeddings)
    
#     relevant_contexts = []
    
#     for i in range(0,len(stored_embeddings)):
#         s_score = util.cos_sim(question_embedding,stored_embeddings[i])
#         if s_score>threshold:
#             relevant_contexts.append(stored_documents[i])

#     # # Filter results based on threshold
#     # relevant_indices = np.where(similarities >= threshold)[0]
    
#     # # Retrieve matching documents
#     # relevant_contexts = [stored_documents[i] for i in relevant_indices]

#     return relevant_contexts

def retrieve_context(question):
    # Embed the input question
    question_embedding = model.encode([question])

    # Get collection first
    collection = vectordb.get_collection(name="langchain")

    # Retrieve all embeddings and documents
    all_data = collection.get(include=['embeddings', 'documents'])

    stored_embeddings = np.array(all_data['embeddings'])
    stored_documents = all_data['documents']

    # Convert to PyTorch tensors
    question_embedding = torch.tensor(question_embedding, dtype=torch.float32)
    stored_embeddings = torch.tensor(stored_embeddings, dtype=torch.float32)

    # Compute cosine similarity
    similarities = util.cos_sim(question_embedding, stored_embeddings)
    
    scores = []
    for i in range(0, len(stored_embeddings)):
        s_score = util.cos_sim(question_embedding, stored_embeddings[i])
        # Store the first 3 words of the document and the similarity score
        scores.append((' '.join(stored_documents[i].split()[:3]), s_score))

    # Sort the scores by similarity score in descending order
    sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)

    # Print the sorted results
    # for doc, score in sorted_scores:
    #     print(f"{doc}: {score}")

    # Get top k most similar documents
    top_k_indices = similarities[0].topk(5).indices.tolist()

    relevant_contexts = [stored_documents[i] for i in top_k_indices]

    return relevant_contexts

# print(retrieve_context(
#     """In which store was customer with email 'MARY.SMITH@sakilacustomer.org' 
#     registered in? Provide the address of the store and provide all the flims the user has rented name the actors of the movie too."""))

# print(retrieve_context("how many customers are there in the system?"))