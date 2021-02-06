"""
Helpful functions to query the endpoint https://www.pch.net/tools/looking_glass_query
"""

import logging
import json
from utils import generate_nonce
from web_utils import get_request_text

LOGGER = logging.getLogger(__name__)


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

    # The correct result should contain the string "BGP router identifier"
    # If it does not contain it, then there is some kind of error
    if router_result.find("BGP router identifier") == -1:
        LOGGER.warning("Response result: %s", router_result.strip())
        router_result = ""

    LOGGER.debug(router_result)

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
