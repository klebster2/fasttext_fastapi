import fasttext
import sys
import json

from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel


model = fasttext.load_model("cc.en.300.bin")

class Word_Neighbors_Request(BaseModel):
    word: str
    neighbors: int

class Word_Neighbors_Response(BaseModel):
    neighbors_output: list

app = FastAPI()

@app.post(
        "/get_word_neighbors/",
        response_model=Word_Neighbors_Response
)

async def get_word_neighbors(word_neighbors_request: Word_Neighbors_Request):
    neighbors = model.get_nearest_neighbors(
            word_neighbors_request.word,
            k=word_neighbors_request.neighbors,
    )
    neighbors_output = []
    for i, neighbor in enumerate(neighbors, 1):
        neighbors_output.append(
            {
                "id": i,
                "neighbor": neighbor[1],
                "score": f"{neighbor[0]:.3f}",
            }
        )
    #return json.dumps(neighbors_output, indent=4)
    return Word_Neighbors_Response(
            neighbors_output=neighbors_output
    )
