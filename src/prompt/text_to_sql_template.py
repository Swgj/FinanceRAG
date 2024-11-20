from llama_index.core import PromptTemplate
from llama_index.core.prompts.prompt_type import PromptType

text_to_sql_template ="""\
Given an input question, first create a syntactically correct {dialect} \
query to run, then look at the results of the query and return the answer. \
You can order the results by a relevant column to return the most \
interesting examples in the database.

Pay attention to use only the column names that you can see in the schema \
description. Be careful to not query for columns that do not exist. \
Pay attention to which column is in which table. Also, qualify column names \
with the table name when needed. 

IMPORTANT NOTE: make sure to enclose each column name in double quotes ("") \
pay attention to syntax and do not allow syntax errors.

You are required to use the following format, \
each taking one line:

Question: Question here
SQLQuery: SQL Query to run
SQLResult: Result of the SQLQuery
Answer: Final answer here

Only use tables listed below.
{schema}


Question: {query_str}
SQLQuery: \
"""

prompt_template = PromptTemplate(
    text_to_sql_template,
    prompt_type=PromptType.TEXT_TO_SQL,
    )

def get_prompt():
    return prompt_template