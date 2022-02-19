from ..model_utils import Model_Name
from pydantic import BaseModel

class Word_Neighbors_Request(BaseModel):
    word: str
    neighbors: int
    model_name: Model_Name
