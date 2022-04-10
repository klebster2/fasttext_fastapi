import fasttext
import sys
import json
import os

from fastapi import FastAPI

from functools import lru_cache
from collections.abc import Iterable

from pathlib import Path
from pydantic import BaseModel

from typing import Iterable, Tuple

import re

class Word_Neighbors_Request(BaseModel):
    word: str
    neighbors: int
    dropstrange: bool

class Word_Neighbors_Response(BaseModel):
    neighbors_output: list

def fsa(word):
    if re.match(".*[a-z]\.[A-Z].*", word): # reject inter-word fullstop
        return False
    elif re.match(".*[A-Z0-9].*", word): # Reject capital letters and numbers
        return False
    elif re.match(r".*([a-z])\1{2,}", word):
        return False
    else:
        return True

model = fasttext.load_model("cc.en.300.bin")

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
    #neighbors_cleaned = map(lambda x: {x.get("word"),}, neighbors))
    neighbors_output = []
    for i, neighbor in enumerate(neighbors, 1):
        if fsa(word=neighbor[1]) and word_neighbors_request.dropstrange:
            neighbors_output.append(
                {
                    "id": i,
                    "neighbor": neighbor[1],
                    "score": f"{neighbor[0]:.3f}",
                }
            )
        elif not word_neighbors_request.dropstrange:
            neighbors_output.append(
                {
                    "id": i,
                    "neighbor": neighbor[1],
                    "score": f"{neighbor[0]:.3f}",
                }
            )
        else:
            continue

    #return json.dumps(neighbors_output, indent=4)
    return Word_Neighbors_Response(
            neighbors_output=neighbors_output
    ) 
