from pydantic import BaseModel

class Word_Neighbors_Request(BaseModel):
    word: str
    neighbors: int
