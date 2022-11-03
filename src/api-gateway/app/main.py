from app import setup_logging
import sys
import signal
import logging
import uvicorn

_logger = logging.getLogger(__name__)

def sig_handler():
    sys.exit(0)


if __name__ == "__main__":
    setup_logging()
    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)
    _logger.info("Run app")
    uvicorn.run("app:app", host="0.0.0.0", port=8000, debug=True, log_level=logging.INFO)