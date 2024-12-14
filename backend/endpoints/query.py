import os
from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException
from openai import AzureOpenAI  # type: ignore

# Load environment variables
load_dotenv()

# Fetch Azure credentials from .env
endpoint = os.getenv("ENDPOINT")
deployment = os.getenv("DEPLOYMENT")
subscription_key = os.getenv("SUBSCRIPTION_KEY")

# Initialize Azure OpenAI client
client = AzureOpenAI(
    azure_endpoint=endpoint,
    api_key=subscription_key,
    api_version="2024-05-01-preview",
)

router = APIRouter()

@router.post("/process-query")
async def process_query(payload: dict):
    """
    Processes a user query using Azure OpenAI and returns a response.
    Payload Example:
    {
        "query": "What is ISO New England?"
    }
    """
    query = payload.get("query", "")
    if not query:
        raise HTTPException(status_code=400, detail="No query provided")

    try:
        # Prepare chat prompt
        chat_prompt = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": query},
        ]

        # Query Azure OpenAI
        completion = client.chat.completions.create(
            model=deployment,
            messages=chat_prompt,
            max_tokens=800,
            temperature=0.7,
        )

        # Extract response
        response = completion.choices[0].message.content
        return {"response": response}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")
