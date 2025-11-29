from pydantic import BaseModel, Field

class QueryRequest(BaseModel):
    session_id: str = Field(..., description="Session ID, Unique session identifier.")
    question: str = Field(..., description="User's question.")

class QueryResponse(BaseModel):
    answer: str = Field(..., description="Answer to the user's question.")
