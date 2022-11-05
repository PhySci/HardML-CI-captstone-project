import logging
import sys

import fastapi
from fastapi import FastAPI, status
import uvicorn
from utils import setup_logging, read_json, load_pickle
import requests
from settings import EMB_SERVING_ADDR, CLUSTER1, CLUSTER2, CLUSTER3, CLUSTER4
import numpy as np
from scipy.spatial.distance import cdist

_logger = logging.getLogger(__name__)
app = FastAPI()

centroids = None
centroids_arr = None
centroids_keys = list()

cluster_services = {"0": CLUSTER1,
                    "1": CLUSTER2,
                    "2": CLUSTER3,
                    "3": CLUSTER4}


@app.on_event("startup")
def init_app():
    global centroids_keys, centroids_arr
    centroids_path = "./data/clusters_centers_use_dg1.pkl"
    try:
        centroids = load_pickle(centroids_path)
    except Exception as err:
        _logger.critical("Can not read embedding centroids from %s. Error message: %s", centroids_path, err)
        sys.exit(0)

    r = list()
    for centroid_key, centroid_val in centroids.items():
        centroids_keys.append(centroid_key)
        r.append(centroid_val)

    centroids_arr = np.array(r)


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

    # @TODO: vectorize this opera

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
