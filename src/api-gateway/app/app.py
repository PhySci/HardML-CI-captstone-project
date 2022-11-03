import logging
import sys

from fastapi import FastAPI, status
import os
import uvicorn
from .utils import setup_logging, read_json, load_pickle

_logger = logging.getLogger(__name__)
app = FastAPI()

centroids = None


@app.on_event("startup")
def init_app():
    global centroids
    centroids_path = "clusters_centers_use_dg1.pkl"
    try:
        centroids = load_pickle(centroids_path)
    except Exception as err:
        _logger.critical("Can not read embedding centroids from %s. Error message: %s", centroids_path, err)
        sys.exit(0)


@app.get("/")
def index():
    pass


@app.get("/update_model")
def update_model(version: int):
    pass


@app.get("/health", status_code=status.HTTP_200_OK)
def health():
    return {"status": "fine"}


if __name__ == "__main__":
    setup_logging("DEBUG")
    uvicorn.run(app, host="0.0.0.0", port=8000, debug=True)
