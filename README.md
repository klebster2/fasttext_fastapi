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

4. run uvicorn with the COMPRESS_FASTTEXT flag

```bash
COMPRESS_FASTTEXT=false uvicorn src.main:app --workers 1 --host 0.0.0.0 --port 8080
```

5. open another shell and run:
```bash
curl "http:/0.0.0.0:8080/get_word_neighbors/" -H "Content-Type: application/json" --data '{"word":"hey","neighbors":500,"dropstrange":true}'
```

