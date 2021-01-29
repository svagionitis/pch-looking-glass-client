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


def parse_select_tag(html, sort_by):
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
    sort_by: Sort the IPX routers by IPX, city or country.
    """

    routers = []

    soup = BeautifulSoup(html, "html.parser")

    if sort_by == "ipx":
        class_attr = "router_sort_ixp"
    elif sort_by == "city":
        class_attr = "router_sort_city"
    elif sort_by == "country":
        class_attr = "router_sort_country"

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


def get_ipx_rooters(url="https://www.pch.net/tools/looking_glass", sort_by="ipx"):
    """
    Get the IPX routers

    url: The URL to get the IPX routers. Default value is https://www.pch.net/tools/looking_glass
    sort_by: Sort the IPX routers by IPX, city or country. Default value is ipx.
    """
    LOGGER.info("url: %s sort_by: %s", url, sort_by)

    sort_by_options = ["ipx", "city", "country"]
    if sort_by not in sort_by_options:
        LOGGER.error("Option %s is not valid for sorting routers.")
        return None

    looking_glass_html = get_html_text(url)

    routers = parse_select_tag(looking_glass_html, sort_by)

    LOGGER.info(routers)

    return routers


def get_html_text(url, user_agent="pch_looking_glass_cli.py"):
    """
    Get the HTML text of a URL

    url: The URL to get the HTML text
    user_agent: The User Agent header to use. Default value is "pch_looking_glass_cli.py"
    """
    LOGGER.info(url)

    headers = {"User-Agent": user_agent}

    try:
        get_url = requests.get(url, headers=headers)

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

    ipx_routers = get_ipx_rooters(sort_by="ipx")
    save_data_to_json_file(ipx_routers, "./", "ipx_routers.json")

    time.sleep(random.randrange(60, 120))

    city_routers = get_ipx_rooters(sort_by="city")
    save_data_to_json_file(city_routers, "./", "city_routers.json")

    time.sleep(random.randrange(60, 120))

    country_routers = get_ipx_rooters(sort_by="country")
    save_data_to_json_file(country_routers, "./", "country_routers.json")


if __name__ == "__main__":
    main()
