import logging
import sys

from fastapi import FastAPI, status
import uvicorn
from sentence_transformers import SentenceTransformer

from utils import setup_logging

_logger = logging.getLogger(__name__)
app = FastAPI()

model = None


@app.on_event("startup")
def init_app():
    global model
    try:
        model = SentenceTransformer("distiluse-base-multilingual-cased-v1", device="cpu")
    except Exception as err:
        _logger.critical("Can not load pre-trained embedding model. Error message: %s", err)
        sys.exit(0)


@app.get("/")
def index():
    return {"message": "Index page of embedding service"}


@app.get("/encode")
def update_model(sentence):
    global model
    emb = model.encode(sentence)
    return {"sentence": sentence, "embedding": emb.tolist()}


@app.get("/health", status_code=status.HTTP_200_OK)
def health():
    return {"status": "fine"}


if __name__ == "__main__":
    setup_logging("WARNING")
    uvicorn.run(app, host="0.0.0.0", port=8000, debug=False)