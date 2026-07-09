from pydantic import BaseModel, Field, HttpUrl ,ConfigDict
from datetime import datetime

class URLCreate(BaseModel):
    url: HttpUrl = Field(..., description="The URL to be shortened")
    
class URLResponse(BaseModel):
    short_code: str = Field(..., description="The shortened code for the URL")
    original_url: HttpUrl = Field(..., description="The original URL that was shortened")
    clicks: int = Field(..., description="The number of times the shortened URL has been accessed")
    created_at: datetime = Field(..., description="The timestamp when the URL was created")

    model_config = ConfigDict(from_attributes=True)
    
