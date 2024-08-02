from pydantic import BaseModel


class WordNeighborsRequest(BaseModel):
    word: str
    neighbors: int
    dropstrange: bool
    language: str
