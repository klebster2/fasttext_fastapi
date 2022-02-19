import fasttext
import sys
import json
import os

from fastapi import FastAPI
from .word_neighbors import (
        Word_Neighbors_Request,
        Word_Neighbors_Response,
)

from .model_names import (
        FASTTEXT_DEFAULT_MODEL_NAMES,
        OTHER_MODEL_NAMES,
)

from .model_utils import (
        Model_Status_Response,
        Model_Name,
)

loaded_models = {}

app = FastAPI()

@app.post(
        "/load_model/",
        response_model=Model_Status_Response
)

@app.post(
        "/get_word_neighbors/",
        response_model=Word_Neighbors_Response,
)

def resolve_model(
        model_path: str,
        sanity_check_model_names: bool,
        ):
    """
    """
    failiure = False
    model = None
    model_basename = os.path.basename(model_path)

    if sanity_check_model_names and model_basename in FASTTEXT_DEFAULT_MODEL_NAMES:
        # download then load
        model = fasttext.load_model(model_path)
    elif sanity_check_model_names and model_basename in OTHER_MODEL_NAMES:
        # download then load
        # model = ...
        pass # method to be added if other model resources are found e.g. online
    elif sanity_check_model_names:
        failiure = True
    else:
        model = fasttext.load_model(model_path)

    return model, failiure

async def load_model(
        model_name: str
    ) -> Model_Status_Response:
    """
    """
    model, failiure = resolve_model(model_name)

    if failiure:
        return Model_Status_Response(
                message=f"failiure loading {model_name}.",
        )
    else:
        loaded_models.update({model_name: model})
        return Model_Status_Response(
                message=f"success loading {model_name}."
        )


async def get_word_neighbors(
        model_name: Model_Name,
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
    neighbors = loaded_models.get(
            model_name
    ).get_nearest_neighbors(
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
