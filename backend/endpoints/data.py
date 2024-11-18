from fastapi import APIRouter

router = APIRouter()

@router.get("/fetch-data")
async def fetch_data():
    """
    Returns sample data from the backend.
    Example Response:
    {
        "data": [
            {"id": 1, "info": "Sample data 1"},
            {"id": 2, "info": "Sample data 2"}
        ]
    }
    """
    # Example data (replace this with your actual data retrieval logic)
    data = [
        {"id": 1, "info": "Sample data 1"},
        {"id": 2, "info": "Sample data 2"}
    ]
    return {"data": data}
