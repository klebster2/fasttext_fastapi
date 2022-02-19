from pydantic import BaseModel

class Model_Status_Response(BaseModel):
    message: str

class Model_Name(BaseModel):
    name: str
