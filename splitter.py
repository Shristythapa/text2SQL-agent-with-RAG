# def split_text_by_sentence(text, max_length=500):
#     sentences = text.split('. ') 
#     chunks = []
#     current_chunk = ""

#     for sentence in sentences:
#         #check adding new sentence to cruent chunk 
#         if len(current_chunk) + len(sentence) + 1 <= max_length: 
#             #if the size is suitable add it
#             current_chunk += sentence + ". "
#         else:
#             #if the size is not suitable add it to the list of chunks by removing the whitespace
#             chunks.append(current_chunk.strip()) 
#             #start a new chunk
#             current_chunk = sentence + ". " 
    
#     #if there is value left in current chunk after the for loop is completed just append it to the chunks list        
#     if current_chunk:
#         chunks.append(current_chunk.strip())

#     return chunks


def split_text_by_sentence(text, max_length=500):
    sentences = text.split('. ') 
    chunks = []
    current_chunk = ""

    for sentence in sentences:
        current_chunk = sentence
        chunks.append(current_chunk.strip()) 

    return chunks

