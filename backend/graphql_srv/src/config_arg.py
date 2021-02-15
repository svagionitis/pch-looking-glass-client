"""
Parsing the input parameters
"""

import os
import logging
import configargparse

LOGGER = logging.getLogger(__name__)


def parse_input_args(config_file="graphql_srv_config.conf"):
    """
    Parse the configuration arguments

    It will read them from the configuration file graphql_srv_config.conf

    config_file: The configuration file. Default value graphql_srv_config.conf
    """
    LOGGER.debug("config_file: %s", config_file)

    cwd = os.path.dirname(os.path.realpath(__file__))

    default_config_files = [os.path.join(cdir, config_file) for cdir in (cwd, ".")]

    conf = configargparse.ArgParser(default_config_files=default_config_files)
    conf.add(
        "--config",
        required=False,
        is_config_file=True,
        help="config file path",
    )
    conf.add(
        "--log-level",
        required=False,
        env_var="LOG_LEVEL",
        choices=["debug", "info", "warning", "error", "critical"],
        help="Set the logging level",
    )
    conf.add(
        "--db-host",
        env_var="DB_HOST",
        required=True,
        type=str,
        help="The host of the DB",
    )
    conf.add(
        "--db-port",
        env_var="DB_PORT",
        required=True,
        type=int,
        help="The port of the DB",
    )
    conf.add(
        "--db-user",
        env_var="DB_USER",
        required=True,
        type=str,
        help="The username to connect to the DB",
    )
    conf.add(
        "--db-pass",
        env_var="DB_PASS",
        required=True,
        type=str,
        help="The password of the user to connect to the DB",
    )
    conf.add(
        "--db-name",
        env_var="DB_NAME",
        required=True,
        type=str,
        help="The name of the DB to connect",
    )

    return conf.parse_args()
