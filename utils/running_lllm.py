import httpx
from langchain_mistralai import ChatMistralAI
import os
from dotenv import load_dotenv


load_dotenv()
print(os.path.exists(".env"))  
api_key = os.getenv("MISTRAL_API_KEY")

print(f"Mistral api key {api_key}")
llm = ChatMistralAI(
    model="pixtral-12b-2409",
    temperature=0,
    max_retries=2,
    api_key= api_key,
    timeout=30
)

def run_llm(formatted_prompt):
    """This function runs the LLM with the inputed prompt

    Args:
        formatted_prompt (prompt): this is the prompt

    Returns:
        string : string can be error or model output 
    """
    print(f"this is the prompt being used {formatted_prompt}")
    try:
        response = llm.invoke(formatted_prompt)
        
        if hasattr(response, 'content'):
            return response.content  
        
        return f"Error: Unexpected response format. Response did not contain 'content'."
        
    except httpx.HTTPStatusError as e:
        try:
            error_json = e.response.json()  
            error_message = error_json.get("message", "Unknown error")

            if e.response.status_code == 429:
                return "Error: Requests rate limit exceeded. Please try again later."

            if "too large for model" in error_message:
                return "Error: Requests rate limit exceeded. Please try again later, break down the input."

            return f"Error: {e.response.status_code} - {error_message}"

        except Exception:
            return f"Error: {e.response.status_code} - {e.response.text}"

    
    except Exception as e:
        return f"Error: {str(e)}"




