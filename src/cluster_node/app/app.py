import logging
import os
import pickle
from typing import List, Any
import numpy as np

from fastapi import FastAPI, status, Query
import uvicorn


from utils import setup_logging, _load_model, _load_pickle
from settings import DATA_GENERATION, CLUSTER_ID, MODEL_PATH, S3_URL, S3_ACCESS_KEY, S3_SECRET_KEY

_logger = logging.getLogger(__name__)
app = FastAPI()

kd_sentences = None
kd_tree = None


def _get_model(data_generation, cluster_id):
    """

    :param data_generation:
    :param cluster_id:
    :return:
    """
    file_name = "cluster_dg{:s}_{:s}.pkl".format(data_generation, cluster_id)
    file_pth = os.path.join(MODEL_PATH, file_name)
    if not os.path.exists(file_pth):
        s3_params = {"endpoint": S3_URL,
                     "access_key": S3_ACCESS_KEY,
                     "secret_key": S3_SECRET_KEY}
        _load_model(file_name, file_pth, s3_params)
    o = _load_pickle(file_pth)
    return o


@app.on_event("startup")
def init_app():
    global kd_tree
    global kd_sentences
    o = _get_model(DATA_GENERATION, CLUSTER_ID)
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