from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
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
            # For example, you can fetch new messages for the user and send them here

# Define a Pydantic model for the notification request
class NotificationRequest(BaseModel):
    """
    Model to validate and store the notification data.
    
    Args:
        message (str): The content of the notification message.
    """
    message: str

# POST endpoint to add a new notification
@router.post("/notifications", dependencies=[Depends(verify_token)], status_code=201)
async def create_notification(notification_request: NotificationRequest):
    """
    Endpoint to add a new notification for all users or a specific user.
    
    Args:
        notification_request (NotificationRequest): The request containing the notification message.
    
    Returns:
        dict: A success message indicating that the notification was created.
    """
    # Logic to save the notification in the database
    # For simplicity, we'll just return a success message here
    return {"message": "Notification created successfully"}

# GET endpoint to retrieve all notifications
@router.get("/notifications", dependencies=[Depends(verify_token)], response_model=list)
async def get_notifications():
    """
    Endpoint to retrieve all notifications.
    
    Returns:
        list: A list of notification messages.
    """
    # Logic to fetch all notifications from the database
    # For simplicity, we'll just return a sample list here
    return [{"message": "Sample notification 1"}, {"message": "Sample notification 2"}]

# GET endpoint to retrieve a specific notification by ID
@router.get("/notifications/{id}", dependencies=[Depends(verify_token)], response_model=dict)
async def get_notification(id: int):
    """
    Endpoint to retrieve a specific notification by its ID.
    
    Args:
        id (int): The ID of the notification to retrieve.
    
    Returns:
        dict: The notification message.
    """
    # Logic to fetch the specified notification from the database
    # For simplicity, we'll just return a sample notification here
    return {"message": f"Notification {id} content"}

# PATCH endpoint to mark a notification as read
@router.patch("/notifications/{id}/read", dependencies=[Depends(verify_token)], status_code=204)
async def mark_notification_as_read(id: int):
    """
    Endpoint to mark a notification as read by its ID.
    
    Args:
        id (int): The ID of the notification to mark as read.
    
    Returns:
        None: No content is returned on success.
    """
    # Logic to update the notification status in the database
    # For simplicity, we'll just return nothing here
    pass

# WebSocket endpoint for marking a notification as read
@router.websocket("/ws/notifications/{user_id}/read/{id}")
async def websocket_mark_notification_as_read(websocket: WebSocket, user_id: int, id: int):
    """
    WebSocket endpoint to mark a notification as read by its ID for a specific user.
    
    Args:
        websocket (WebSocket): The WebSocket connection object.
        user_id (int): The ID of the user to receive notifications.
        id (int): The ID of the notification to mark as read.
    """
    await websocket.accept()
    try:
        # Logic to update the notification status in the database
        # For simplicity, we'll just return nothing here
        await websocket.send_text(f"Notification {id} marked as read for user {user_id}")
    except WebSocketDisconnect:
        pass
