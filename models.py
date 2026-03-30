from pydantic import BaseModel
from typing import Optional


class SubjectCreate(BaseModel):
    id: str
    name: str
    semester: str
    category: str  # basic / required / elective
    credits: int
    concepts: list[str]
    description: str = ""


class SubjectUpdate(BaseModel):
    name: Optional[str] = None
    semester: Optional[str] = None
    category: Optional[str] = None
    credits: Optional[int] = None
    concepts: Optional[list[str]] = None
    description: Optional[str] = None


class SubjectResponse(BaseModel):
    id: str
    name: str
    semester: str
    category: str
    credits: int
    concepts: list[str]
    description: str


class ConnectionCreate(BaseModel):
    from_id: str
    to_id: str
    type: str  # prereq / overlap / extends
    reason: str = ""
    shared: list[str] = []


class ConnectionUpdate(BaseModel):
    from_id: Optional[str] = None
    to_id: Optional[str] = None
    type: Optional[str] = None
    reason: Optional[str] = None
    shared: Optional[list[str]] = None


class ConnectionResponse(BaseModel):
    id: int
    from_id: str
    to_id: str
    type: str
    reason: str
    shared: list[str]
