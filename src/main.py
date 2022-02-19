import fasttext
import sys
import json

from fastapi import FastAPI
from .word_neighbors import (
        Word_Neighbors_Request, Word_Neighbors_Response
)

model = fasttext.load_model("cc.en.300.bin")

app = FastAPI()

@app.post(
        "/get_word_neighbors/",
        response_model=Word_Neighbors_Response
)

async def get_word_neighbors(
        word_neighbors_request: Word_Neighbors_Request,
    ) -> Word_Neighbors_Response:
    """
    Parameters
    ----------
    word_neighbors_request: Word_Neighbors_Request

    Returns
    -------
    Word_Neighbors_Response

    See Also
    --------
    ...

    Examples
    --------
    """
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
    return Word_Neighbors_Response(
            neighbors_output=neighbors_output
    )
