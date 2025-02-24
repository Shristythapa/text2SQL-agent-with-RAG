
import re

def extract_sql_query(text):
    response = text

    sql_pattern = r"(SELECT .*?;|INSERT INTO .*?;|UPDATE .*?;|DELETE FROM .*?;|CREATE TABLE .*?;|DROP TABLE .*?;|ALTER TABLE .*?;|WITH .*?;)"
    
    queries = re.findall(sql_pattern, response, re.IGNORECASE | re.DOTALL)
    #print("main",queries)
    query_string = ""
    for i in queries:
        query_string +=i
    print(f"this is the query string {query_string}")
    return query_string

