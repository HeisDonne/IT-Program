import logging
import os
import sys


def setup_logging(app):
    level = os.environ.get("LOG_LEVEL", "WARNING").upper()

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(
        logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s")
    )

    app.logger.handlers.clear()
    app.logger.addHandler(handler)
    app.logger.setLevel(level)
    app.logger.info("Logging started at level %s", level)