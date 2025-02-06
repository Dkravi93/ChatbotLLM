import logging
import re
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from langchain_groq import ChatGroq
import os

logger = logging.getLogger(__name__)
groq_api_key = os.getenv("GROQ_API_KEY")
llm = ChatGroq(groq_api_key=groq_api_key, model_name="gemma2-9b-it")

async def process_query(user_query: str, db: AsyncSession):
    """Process user query using LLM and fetch relevant data from the database."""
    
    try:
        sql_prompt = f"""
        You are an expert SQL assistant with access to a PostgreSQL database.
        The database schema is as follows:

        - Table: products (id, name, brand, price, category, description, supplier_id)
        - Table: suppliers (id, name, contact_info, product_categories)

        Given the following user query:
        "{user_query}"

        Generate a SQL query to retrieve the necessary information.
        Ensure the query is safe and does not delete or modify data.
        """

        llm_sql_response = await llm.ainvoke([{"role": "user", "content": sql_prompt}])
        sql_query = llm_sql_response.content.strip()
        sql_match = re.search(r'```sql(.*?)```', sql_query, re.DOTALL)

        if sql_match:
            sql_query = sql_match.group(1).strip()
        else:
            raise ValueError("SQL query not found in the response.")

        result = await db.execute(text(sql_query))
        query_results = result.all()
        
        summarization_prompt = f"""
        User Query: "{user_query}"

        Below is the structured data retrieved from the database:

        {query_results}

        Please generate a user-friendly response.
        """

        llm_summary_response = await llm.ainvoke([{"role": "user", "content": summarization_prompt}])
        response = llm_summary_response.content.strip()
    
    except Exception as e:
        logger.error(f"Error processing query: {e}")
        response = "I'm unable to process your request at the moment."
    
    return response
