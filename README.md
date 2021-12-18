# fasttext_fastapi

A simple API for some of the fasttext functions

1. install miniconda

2. create env

```bash
conda env create -f environment.yml
```

and activate env

3. download model

```bash
python3 -c "import fasttext.util; fasttext.util.download_model('en', if_exists='ignore')  # English 300 dim cc vecs"
```

4. run uvicorn

```bash
uvicorn main:app --workers 1 --host 0.0.0.0 --port 8080
```
