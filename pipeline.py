from utils.context_retriver import retrieve_context
from utils.prompts import format_prompt_for_sql_query, humanize_output_prompt,determine_query_type, format_insert_prompt_for_sql_query, format_delete_prompt_for_sql_query
from utils.db_functions import execute_sql_query
from utils.formtting import extract_sql_query
from utils.running_lllm import run_llm

import pandas as pd

def run_pipeline(question):
    
    #this is where all the queries tried by the system and the query output is stored
    history = {}   
    
    #context is the information about the database 
    context = retrieve_context(question)

    #run llm to determin what type of sql problem user has entred
    query_type = run_llm(determine_query_type(question))
    print(f"determined query type: {query_type}.")
    
    #load different formated prompt according to the prompt type
    prompt = "" 
    if query_type == '"INSERT"':
        prompt = format_insert_prompt_for_sql_query(context,question,history)
        
    elif query_type == '"DELETE"':
        prompt = format_delete_prompt_for_sql_query(context,question,history)
        
    elif "can't process" in query_type:
        return query_type.strip("'\"")
    else:
        prompt = format_prompt_for_sql_query(context, question, history)
        
    #run llm with specilized formatted prompt to get SQL query
    llm_output = run_llm(prompt)
    
    #if error occurs when getting sql query
    if "Error" in llm_output:
        return llm_output
    
    #extract the sql query from model output
    extracted_query = extract_sql_query(llm_output)
    
    #total number of attempts
    attempts = 5
    
    #counting done attempt
    attempt = 0
    
    #the output after executing query
    result = None
    
    #list all the tried queries
    SQL_queries = []

    #while loop to keep executing query untile there is no error
    while attempt < attempts:    
        
        #execute extracted query
        result = execute_sql_query(extracted_query.strip("'\""))
        
        #append executed query
        SQL_queries.append(extracted_query)

        #handling error cases returned when running query in db
        #these stop loop cause when such error occurs there is no way of fixing it
        if isinstance(result, str) and "No SQL Query found" in result:
            return "Sorry, I am not able to generate SQL query for that question. You can try rephrasing the question."
        
        elif isinstance(result, str) and ("insufficient user privileges" in result or "command denied" in result) :
            return "Sorry, I don't have enough permission to execute that request."
        
        elif isinstance(result, str) and "empty" in result:
            return "Sorry, I am not able to generate SQL query for that question. You can try rephrasing the question."
        
        elif isinstance(result, str) and "limit exceeded" in result:
            return "Apologies, but I am currently unable to access the LLM due to rate limits being exceeded. Please try again later."
        
        
        #handling error cases returned when running query in db
        #this continues the loop cause here the problem might be solvable 
        elif isinstance(result, str) and result.startswith("Error:"): 
            
            # insert the latest query and error to history dic
            history[f"executed_query"] = extracted_query
            history[f"error"] = result
            
            # Refine or regenerate the query by re-running the LLM
            prompt = format_prompt_for_sql_query(context, question, history)
            llm_output = run_llm(prompt)    
            extracted_query = extract_sql_query(llm_output) #rerun the loop with new extracted query
        
        #break if no error was found - The Execution Was Successful    
        elif not isinstance(result, str) or not result.startswith("Error:"):
            break
        
        attempt += 1
        
    #if output returned by db is a error    
    if isinstance(result, str) and "Error:" in result:
        
        output = {
          "SQL_queries" : SQL_queries,
          "db_output":  pd.DataFrame(),
          "Summary": humanize_output_prompt(question,result)
        }
        print(f"output result: {output}")
        return output
    
    
    
    #if the database output is too long LLM can't process that data and trying to proces it will just waste resource.     
    if len(result) > 500:
        df_table_output = pd.DataFrame(result)
        output = {
        "SQL_queries" : SQL_queries,
        "db_output": df_table_output if len(result) > 3 else pd.DataFrame(),
        "Summary":"Sorry I am not able to summarize as the output is too long."
         }
        return output
    
    
    summary = run_llm(humanize_output_prompt(question,result))
    print("Result informations: ")
    print(result)
    print(type(result))
    df_table_output = pd.DataFrame(result)
    
    #formatting summary in case error occurced during summary to notficy user that the error was only during summary.
    if "Error" in summary:
        summary = f"During summarizing: {summary} Note that the query generation and execution was successful."
        output = {
        "SQL_queries" : SQL_queries,
        "db_output": df_table_output,
        "Summary":summary
        }
        return output
    
    output = {
        "SQL_queries" : SQL_queries,
        "db_output": df_table_output if len(df_table_output) > 3 else pd.DataFrame(),
        "Summary":summary
    }
    
    print(f"the final output {output}")
    return output
 
# print(run_pipeline("Insert kathmandu of country nepal in city table."))
