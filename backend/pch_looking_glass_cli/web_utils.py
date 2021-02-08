"""
Some functions regarding web, such as making requests and parsing html pages
"""

import logging
import requests
from bs4 import BeautifulSoup

LOGGER = logging.getLogger(__name__)


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
    LOGGER.debug("html: %s class_attr: %s", html, class_attr)

    data = []

    soup = BeautifulSoup(html, "html.parser")

    option_tags = soup.find("select", class_=class_attr).find_all("option")
    if option_tags is None:
        LOGGER.error("Error finding the select or option tag")
        return None

    for option_tag in option_tags:
        option = {}

        option["id"] = option_tag.get("value")

        option_triplet = option_tag.text.split(",")
        option["ixp"] = option_triplet[0].strip()
        option["city"] = option_triplet[1].strip()
        option["country"] = option_triplet[2].strip()

        data.append(option)

    LOGGER.debug(data)

    return data
