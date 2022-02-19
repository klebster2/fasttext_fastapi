import os
from pathlib import Path

TEST_FIXTURES = Path(Path(__file__).parents[0])
ROOT_DIR = Path(Path(TEST_FIXTURES).parents[1])

EN_TEST_MODEL = TEST_FIXTURES / "test_model.bin.gz"
