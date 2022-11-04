import logging
import os
import pickle
import sys
from typing import List, Any
import numpy as np

from fastapi import FastAPI, status, Query
import uvicorn

from utils import setup_logging
from settings import DATA_GENERATION, CLUSTER_ID

_logger = logging.getLogger(__name__)
app = FastAPI()

kd_sentences = None
kd_tree = None


@app.on_event("startup")
def init_app():
    global kd_tree
    global kd_sentences
    file_pth = "cluster_dg{:s}_{:s}.pkl".format(DATA_GENERATION, CLUSTER_ID)
    with open(os.path.join("./data", file_pth), "rb") as fid:
        o = pickle.load(fid)
    kd_tree = o["tree"]
    kd_sentences = o["sentences"]


@app.get("/")
def index():
    return {"message": "Index page of cluster node"}


@app.get("/candidates")
def get_candidatest(emb: List[Any] = Query(default=None)):
    global kd_tree
    global kd_sentences
    v = np.array(emb)
    _, ids = kd_tree.query(v, k=2, eps=2)
    res = [kd_sentences[i] for i in ids]
    return {"candidates": res}


@app.get("/health", status_code=status.HTTP_200_OK)
def health():
    return {"status": "fine"}


if __name__ == "__main__":
    setup_logging("DEBUG")
    uvicorn.run(app, host="0.0.0.0", port=8002, debug=True)