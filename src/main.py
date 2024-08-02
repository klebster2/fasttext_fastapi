import fasttext
import sys
import json
import os
import fasttext.util

from fastapi import FastAPI

from functools import lru_cache
from collections.abc import Iterable

from pathlib import Path
from pydantic import BaseModel

import re

from .word_neighbors import WordNeighborsRequest, WordNeighborsResponse
from .etymologies import (
    get_etymologies_file,
    WordEtymologyRequest,
    WordEtymologyResponse,
)

global etymologies

etymologies = get_etymologies_file()


def word_is_clean(word):
    if re.match(r".*[a-z]{2,}[\.!?,;:*][A-Z].*", word):  # reject inter-word fullstop
        print("1")
        return False
    elif re.match(r".*[A-Z0-9].*", word):  # Reject capital letters and numbers
        print("2")
        return False
    elif re.match(r".*([a-z])\1{2,}", word):
        print("3")
        return False
    elif len(word) > 20:
        print("4")
        return False
    else:
        return True


with open(Path(Path(__file__).parent, "fbaipublicfiles.json"), "r") as f:
    fbaipublicfile = json.loads(f.read())


MAX_MODELS_IN_MEMORY = 3

global models
models = {}

app = FastAPI()


class LoadFastTextModel(BaseModel):
    language: str


models.update(
    {"English": fasttext.load_model(fbaipublicfile["English"]["local_uncompressed"])}
)


@app.post("/add_model/")
async def get_model(modelloader: LoadFastTextModel):

    if modelloader.language in models.keys():
        return "Model already in memory"

    elif (
        modelloader.language not in models.keys()
        and len(models.keys()) == MAX_MODELS_IN_MEMORY
    ):
        raise ValueError("Cannot fulfil request, too many models are in memory!")

    elif os.path.exists(fbaipublicfile[modelloader.language]["local_uncompressed"]):
        print("Path already exists, loading model")
        models.update(
            {
                modelloader.language: fasttext.load_model(
                    fbaipublicfile[modelloader.language]["local_uncompressed"]
                )
            }
        )

    else:
        language_code = fbaipublicfile[modelloader.language][
            "local_uncompressed"
        ].split(".")[1]
        fasttext.util.download_model(language_code, if_exists="ignore")  # English
        models.update(
            {
                modelloader.language: fasttext.load_model(
                    fbaipublicfile[modelloader.language]["local_uncompressed"]
                )
            }
        )
        return "Loading Model"


@app.post("/get_word_neighbors/", response_model=WordNeighborsResponse)
async def get_word_neighbors(
    word_neighbors_request: WordNeighborsRequest,
) -> WordNeighborsResponse:
    neighbors = models[word_neighbors_request.language].get_nearest_neighbors(
        word_neighbors_request.word,
        k=word_neighbors_request.neighbors,
    )

    _neighbors = []
    for i, neighbor in enumerate(neighbors, 1):
        print(neighbor)
        _etymologies = []
        if word_is_clean(word=neighbor[1]) and word_neighbors_request.dropstrange:
            for e in etymologies.get(neighbor[1], []):
                if e["ety"]:  # type: ignore
                    _etymologies.append(e["ety"])  # type: ignore

            _neighbors.append(
                {
                    "id": i,
                    "neighbor": neighbor[1],
                    "score": f"{neighbor[0]:.3f}",
                    "etymology": "\n\n".join(_etymologies),  # type: ignore
                }
            )

    print(_neighbors)

    return WordNeighborsResponse(neighbors=_neighbors)


# @app.post("/get_word_etymology/", response_model=WordEtymologyResponse)
# async def get_word_etymology(word_etymology_request: WordEtymologyRequest):
#    if word_etymology_request.word in etymologies.keys():  # type: ignore
#        return WordEtymologyResponse(etymology="\n".join([e["ety"] for e in etymologies[word_etymology_request.word]]))  # type: ignore
#    else:
#        return WordEtymologyResponse(etymology="")
# word
