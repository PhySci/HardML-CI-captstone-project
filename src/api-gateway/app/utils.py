import logging
import json
from typing import Dict, Any
import logging
import pickle

_logger = logging.getLogger(__name__)


def setup_logging(logfile=None, loglevel="INFO") -> None:
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
