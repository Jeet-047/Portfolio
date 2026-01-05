import os
from supabase import create_client, Client
from typing import Dict, Any
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class DatabaseService:
    """Service for interacting with Supabase database."""
    
    def __init__(self):
        """Initialize Supabase client."""
        self.supabase_url = os.getenv("SUPABASE_URL")
        self.supabase_key = os.getenv("SUPABASE_PUBLIC_KEY")
        
        if not self.supabase_url or not self.supabase_key:
            raise ValueError("SUPABASE_URL and SUPABASE_PUBLIC_KEY must be set in environment variables")
        
        self.supabase: Client = create_client(
            self.supabase_url,
            self.supabase_key
        )
    
    def insert_contact_message(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Insert a contact message into the database.
        
        Args:
            data: Dictionary containing name, email, subject, message
            
        Returns:
            Response from Supabase insert operation
        """
        response = self.supabase.table("contact_messages").insert(data).execute()
        return response


# Create a singleton instance
db_service = DatabaseService()

