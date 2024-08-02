import fasttext
import sys
import json
import os
import fasttext.util
import compress_fasttext

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


@lru_cache(maxsize=1000)
def word_is_clean(word):
    if re.match(r".*[a-z]{2,}[\.!?,;:*][A-Z].*", word):  # reject inter-word fullstop
        print("1")
        return False
    elif re.match(r".+[A-Z0-9].*", word):  # Reject capital letters and numbers
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


if bool(os.environ["COMPRESS_FASTTEXT"] == "true"):
    models.update(
        {
            "English": compress_fasttext.models.CompressedFastTextKeyedVectors.load(
                "https://github.com/avidale/compress-fasttext/releases/download/v0.0.4/cc.en.300.compressed.bin"
            )
        }
    )
elif bool(os.environ["COMPRESS_FASTTEXT"] == "false"):
    model = fasttext.load_model(fbaipublicfile["English"]["local_uncompressed"])
    from gensim.models.fasttext import FastTextKeyedVectors
    import compress_fasttext

    # big_model = FastTextKeyedVectors.load('path-to-original-model')
    # big_model = FastTextKeyedVectors.load(
    #    fbaipublicfile["English"]["local_uncompressed"]
    # )
    # small_model = compress_fasttext.prune_ft_freq(big_model, pq=True, qdim=200)
    # small_model.save('path-to-new-model')
    # ft = fasttext.load_model('cc.en.300.bin')
    # model.get_dimension()
    # fasttext.util.reduce_model(model, 100)
    # model.get_dimension()
    # model.quantize(retrain=False, qnorm=True)
    models.update({"English": model})
else:
    raise ValueError("COMPRESS_FASTTEXT environment variable not set")


@app.post("/add_model/")
@lru_cache(maxsize=20)
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

    if isinstance(models[word_neighbors_request.language], fasttext.FastText._FastText):
        print("calling fasttext")
        # Default FastText model
        neighbors = models[word_neighbors_request.language].get_nearest_neighbors(
            word_neighbors_request.word,
            k=word_neighbors_request.neighbors,
        )
        score_idx = 0
        word_idx = 1
    elif isinstance(
        models[word_neighbors_request.language],
        compress_fasttext.models.CompressedFastTextKeyedVectors,
    ):
        print("calling compress_fasttext")
        # Compute cosine similarity to get the most similar words
        neighbors = models[word_neighbors_request.language].most_similar(
            word_neighbors_request.word,
            topn=word_neighbors_request.neighbors,
        )
        score_idx = 1
        word_idx = 0
    else:
        raise ValueError("Model not recognized")

    _neighbors = []
    for i, neighbor in enumerate(neighbors, 1):
        _etymologies = []
        if (
            word_is_clean(word=neighbor[word_idx])
            and word_neighbors_request.dropstrange
        ):
            for e in etymologies.get(neighbor[word_idx], []):
                if e["ety"]:  # type: ignore
                    _etymologies.append(e["ety"])  # type: ignore

            _etymologies = [e for e in set(_etymologies)]
            _neighbors.append(
                {
                    "id": i,
                    "neighbor": neighbor[word_idx],
                    "score": f"{neighbor[score_idx]:.3f}",
                    "etymology": "\n\n".join(_etymologies),  # type: ignore
                }
            )
    print(_neighbors)

    return WordNeighborsResponse(neighbors=_neighbors)
