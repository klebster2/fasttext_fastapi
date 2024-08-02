import os
import json
from pydantic import BaseModel

import typing as t


def get_etymologies_file() -> t.Dict[str, str]:
    import requests

    if not os.path.exists("etymologies.json"):

        etymologies = requests.get(
            "https://raw.githubusercontent.com/klebster2/wiktionary-dictionary/master/etymologies.json"
        )
        with open("etymologies.json", "w") as f:
            f.write(etymologies.text)
        etymologies = etymologies.json()

    else:
        with open("etymologies.json", "r") as f:
            etymologies = json.loads(f.read())

    return etymologies


class WordEtymologyResponse(BaseModel):
    etymology: str


class WordEtymologyRequest(BaseModel):
    word: str


if __name__ == "__main__":
    print()
