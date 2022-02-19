from pydantic import BaseModel

class Word_Neighbors_Response(BaseModel):
    neighbors_output: list
