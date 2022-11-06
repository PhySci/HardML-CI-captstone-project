import logging
import sys

import fastapi
from fastapi import FastAPI, status
import uvicorn
from utils import setup_logging, load_model, load_pickle
import requests
from settings import EMB_SERVING_ADDR, CLUSTER1, CLUSTER2, CLUSTER3, CLUSTER4, S3_URL, S3_ACCESS_KEY, S3_SECRET_KEY, DATA_GENERATION
import numpy as np
from scipy.spatial.distance import cdist
import os

_logger = logging.getLogger(__name__)
app = FastAPI()

centroids_arr = None
centroids_keys = list()

cluster_services = {"0": CLUSTER1,
                    "1": CLUSTER2,
                    "2": CLUSTER3,
                    "3": CLUSTER4}


@app.on_event("startup")
def init_app():
    """

    :return:
    """
    global centroids_keys, centroids_arr
    try:
        centroids = _get_model()
    except Exception as err:
        _logger.critical("Can not load centroids. Error message: %s", err)
        sys.exit(0)

    r = list()
    for centroid_key, centroid_val in centroids.items():
        centroids_keys.append(centroid_key)
        r.append(centroid_val)

    centroids_arr = np.array(r)


def _get_model():
    """
    :return:
    """
    model_path = os.path.join(os.path.dirname(__file__), "data")
    file_name = "clusters_centers_use_dg{:s}.pkl".format(os.environ["DATA_GENERATION"])
    file_pth = os.path.join(model_path, file_name)
    if not os.path.exists(file_pth):
        s3_params = {"endpoint": S3_URL,
                     "access_key": S3_ACCESS_KEY,
                     "secret_key": S3_SECRET_KEY}
        load_model(file_name, file_pth, s3_params)
    o = load_pickle(file_pth)
    return o


@app.get("/")
def index():
    return fastapi.Response("<h1>QA service main page</h1>")


@app.get("/update_model", status_code=status.HTTP_501_NOT_IMPLEMENTED)
def update_model(version: int):
    pass


@app.get("/health", status_code=status.HTTP_200_OK)
def health():
    return {"status": "fine"}


@app.get("/similar")
def predict(sentence: str):

    r = requests.get("http://"+EMB_SERVING_ADDR+"/encode",
                     params={"sentence": sentence},
                     headers={"Content-Type": "application/json"})
    if r.status_code != 200:
        _logger.error("Can not encode the sentence")
        sys.exit(0)

    content = r.json()
    emb = content["embedding"]
    centroid_id = _get_centroid_id(emb)
    _logger.info("Cluster %s", centroid_id)

    r = requests.get("http://" + cluster_services[centroid_id]+":8000/candidates",
                     params={"emb": emb},
                     headers={"Content-Type": "application/json"})
    if r.status_code != 200:
        _logger.error("Can not get candidates")
        sys.exit(0)

    return r.json()


def _get_centroid_id(emb):
    global centroids_arr
    global centroids_keys
    emb_arr = np.array(emb)
    cosine_dist = cdist(centroids_arr, emb_arr[np.newaxis, :], "cosine")
    best_centroid_id = centroids_keys[np.argmin(cosine_dist)]
    return best_centroid_id


if __name__ == "__main__":
    setup_logging("WARNING")
    uvicorn.run(app, host="0.0.0.0", port=8000, debug=False)
