import os

import pytest

import fasttext
from pydantic import BaseModel

from src.word_neighbors import (
        Word_Neighbors_Request,
        Word_Neighbors_Response,
)

from src.main import get_word_neighbors
from src.main import resolve_model

from tests.fixtures import EN_TEST_MODEL

def test_resolve_model_success():
    """
    """
    model, failiure = resolve_model(
        str(EN_TEST_MODEL.resolve()),
        sanity_check_model_names=False,
    )
    assert failiure == False

#def test_get_word_neighbors():
    #    model = fasttext.load_model(EN_TEST_MODEL.resolve())
#    get_word_neighbors()

