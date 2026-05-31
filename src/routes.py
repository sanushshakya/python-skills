from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, HTTPException, status
from pydantic import BaseModel
import re
from src.auth import verify_token

# Initialize router
router = APIRouter()

# Define a Pydantic model for the query input
class QueryInput(BaseModel):
    """
    Model to validate and store the natural language query.
    
    Args:
        query (str): The user's input query.
    """
    query: str

# Define a Pydantic model for the output filter
class FilterOutput(BaseModel):
    """
    Model to represent the SQL filter generated from the query.
    
    Args:
        filter_string (str): The SQL-like filter string.
    """
    filter_string: str

# Sample mapping of keywords to SQL filter conditions
KEYWORD_MAP = {
    "age": "user_age",
    "name": "user_name",
    "email": "user_email"
}

def natural_language_to_sql_filter(query: str) -> str:
    """
    Translates a natural language query into a SQL-like filter string.
    
    Args:
        query (str): The user's input query.
    
    Returns:
        str: The generated SQL-like filter string.
    """
    # Tokenize the query
    tokens = re.findall(r'\b\w+\b', query)
    conditions = []
    
    for token in tokens:
        if token.lower() in KEYWORD_MAP:
            keyword = KEYWORD_MAP[token.lower()]
            conditions.append(f"{keyword} LIKE '%{token}%'")
    
    return " AND ".join(conditions)

# Define the smart-search endpoint
@router.post("/ai/smart-search", response_model=FilterOutput)
def smart_search(query_input: QueryInput, q: str = Depends(lambda: query_input.query)):
    """
    Endpoint to translate natural language queries into database filters.
    
    Args:
        query_input (QueryInput): The input containing the natural language query.
    
    Returns:
        FilterOutput: The generated SQL-like filter string.
    
    Raises:
        HTTPException: If the query is empty or invalid.
    """
    # Validate the query
    if not q.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Query cannot be empty"
        )
    
    # Generate the SQL filter
    sql_filter = natural_language_to_sql_filter(q)
    
    return FilterOutput(filter_string=sql_filter)

# WebSocket endpoint for real-time notifications
@router.websocket("/ws/notifications/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int):
    """
    WebSocket endpoint to send real-time notifications to a specific user.
    
    Args:
        websocket (WebSocket): The WebSocket connection object.
        user_id (int): The ID of the user to receive notifications.
    """
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            if data == "close":
                await websocket.close()
                break
            # Logic to send notifications based on user_id
            # For example, you can fetch new messages for the use