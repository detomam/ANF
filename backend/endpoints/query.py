from fastapi import APIRouter

router = APIRouter()

@router.post("/process-query")
async def process_query(payload: dict):
    """
    Processes a user query and returns a response.
    Payload Example:
    {
        "query": "What is the weather like today?"
    }
    """
    query = payload.get("query", "")
    if not query:
        return {"error": "No query provided"}

    # Simulate processing the query (you can replace this with LLM logic)
    response = f"Processed query: {query}"
    return {"response": response}
