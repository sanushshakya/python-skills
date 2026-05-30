from datetime import datetime

class ConversationHistory:
    """Model to store conversation history between users and an AI assistant."""
    
    def __init__(self):
        """
        Initializes a new instance of the ConversationHistory class.
        
        Attributes:
            conversations (list): A list to store individual conversations.
        """
        self.conversations = []
    
    def add_conversation(self, user_id: int, ai_assistant_id: int, message: str, timestamp: datetime):
        """
        Adds a new conversation entry to the history.

        Args:
            user_id (int): The ID of the user.
            ai_assistant_id (int): The ID of the AI assistant.
            message (str): The text of the message exchanged.
            timestamp (datetime): The timestamp when the message was exchanged.
        """
        self.conversations.append({
            "user_id": user_id,
            "ai_assistant_id": ai_assistant_id,
            "message": message,
            "timestamp": timestamp
        })
    
    def get_conversation_history(self, user_id: int) -> list:
        """
        Retrieves the conversation history for a specific user.

        Args:
            user_id (int): The ID of the user.

        Returns:
            list: A list of conversation entries.
        """
        return [conv for conv in self.conversations if conv["user_id"] == user_id]
    
    def get_ai_assistant_conversation_history(self, ai_assistant_id: int) -> list:
        """
        Retrieves the conversation history involving a specific AI assistant.

        Args:
            ai_assistant_id (int): The ID of the AI assistant.

        Returns:
            list: A list of conversation entries.
        """
        return [conv for conv in self.conversations if conv["ai_assistant_id"] == ai_assistant_id]
    
    def clear_conversation_history(self):
        """
        Clears all conversation history.
        """
        self.conversations.clear()