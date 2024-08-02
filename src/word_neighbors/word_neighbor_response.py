from pydantic import BaseModel


class WordNeighborsResponse(BaseModel):
    neighbors: list
