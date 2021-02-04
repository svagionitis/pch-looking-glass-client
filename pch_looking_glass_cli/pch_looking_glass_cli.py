"""
A PCH looking glass tool (https://www.pch.net/tools/looking_glass/) client
"""

import logging
import json
import os
import re
import sys
from utils import setup_logging, save_data_to_json_file
from web_utils import get_request_text, parse_select_tag
from config_arg import parse_input_args
from pch_looking_glass_query import get_ixp_router_query_summary

LOGGER = logging.getLogger(__name__)


def get_ixp_rooters(
    cached_dir=".",
    cached_filename="cached_ixp_routers.json",
    force_retrieve=False,
    url="https://www.pch.net/tools/looking_glass",
):
    """
    Get the IXP routers

    We save the IXP routers in a json file and use this one to get information from a specific router.
    In this way we don't perform yet another request to the web page to retrieve them each time.

    cached_dir: The directory to save the cached list of ixp routers. Default value ".".
    cached_filename: The filename of the cached list of ixp routers. Default value "cached_ixp_routers.json".
    force_retrieve: A flag to force the retrieve of the list of routers. Default value is False.
    url: The URL to get the list of IXP routers. Default value is https://www.pch.net/tools/looking_glass
    """
    LOGGER.debug(
        "cacher_dir: %s cached_filename: %s url: %s", cached_dir, cached_filename, url
    )

    cached_json_filename = os.path.join(cached_dir, cached_filename)
    # Check if cached ixp routers exist
    if os.path.exists(cached_json_filename) and not force_retrieve:
        # If exists, then read from the file
        with open(cached_json_filename, "r") as cached_json_file:
            routers = json.load(cached_json_file)
    else:
        # If it does not exist, download and save it
        looking_glass_html = get_request_text(url)
        routers = parse_select_tag(looking_glass_html)
        save_data_to_json_file(routers, cached_dir, cached_filename)

    LOGGER.debug(routers)

    return routers


def get_router_summary(ixp, city, country, ip_version):
    """
    Get the summary for a specific router with IXP, city, country and IP version

    ixp: The IXP of the router
    city: The city located.
    country: The country located.
    ip_version: The IP version of the summary. Available values are "ipv4" or "ipv6"
    """
    LOGGER.info(
        "ixp: %s city: %s country: %s ip_version: %s", ixp, city, country, ip_version
    )

    # Step 1: Get all the IXP routers which comes as id, ixp, city, country
    routers = get_ixp_rooters()

    # Step 2: Search the list of routers if the specific ixp, city, country router exists
    router_found = next(
        (
            router
            for router in routers
            if router["ixp"] == ixp
            and router["city"] == city
            and router["country"] == country
        ),
        None,
    )
    if router_found is None:
        LOGGER.error(
            "No router with ixp: %s city: %s and country: %s found.", ixp, city, country
        )
        return None

    LOGGER.debug(router_found)

    # Step 3: If the specific router exists, use the id to make a query for the summary
    router_summary = get_ixp_router_query_summary(router_found["id"], ip_version)

    LOGGER.debug(router_summary)

    return router_summary


def parse_router_summary(summary):
    """
    Get specific information from the router summary

    The specific information to retrieve are
    * Route Server local ASN
    * Number of RIB entries
    * Number of Peers
    * Total number of neighbors

    summary: The router summary to parse in order to get specific information
    """
    LOGGER.debug("summary: %s", summary)

    router_summary = {}

    # Clean up the summary, replace multiple occurences of white spaces
    # and strip the start and end of the string
    clean_up_summary = re.sub(r"(\s)(?=\1)", "", summary.strip())

    router_summary["ixp_local_asn"] = int(
        re.search(r"local AS number (\d+)", clean_up_summary).group(1)
    )
    router_summary["ixp_rib_entries"] = int(
        re.search(r"RIB entries (\d+)", clean_up_summary).group(1)
    )
    router_summary["ixp_number_of_peers"] = int(
        re.search(r"Peers (\d+)", clean_up_summary).group(1)
    )
    router_summary["ixp_number_of_neighbors"] = int(
        re.search(r"Total number of neighbors (\d+)", clean_up_summary).group(1)
    )

    LOGGER.debug(router_summary)

    return router_summary


def get_specific_information_for_router(ixp, city, country, ip_version):
    """
    Get specific information for the specific router

    The specific information to retrieve are
    * Route Server local ASN
    * Number of RIB entries
    * Number of Peers
    * Total number of neighbors

    ixp: The IXP of the router
    city: The city located.
    country: The country located.
    ip_version: The IP version of the summary. Available values are "ipv4" or "ipv6"
    """
    router_info = {}

    router_info["ixp"] = ixp
    router_info["ixp_city"] = city
    router_info["ixp_country"] = country
    router_info["ixp_ip_version"] = ip_version

    summary = get_router_summary(ixp, city, country, ip_version)

    summary_info = parse_router_summary(summary)
    router_info.update(summary_info)

    LOGGER.debug(router_info)

    return router_info


def main():
    """
    Main function
    """

    config = parse_input_args(sys.argv[1:])
    LOGGER.info(config)

    if not config.log_level:
        setup_logging("info")
    else:
        setup_logging(config.log_level)

    result = get_specific_information_for_router(
        config.ixp, config.ixp_city, config.ixp_country, config.ixp_ip_version
    )

    print(result)


if __name__ == "__main__":
    main()
