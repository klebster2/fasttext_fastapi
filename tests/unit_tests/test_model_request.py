import os

import pytest

import fasttext
from pydantic import BaseModel

from src.word_neighbors import (
        Word_Neighbors_Request,
        Word_Neighbors_Response,
)

from src.main import get_word_neighbors
from src.main import load_model

from tests.fixtures import EN_TEST_MODEL


def test_resolve_model_success():
    """
    """
    en_test_model = str(EN_TEST_MODEL.resolve())
    model, failiure = load_model(
        en_test_model,
    )
    assert failiure == False


