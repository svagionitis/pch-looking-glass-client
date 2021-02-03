"""
A PCH looking glass tool (https://www.pch.net/tools/looking_glass/) client
"""

import logging
import json
import os
from utils import setup_logging, save_data_to_json_file, generate_nonce
from web_utils import get_request_text, parse_select_tag

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

    LOGGER.info(routers)

    return routers


def get_ixp_router_query(
    query, args, router_id, url="https://www.pch.net/tools/looking_glass_query"
):
    """
    Get IXP router information using a query in the Looking Glass utility

    For more information about the query, have a look at the source of the page https://www.pch.net/tools/looking_glass/. You can see the following:

    ```
    Hello! Are you a coder looking to scrape our looking glass
    information?  If yes, welcome! You've come to the right place.
    First off, this form was not meant for robots to scrape. Please
    consider contacting us and we'd be happy to try and assist you:

            https://www.pch.net/about/contact

    Otherwise, if you insist on scraping us, you'll need to know some
    tidbits to make your life easier:

    * The actual URL that returns results is here:

            https://www.pch.net/tools/looking_glass_query

    * This URL accepts it's parameters via GET, not POST. They are:

            query=QUERYHERE&args=ARGSHERE&router=ROUTERIDHERE&pch_nonce=NONCEHERE

    * This URL will return JSON in this format:

            [{"nonce":"NONCE HERE","status":"STATUS HERE","result":"RESULT HERE"}]

    * We use nonces to prevent CSRF. This means you'll need to pass
    a nonce both in the query string as denoted above *and* in the cookies you
    send with with your GET to looking_glass_query. Here's a snippet we published
    to show how to login using nonces. You should be able to adopt this your uses
    on this page:

            https://github.com/Packet-Clearing-House/gists/blob/master/IMPACT.wget.recursive.sh

    * the result returned in JSON is HTML with "<br />\n" inline

    All this said, even if you're going to scrape us, please do contact us.
    We want to help you!
    ```

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

    pch_cookie = "pch_nonce{0}={0}; pch_nonce{1}={1}".format(
        nonce_generated_cookie,
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
        LOGGER.info("Router not available")
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
        query = "summary"
    elif ip_version == "ipv6":
        query = "v6_summary"

    return get_ixp_router_query(query, "", router_id)


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

    LOGGER.debug(router_found)

    # Step 3: If the specific router exists, use the id to make a query for the summary
    router_summary = get_ixp_router_query_summary(router_found["id"], ip_version)

    LOGGER.debug(router_summary)

    return router_summary


def main():
    """
    Main function
    """

    setup_logging("info")

    get_router_summary("A-IX", "Beirut", "Lebanon", "ipv4")


if __name__ == "__main__":
    main()
