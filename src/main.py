import fasttext
import sys
import json
import os

from fastapi import FastAPI

from functools import lru_cache
from collections.abc import Iterable

from pathlib import Path

from .word_neighbors import (
        Word_Neighbors_Request,
        Word_Neighbors_Response,
)

from fasttext.util.util import valid_lang_ids as VALID_LANG_IDS

#from .model_names import (
#        FASTTEXT_DEFAULT_MODEL_NAMES,
#        OTHER_MODEL_NAMES,
#)

from .model_utils import (
        Model_Status_Response,
)

app = FastAPI()

# TODO: add get langids
#@app.get(
        #"/get_fasttext_langids/",
        #response_model=LangIds,
        #)

@app.post(
        "/get_word_neighbors/",
        response_model=Word_Neighbors_Response,
)

@lru_cache()
def load_model(
        model_name: str,
        ) -> Iterable[fasttext.FastText._FastText, bool]:
    """
    """
    failiure = False
    model = None
    model_path = Path("models") / model_name

    if model_path.exists():
        model = fasttext.load_model(str(model_path))
    else:
        failiure = True

    return model, failiure

def download_model(model_name):
    """
    Parameters
    ----------
    model_name: str
    a binarized fasttext model

    Returns
    -------
    None

    See Also
    --------
    ...

    Examples
    --------
    ...
    """
    lang_id = re.sub(r"cc\.([a-z]{2,4})\.300\.bin", r"\1", model_name)

    if not lang_id in VALID_LANG_IDS:
        return None
#    elif model_basename in OTHER_MODEL_NAMES:
        # download then load
#        pass # method to be added if other model resources are found e.g. online

    if not os.path.exists("models"):
        os.makedirs('models', exist_ok=True)

    filename = fasttext.util.download_model(
        lang_id,
        if_exists='ignore'
    )

    return filename

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
    ...
    """
    model, failiure = load_model(model_name)

    if failiure:
        model, failiure = download_model(model_name)
        pass # if we hit failiure, download the model

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
            neighbors_output=neighbors_output,
    )
