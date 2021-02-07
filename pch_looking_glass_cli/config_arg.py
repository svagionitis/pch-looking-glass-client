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

    return conf.parse_args(script_args)
