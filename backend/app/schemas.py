from typing import List, Optional
from pydantic import BaseModel

class MaterialCreate(BaseModel):
    name: str

class SampleCreate(BaseModel):
    name: str
    quantity: Optional[str] = None

class HCPInteractionBase(BaseModel):
    hcp_name: str
    interaction_type: str
    date: str
    time: str
    attendees: Optional[str] = None
    topics: Optional[str] = None
    sentiment: Optional[str] = None
    outcomes: Optional[str] = None
    follow_up: Optional[str] = None
    notes: Optional[str] = None

class HCPInteractionCreate(HCPInteractionBase):
    materials: Optional[List[MaterialCreate]] = []
    samples: Optional[List[SampleCreate]] = []

class HCPInteractionUpdate(HCPInteractionBase):
    materials: Optional[List[MaterialCreate]] = []
    samples: Optional[List[SampleCreate]] = []

class Material(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

class Sample(BaseModel):
    id: int
    name: str
    quantity: Optional[str] = None

    class Config:
        orm_mode = True

class HCPInteraction(BaseModel):
    id: int
    hcp_name: str
    interaction_type: str
    date: str
    time: str
    attendees: Optional[str] = None
    topics: Optional[str] = None
    sentiment: Optional[str] = None
    outcomes: Optional[str] = None
    follow_up: Optional[str] = None
    notes: Optional[str] = None
    ai_summary: Optional[str] = None
    materials: List[Material] = []
    samples: List[Sample] = []

    class Config:
        orm_mode = True

class AIRequest(BaseModel):
    prompt: str
    interaction_id: Optional[int] = None

class AIResponse(BaseModel):
    text: str
    tool: str
    interaction: Optional[HCPInteraction] = None
