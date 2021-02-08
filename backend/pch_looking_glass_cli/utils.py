"""
Some generic utilities functions.
"""

import logging
import json
import os
import random

LOGGER = logging.getLogger(__name__)


def generate_nonce(length=100):
    """
    Generate pseudorandom number.

    See https://github.com/joestump/python-oauth2/blob/master/oauth2/__init__.py#L171
    """

    return "".join([str(random.SystemRandom().randint(0, 9)) for i in range(length)])


def save_data_to_json_file(data, data_dir, data_filename):
    """
    Save data to a JSON file

    data: The data to save.
    data_dir: The directory to save the data.
    data_filename: The filename of the data.
    """
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    data_json_filename = os.path.join(data_dir, data_filename)

    with open(data_json_filename, "w") as data_json_file:
        json.dump(data, data_json_file, indent=2)


def setup_logging(level):
    """
    Setup the logging levels for LOGGER

    level: Logging level to set
    """

    fmt = "%(asctime)s %(levelname)s: %(message)s [%(name)s:%(funcName)s:%(lineno)d] "
    logging.basicConfig(level=logging.getLevelName(str(level).upper()), format=fmt)
    LOGGER.info("Log level set to %s", level)
