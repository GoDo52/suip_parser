import requests

from bs4 import BeautifulSoup

from random import choice

from typing import List, Union

import re


# ======================================================================================================================


def validate_domain_name(domain: str) -> bool:
    """
    Validates if the provided string is a structured domain name.

    Args:
    domain (str): The domain name to validate.

    Returns:
    bool: True if the domain name is valid based on structure, False otherwise.
    """
    pattern = r"^(?!-)([A-Za-z0-9-]{1,63}(?<!-)\.)+[A-Za-z]{2,6}$"

    return bool(re.fullmatch(pattern, domain))


def status_code_checker(domain: str) -> int | None:
    domain = 'http://' + domain.removeprefix("http://").removeprefix("https://")

    try:
        response = requests.get(url=domain, timeout=1)
        return response.status_code
    except requests.exceptions.RequestException as e:
        response_text = f"Failed to connect to {domain}: {e}"
        return None


# ======================================================================================================================


def load_proxies():
    proxies = []
    try:
        with open('proxy.txt', 'r') as file:
            for line in file:
                line = line.strip()
                if line:
                    ip, port, username, password = line.split(':')
                    proxies.append(f"http://{username}:{password}@{ip}:{port}")
    except FileNotFoundError:
        print("The proxy file was not found.")
    except Exception as e:
        print(f"Failed to load proxies: {e}")
    return proxies


def parse_suip_biz(url, act, proxies):
    """
    Parses the given URL based on the action ('findomain' or 'subfinder') from suip.biz using a rotating proxy.

    Args:
    url (str): URL to be parsed.
    act (str): Action type, 'findomain' or 'subfinder'.
    proxies (list): List of proxies to use.

    Returns:
    list: A list of parsed subdomains formatted with 'http://', or an error code (1).
    """
    params = {
        'act': act,
    }
    files = {
        'url': (None, url),
        'Submit1': (None, 'Submit'),
    }
    proxy = {'http': choice(proxies)}

    try:
        response = requests.post('https://suip.biz/', params=params, files=files, proxies=proxy)
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return 1

    soup = BeautifulSoup(response.text, "html.parser")
    raw_list = soup.find("pre").text

    subdomains_list = []
    match act:
        case "findomain":
            search_marker_index = raw_list.rfind('🔍')
            job_marker_index = raw_list.rfind('Job')
            filtered_text = raw_list[search_marker_index + 1:job_marker_index]
            subdomains_list = filtered_text.split("\n")[3:-2]
        case "subfinder":
            subdomains_list = raw_list.split("\n")[:-1]

    subdomains_list = [f"{sub.strip()}" for sub in subdomains_list if sub.strip()]
    return subdomains_list


def get_subdomains(url: str) -> Union[List[str], int]:
    """
    Retrieves subdomains for a given URL either from a database or by making HTTP requests.

    Args:
    url (str): The URL to fetch subdomains for.

    Returns:
    List[str] | int: Returns a list of subdomains if successful, or an HTTP status code if requests fail.
    """
    try:
        normalized_url = url.removeprefix("http://").removeprefix("https://")
        first_subdomains_list = parse_suip_biz(normalized_url, "findomain")
        second_subdomains_list = parse_suip_biz(normalized_url, "subfinder")

        subdomains_list = list(set(first_subdomains_list + second_subdomains_list))

        return subdomains_list

    except requests.exceptions.RequestException as e:
        print(f'Request failed: {e}')
        return e.response.status_code
    except Exception as e:
        print(f'An error occurred: {e}')
        return []


if __name__ == '__main__':
    # print(parse_suip_biz("Layerzero.network", "findomain"))
    # print(parse_suip_biz("Layerzero.network", "subfinder"))
    # print(load_proxies())
    ...
