from minio import Minio
from minio.error import S3Error
import pickle
from scipy.spatial import KDTree
import json
import numpy as np
import os


def upload_data(data_pth: str, data_generation: str):

    bucket_name = "qa-cluster"

    with open(os.path.join(data_pth, "use_embeddings_dg{:d}.pkl".format(data_generation)), "rb") as fid:
        use_embs = pickle.load(fid)

    with open(os.path.join(data_pth, "clusters_use_dg{:d}.json".format(data_generation)), "rb") as fid:
        sentence2clust = json.load(fid)

    s3_client = Minio(endpoint="localhost:9900", secret_key="s3_secret_key", access_key="s3_access_key", secure=False)

    if not s3_client.bucket_exists(bucket_name):
        s3_client.make_bucket(bucket_name)

    for cluster_id in sentence2clust.keys():
        cluster1 = [use_embs[sentence] for sentence in sentence2clust[cluster_id]]
        arr = np.concatenate(cluster1)
        tree = KDTree(arr, copy_data=True)

        temp_file = "temp_file.pkl"

        file_name = "cluster_dg{:d}_{:s}.pkl".format(data_generation, cluster_id)

        s = {"tree": tree, "sentences": sentence2clust[cluster_id]}
        with open(temp_file, "wb") as fid:
            pickle.dump(s, fid)

        try:
            s3_client.fput_object(bucket_name, file_name, temp_file)
        except S3Error as err:
            print(repr(err))

        os.remove(temp_file)


if __name__ == "__main__":
    upload_data(data_pth="../../data", data_generation=1)