"""
Parsing the input parameters
"""

import os
import logging
import configargparse

LOGGER = logging.getLogger(__name__)


def parse_input_args(script_args, config_file="pch_looking_glass_cli_config.conf"):
    """
    Parse the configuration arguments

    If no input arguments is given, it will read them from the configuration file pch_looking_glass_cli_config.conf

    script_args: Input arguments
    config_file: The configuration file. Default value pch_looking_glass_cli_config.conf
    """
    LOGGER.debug("script_args: %s config_file: %s", script_args, config_file)

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
        "--ixp",
        env_var="IXP",
        required=False,
        type=str,
        help="IXP",
    )
    conf.add(
        "--ixp-city",
        env_var="IXP_CITY",
        required=False,
        type=str,
        help="The city of the IXP",
    )
    conf.add(
        "--ixp-country",
        env_var="IXP_COUNTRY",
        required=False,
        type=str,
        help="The country of the IXP",
    )
    conf.add(
        "--ixp-ip-version",
        env_var="IXP_IP_VERSION",
        required=False,
        choices=["ipv4", "ipv6"],
        help="The IPv summary of the IXP",
    )
    conf.add(
        "--cache-dir",
        env_var="CACHE_DIR",
        required=False,
        type=str,
        help="The cache directory to store any cached info",
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

    return conf.parse_args(script_args)
