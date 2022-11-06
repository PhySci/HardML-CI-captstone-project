import logging
import json
from typing import Dict, Any
import logging
import pickle
from minio import Minio
from minio.error import S3Error

_logger = logging.getLogger(__name__)


def setup_logging(loglevel="INFO", logfile=None) -> None:
    """

    :param logfile:
    :param loglevel:
    :return:
    """

    loglevel = getattr(logging, loglevel)

    logger = logging.getLogger()
    logger.setLevel(loglevel)
    fmt = '%(asctime)s: %(levelname)s: %(filename)s: ' + \
          '%(funcName)s(): %(lineno)d: %(message)s'
    formatter = logging.Formatter(fmt)

    if logfile:
        fh = logging.FileHandler(filename=logfile)
        fh.setLevel(loglevel)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    ch = logging.StreamHandler()
    ch.setLevel(loglevel)
    ch.setFormatter(formatter)
    logger.addHandler(ch)


def read_json(file_path: str) -> Dict:
    """
    :param file_path: path to JSON file
    :return:
    """
    with open(file_path, "r") as fid:
        try:
            res = json.load(fid)
        except Exception as err:
            _logger.error("Can not read file %s. Error message: %r", file_path, err)
            raise err
    return res


def load_pickle(file_path: str) -> Any:
    """
    :param file_path: path to Pickle file
    :return:
    """
    with open(file_path, "rb") as fid:
        try:
            res = pickle.load(fid)
        except Exception as err:
            _logger.error("Can not read file %s. Error message: %r", file_path, err)
            raise err
    return res


def load_model(model_name, save_pth: str, s3_params) -> None:
    """
    Load and save a file from S3 bucket
    :param model_name: name of object to get
    :param save_pth: path to save file
    :param s3_params: S3 credentials (endpoint, access_key, secret_key)
    """
    s3_client = Minio(**s3_params, secure=False)
    try:
        s3_client.fget_object(bucket_name="qa-cluster", object_name=model_name, file_path=save_pth)
    except S3Error as err:
        _logger.exception("S3 error: %r", err)
        raise err
    except Exception as err:
        _logger.exception("Can not download S3 object %s from %s. Error message: %r",
                          model_name, s3_params.get("S3_URL"), err)
        raise err
