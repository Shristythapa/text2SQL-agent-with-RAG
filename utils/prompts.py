from langchain.prompts import PromptTemplate

def format_prompt_for_sql_query(contexts: str, query: str, history:dict) -> str:
    prompt_template = PromptTemplate(
        input_variables=["query", "contexts","history"],
        template=
        
        """
        You are a helpful assistant who creates SQL queries for MySQL database based on the given schema description.
        If the question cannot be answered using the provided information, say "I don't have that information."
        Note that column and table names are written like this - `flim` in the context which should match in the query.
        Incase history is provided with error consider past mistake to provide the correct answer.
        Only retrive necessary columns try to make it minimal.
        - If only a list of data is provided without an instruction, respond with: "I can't process this without a specific instruction."
        Ensure the output format strictly follows: 
        SQL Query: SELECT ...
        
        Examples:
        User Query: "Get data of movies of actor 'PENELOPE' that the customer with the email 'MARY.SMITH@sakilacustomer.org' has watched."
        SQL Query: SELECT * FROM `film` JOIN `film_actor` ON `film`.`film_id` = `film_actor`.`film_id` JOIN `actor` ON `film_actor`.`actor_id` = `actor`.`actor_id` JOIN `rental` ON `film`.`film_id` = `rental`.`inventory_id` JOIN `customer` ON `rental`.`customer_id` = `customer`.`customer_id` WHERE `actor`.`first_name` = 'PENELOPE' AND `customer`.`email` = 'MARY.SMITH@sakilacustomer.org';
      
        User Query: "Get all the customers who rented the movie 'ACADEMY DINOSAUR'."
        SQL Query: SELECT `customer`.* FROM `customer` JOIN `rental` ON `customer`.`customer_id` = `rental`.`customer_id` JOIN `inventory` ON `rental`.`inventory_id` = `inventory`.`inventory_id` JOIN `film` ON `inventory`.`film_id` = `film`.`film_id` WHERE LOWER(`film`.`title`) = LOWER('ACADEMY DINOSAUR');
        
        User Query: "Get the list of staff members working at the store 'Store 1'."
        SQL Query: SELECT `staff`.* FROM `staff` JOIN `store` ON `staff`.`store_id` = `store`.`store_id` WHERE `store`.`store_id` = 1;
        
        Schema: {contexts}
        User Query: {query}
        History: {history}
        SQL Query: 
        """
    )
    
    formatted_prompt = prompt_template.format(query=query, contexts=contexts,history=history)
    return formatted_prompt

def humanize_output_prompt(question: str, query_result: str):
    humanize_prompt = PromptTemplate(
        input_variables=["question", "query_result"],
        template="""
            You are a helpful assistant that **summarizes** database results and provides useful **insights**.
            If the query executes successfully:
            - Provide a clear and concise summary of the results.
            - Focus on key insights rather than listing all details unless absolutely necessary.
            - Do **not** list long tables, rows, or columns. Provide summaries instead.
            - Respond as if you are answering the question directly from the database.
            - Do **not** include phrases like "let me know if you have more questions" or "feel free to ask more."
            - Do **not** include any notes or meta information like "This is a summary."

            If there is an error:
            - Explain the error in simple terms, without suggesting solutions or speculating.
            - Examples:
                - "Database connection error" → "I can't connect to the database right now."
                - "Syntax error near 'FROM'" → "There's an issue with the SQL syntax."

            For statements like INSERT, DELETE, or UPDATE:
            - Confirm that the task has been executed successfully.

            Input Information:
                Question: {question}
                Query Result: {query_result}
                
            Summarized Answer:
            """
    )
    
    formatted_prompt = humanize_prompt.format(question=question, query_result=query_result)
    return formatted_prompt 


def determine_query_type(user_query: str):
    prompt_template = PromptTemplate(
        input_variables=["user_query"],
        template="""
        You are a helpful assistant that determines the type of SQL query based on the user's natural language query. 
        Given the user's query, determine whether it corresponds to an `INSERT`, `DELETE`, `UPDATE`, or `SELECT` operation. 
        Do not explain or provide extra information, only return the corresponding operation type.
        - If only a list of data is provided without an instruction, respond with: "I can't process this without a specific instruction."
        **Instructions:**
        - If the query requires adding data, return "INSERT".
        - If the query requires removing data, return "DELETE".
        - If the query requires modifying existing data, return "UPDATE".
        - If the query requires retrieving data, return "SELECT".

        **Example Input and Output:**

        Input: "add Kathmandu to city"
        Output: "INSERT"

        Input: "remove user Mike"
        Output: "DELETE"

        Input: "update user Mike's email to mike@example.com"
        Output: "UPDATE"

        Input: "get all user emails"
        Output: "SELECT"

        Input: "{user_query}"
        Output:
        """
    )

    formatted_prompt = prompt_template.format( user_query=user_query)
    return formatted_prompt 

def format_insert_prompt_for_sql_query(contexts: str, query: str, history: dict) -> str:
    prompt_template = PromptTemplate(
        input_variables=["query", "contexts", "history"],
        template= 
        """
        You are a helpful assistant who creates SQL `INSERT` queries for MySQL database based on the given schema description.
        If the question cannot be answered using the provided information, say "I don't have that information."
        Note that column and table names are written like this - `flim` in the context which should match in the query.
        Incase history is provided with an error, consider past mistakes to provide the correct answer.
        Only insert necessary columns, try to make it minimal.
        - If only a list of data is provided without an instruction, respond with: "I can't process this without a specific instruction."
        Ensure the output format strictly follows:
        SQL Query: INSERT INTO ...

        Examples:
        User Query: "Add a new movie with title 'NEW MOVIE' and release year 2025."
        SQL Query: INSERT INTO `film` (`title`, `release_year`) VALUES ('NEW MOVIE', 2025);

        User Query: "Insert a new customer with name 'John Doe' and email 'johndoe@example.com'."
        SQL Query: INSERT INTO `customer` (`first_name`, `last_name`, `email`) VALUES ('John', 'Doe', 'johndoe@example.com');

        Schema: {contexts}
        User Query: {query}
        History: {history}
        SQL Query:
        """
    )

    formatted_prompt = prompt_template.format(query=query, contexts=contexts, history=history)
    return formatted_prompt


def format_delete_prompt_for_sql_query(contexts: str, query: str, history: dict) -> str:
    prompt_template = PromptTemplate(
        input_variables=["query", "contexts", "history"],
        template= 
        """
        You are a helpful assistant who creates SQL `DELETE` queries for MySQL database based on the given schema description.
        If the question cannot be answered using the provided information, say "I don't have that information."
        Note that column and table names are written like this - `flim` in the context which should match in the query.
        Incase history is provided with an error, consider past mistakes to provide the correct answer.
        - If only a list of data is provided without an instruction, respond with: "I can't process this without a specific instruction."
        Ensure the output format strictly follows:
        SQL Query: DELETE ...

        Examples:
        User Query: "Delete the customer with email 'johndoe@example.com'."
        SQL Query: DELETE FROM `customer` WHERE `email` = 'johndoe@example.com';

        User Query: "Remove the movie 'OLD MOVIE' from the film database."
        SQL Query: DELETE FROM `film` WHERE `title` = 'OLD MOVIE';

        Schema: {contexts}
        User Query: {query}
        History: {history}
        SQL Query:
        """
    )

    formatted_prompt = prompt_template.format(query=query, contexts=contexts, history=history)
    return formatted_prompt


def format_update_prompt_for_sql_query(contexts: str, query: str, history: dict) -> str:
    prompt_template = PromptTemplate(
        input_variables=["query", "contexts", "history"],
        template= 
     """
        You are a helpful assistant who creates SQL `UPDATE` queries for MySQL database based on the given schema description.
        If the question cannot be answered using the provided information, say "I don't have that information."
        Note that column and table names are written like this - `flim` in the context which should match in the query.
        In case history is provided with an error, consider past mistakes to provide the correct answer.
        Only update necessary columns, try to make it minimal.
        - If only a list of data is provided without an instruction, respond with: "I can't process this without a specific instruction."
        Ensure the output format strictly follows:
        SQL Query: UPDATE ...

        Examples:
        User Query: "Update the title of the movie with id 1 to 'Updated Movie'."
        SQL Query: UPDATE `film` SET `title` = 'Updated Movie' WHERE `id` = 1;

        User Query: "Update the address of the store located in Kathmandu, update the postal code to '44600' and phone number to '9856000000'"
        SQL Query: UPDATE `store` JOIN `address` ON `store`.`address_id` = `address`.`address_id` SET `address`.`postal_code` = '44600', `address`.`phone` = '9856000000' WHERE `address`.`city_id` = (SELECT `city_id` FROM `city` WHERE `city` = 'Kathmandu');

        User Query: "Change the price of the product in store 5 to 19.99, and update the inventory's stock for film ID 30"
        SQL Query: UPDATE `inventory` SET `rental_rate` = 19.99 WHERE `store_id` = 5 AND `film_id` = 30;

        Schema: {contexts}
        User Query: {query}
        History: {history}
        SQL Query:
     """
    )

    formatted_prompt = prompt_template.format(query=query, contexts=contexts, history=history)
    return formatted_prompt