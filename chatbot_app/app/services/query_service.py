import logging
import re
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from langchain_groq import ChatGroq
from app.services.chat_memory import ChatMemory
import os
import traceback

logger = logging.getLogger(__name__)
groq_api_key = os.getenv("GROQ_API_KEY")
llm = ChatGroq(groq_api_key=groq_api_key, model_name="gemma2-9b-it")

async def process_query(user_id: int, user_query: str, db: AsyncSession, chat_memory: ChatMemory):
    """Process user query using LLM and fetch relevant data from the database, considering recent chat history."""
    try:
        try:
            logger.info("Fetching recent queries for user_id: %s", user_id)
            recent_queries = await chat_memory.get_recent_queries(user_id, limit=5)
            logger.info("Fetched recent queries: %s", recent_queries)
        except Exception as e:
            logger.error("Error fetching recent queries: %s", str(e), exc_info=True)
            recent_queries = []
        # Fetch last 5 user queries from chat history
        
        sql_prompt = f"""
        You are an expert SQL assistant with access to a PostgreSQL database.
        The database schema is as follows:

        - Table: products (id, name, brand, price, category, description, supplier_id)
        - Table: suppliers (id, name, contact_info, product_categories)

        Given the following user query:
        "{user_query}"

        Here is the user's recent search history:
        {recent_queries}

        Generate a SQL query that retrieves the **most relevant** information based on the **current query and past searches**.
        Ensure the query is safe and does not delete or modify data.
        """

        # Generate SQL query using LLM
        llm_sql_response = await llm.ainvoke([{"role": "user", "content": sql_prompt}])
        sql_query = llm_sql_response.content.strip()
        sql_match = re.search(r'```sql(.*?)```', sql_query, re.DOTALL)

        if sql_match:
            sql_query = sql_match.group(1).strip()
        else:
            raise ValueError("SQL query not found in the response.")

        # Execute the SQL query
        result = await db.execute(text(sql_query))
        query_results = result.all()

        # Generate a user-friendly response using chat history
        summarization_prompt = f"""
            You are a helpful and friendly assistant providing responses to user queries.

            User Query: "{user_query}"

            User's Recent Queries:
            {recent_queries}

            Below is the structured data retrieved from the database:
            {query_results}

            Please generate a **natural, user-friendly response** that:
            - Uses prior queries for **better context**.
            - Explains the information **clearly**.
            - Uses a **conversational and engaging tone**.
            - Avoids technical jargon unless necessary.
            - If multiple results exist, summarize them concisely.
            - If no data is found, provide a polite and helpful message.

            Make sure the response sounds natural and human-like.
            """

        llm_summary_response = await llm.ainvoke([{"role": "user", "content": summarization_prompt}])
        response = llm_summary_response.content.strip()

    except Exception as e:
        logger.error(f"Error processing query: {e}")
        logger.error(traceback.format_exc())
        response = "I'm unable to process your request at the moment."
    
    return response


