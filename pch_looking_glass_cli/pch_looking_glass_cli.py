"""
A PCH looking glass tool (https://www.pch.net/tools/looking_glass/) client
"""

import logging
from datetime import datetime
import json
import random
import time
import os
import requests
from bs4 import BeautifulSoup

LOGGER = logging.getLogger(__name__)


def parse_select_tag(html, class_attr="router_sort_ixp"):
    """
    Parse data in the following format

    <select size="12" class="router_sort_country router_sort_stage">
        <option city="Malaysia" value="1">MyIX, Kuala Lumpur, Malaysia</option>
        <option city="Philippines" value="2">PhOpenIX, Manila, Philippines</option>
        <option city="Germany" value="3">DE-CIX Frankfurt, Frankfurt, Germany</option>
        <option city="Lebanon" value="4">BeirutIX, Beirut, Lebanon</option>
        <option city="United States" value="7">NOTA, Miami, United States</option>
        <option city="United States" value="8">Equinix-NY, New York, United States</option>
        <option city="Singapore" value="9">SOX, Singapore, Singapore</option>
        <option city="United Kingdom" value="12">LINX, London, United Kingdom</option>
        <option city="United States" value="13">Any2, Los Angeles, United States</option>
    </select>

    html: The html text to parse in order to get the data.
    class_attr: The class attribute of the select tag to get. Defaul value is "router_sort_ixp".
    """

    routers = []

    soup = BeautifulSoup(html, "html.parser")

    option_tags = soup.find("select", class_=class_attr).find_all("option")
    if option_tags is None:
        LOGGER.error("Error finding the select or option tag")
        return None

    for option_tag in option_tags:
        router = {}

        router["id"] = option_tag.get("value")

        router_triplet = option_tag.text.split(",")
        router["ixp"] = router_triplet[0].strip()
        router["city"] = router_triplet[1].strip()
        router["country"] = router_triplet[2].strip()

        routers.append(router)

    LOGGER.debug(routers)

    return routers


def get_ixp_rooters(url="https://www.pch.net/tools/looking_glass"):
    """
    Get the IXP routers

    url: The URL to get the IXP routers. Default value is https://www.pch.net/tools/looking_glass
    """
    LOGGER.debug("url: %s", url)

    looking_glass_html = get_request_text(url)

    routers = parse_select_tag(looking_glass_html)

    LOGGER.info(routers)

    return routers


def generate_nonce(length=100):
    """
    Generate pseudorandom number.

    See https://github.com/joestump/python-oauth2/blob/master/oauth2/__init__.py#L171
    """

    return "".join([str(random.SystemRandom().randint(0, 9)) for i in range(length)])


def get_ixp_router_query(
    query, args, router_id, url="https://www.pch.net/tools/looking_glass_query"
):
    """
    Get IXP router information using a query in the Looking Glass utility

    query: The query to ask. The available values are "summary", "v6_summary", "prefix", "v6_prefix" and "regex".
    args: The arguments for the query. "summary" and "v6_summary" do not need arguments.
    router_id: The router ID.
    url: The url to send the query. Default value is https://www.pch.net/tools/looking_glass_query
    """
    LOGGER.info("query: %s args: %s router_id: %s url: %s", query, args, router_id, url)

    query_options = ["summary", "v6_summary", "prefix", "v6_prefix", "regex"]
    if query not in query_options:
        LOGGER.error("Query %s is not valid.", query)
        return None

    nonce_generated_cookie = generate_nonce()
    nonce_generated_query = generate_nonce()

    query_params = {
        "query": query,
        "args": args,
        "router": router_id,
        "pch_nonce": nonce_generated_query,
    }

    pch_cookie = "pch_nonce{0}={1}; pch_nonce{2}={3}".format(
        nonce_generated_cookie,
        nonce_generated_cookie,
        nonce_generated_query,
        nonce_generated_query,
    )

    looking_glass_query_json = get_request_text(
        url, params=query_params, cookie=pch_cookie
    )

    LOGGER.info(looking_glass_query_json)

    resp = json.loads(looking_glass_query_json)[0]

    if resp["status"] != "good":
        LOGGER.error("Response status: %s", resp["status"])
        return None

    router_result = resp["result"]

    if router_result == "NA":
        LOGGER.warn("Router not available")
        router_result = ""

    LOGGER.info(router_result)

    return router_result


def get_ixp_router_query_summary(router_id, ip_version="ipv4"):
    """
    Get the IPv4 or IPv6 summary of an IXP router

    router_id: The router ID.
    ip_version: The IP version to get the summary of. Default value is "ipv4".
    """
    LOGGER.debug("router_id: %s ip_version: %s", router_id, ip_version)

    ip_version_options = ["ipv4", "ipv6"]
    if ip_version not in ip_version_options:
        LOGGER.error("IP version %s not valid")
        return None

    if ip_version == "ipv4":
        return get_ixp_router_query("summary", "", router_id)
    elif ip_version == "ipv6":
        return get_ixp_router_query("v6_summary", "", router_id)


def get_router_summary(ixp, city, country, ip_version):
    """
    Get the summary for a specific router with IXP, city and country

    ixp: The IXP of the router
    city: The city located.
    country: The country located.
    ip_version: The IP version of the summary. Available values are "ipv4" or "ipv6"
    """
    LOGGER.debug(
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

    LOGGER.info(router_found)

    # Step 3: If the specific router exists, use the id to make a query for the summary
    router_summary = get_ixp_router_query_summary(router_found["id"], ip_version)

    LOGGER.info(router_summary)

    return router_summary


def get_request_text(
    url, params=None, cookie=None, user_agent="pch_looking_glass_cli.py"
):
    """
    Make a GET request to a URL

    url: The URL to make the GET request
    params: The parameters to pass in the URL. Default value is None.
    cookie: The Cookie header to use. Default value is none.
    user_agent: The User Agent header to use. Default value is "pch_looking_glass_cli.py"
    """
    LOGGER.info(
        "url: %s params: %s cookie: %s user_agent: %s", url, params, cookie, user_agent
    )

    headers = {"User-Agent": user_agent}
    if cookie:
        headers["Cookie"] = cookie

    try:
        get_url = requests.get(url, headers=headers, params=params)

        LOGGER.debug(get_url)

        get_url.raise_for_status()
        get_url.encoding = get_url.apparent_encoding
        return get_url.text
    except requests.exceptions.RequestException as req_ex:
        LOGGER.error("Error getting the URL %s: %s", url, req_ex)
        return None


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


def main():
    """
    Main function
    """

    setup_logging("info")

    get_router_summary("A-IX", "Beirut", "Lebanon", "ipv4")


if __name__ == "__main__":
    main()
