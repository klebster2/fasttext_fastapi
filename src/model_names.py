import json
import os

with open("./src/fbaipublicfiles.json", "r") as f:
    fbai_languages = json.loads(f.read())

FASTTEXT_DEFAULT_MODEL_NAMES = [
    os.path.basename(v.get('local_uncompressed')) for v in fbai_languages.values()
]

FASTTEXT_AVAILABLE_LANGUAGES = [
    k for k in fbai_languages.keys()
]

OTHER_MODEL_NAMES = [
]
