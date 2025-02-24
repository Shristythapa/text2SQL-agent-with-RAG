
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from langchain_community.utilities import SQLDatabase 


# Load environment variables
load_dotenv()
openai_api_key = os.getenv("MISTRAL_API_KEY")
DB_URL = os.getenv("DB_URL")

# Define SQL query execution tool
def execute_sql_query(query: str):
    
    """Executes a given SQL query and returns the results."""
    
    try:
        engine = create_engine(DB_URL, echo=False)
        db = SQLDatabase(engine)
        results = db._execute(query)
        return results
    
    except Exception as e:
        #print(f"SQL Error: {e}")
        return f"Error: {e}"
