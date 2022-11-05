import logging
from minio import Minio
from minio.error import S3Error
from typing import Any
import pickle

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

    if logfile is not None:
        fh = logging.FileHandler(filename=logfile)
        fh.setLevel(loglevel)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    ch = logging.StreamHandler()
    ch.setLevel(loglevel)
    ch.setFormatter(formatter)
    logger.addHandler(ch)


def _load_model(model_name, save_pth: str, s3_params) -> None:
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


def _load_pickle(file_name) -> Any:
    with open(file_name, "rb") as fid:
        try:
            o = pickle.load(fid)
        except Exception as err:
            _logger.exception(repr(err))
    return o


