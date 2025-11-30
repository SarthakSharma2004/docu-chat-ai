from pydantic import BaseModel, Field

class QueryRequest(BaseModel):
    session_id: str = Field(..., description="Session ID, Unique session identifier.")
    question: str = Field(..., description="User's question.")


class Source(BaseModel):
    content: str = Field(description= "Content of the source document.")
    meta: str = Field(default="Unknown", description= "Metadata (Source document) of the source document.")
    page: str = Field(default="N/A", description= "Page number of the source document.")

class QueryResponse(BaseModel):
    answer: str = Field(..., description="Answer to the user's question.")
    sources: list[Source] = Field(default= [], description= "Sources of the answer.")
