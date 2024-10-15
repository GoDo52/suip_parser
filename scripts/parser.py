import requests

from bs4 import BeautifulSoup

from random import choice

from database.db import Proxy


# ======================================================================================================================


def status_code_checker(domain: str) -> int | None:
    domain = 'http://' + domain.removeprefix("http://").removeprefix("https://")

    try:
        response = requests.get(url=domain, timeout=1)
        return response.status_code
    except requests.exceptions.RequestException as e:
        response_text = f"Failed to connect to {domain}: {e}"
        return None


def load_proxies():
    proxies = Proxy().proxies_list
    proxies_final = []
    for i in proxies:
        try:
            ip, port, username, password = i[0].split(':')
            proxies_final.append(f"http://{username}:{password}@{ip}:{port}")
        except Exception as e:
            print(f"Error in loading proxy: {i}, with error: {e}")
    return proxies_final


def check_proxies():
    proxies = Proxy().proxies_list
    proxies_final_good = []
    proxies_final_bad = []
    for i in proxies:
        try:
            ip, port, username, password = i[0].split(':')
            proxy = f"http://{username}:{password}@{ip}:{port}"
            if is_proxy_working(proxy):
                proxies_final_good.append(i[0])
            else:
                proxies_final_bad.append(i[0])
        except Exception as e:
            proxies_final_bad.append(i[0])
            print(f"Error in checking proxy: {i}, with error: {e}")
    return proxies_final_good, proxies_final_bad


def is_proxy_working(proxy):
    """
    Test if the given proxy is working by attempting a GET request through the proxy.

    Args:
    proxy (str): The proxy URL.

    Returns:
    bool: True if the proxy is working, False otherwise.
    """
    headers = {
        "User-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36",
        'Accept': 'application/json',
        'Connection': 'keep-alive',
        'Accept-Encoding': 'gzip, deflate, br'
    }
    proxies = {
        'http': proxy,
        'https': proxy
    }
    test_url = 'https://httpbin.org/ip'

    try:
        response = requests.get(test_url, proxies=proxies, headers=headers, timeout=3)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        return True
    except requests.exceptions.RequestException as e:
        print(f"Proxy failed with error: {e}")
        return False


# ======================================================================================================================


def parse_suip_biz(url, act, proxy):
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
    proxy = {'http': proxy, 'https': proxy}
    headers = {
        "User-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36",
        'Accept': 'application/json',
        'Connection': 'keep-alive',
        'Accept-Encoding': 'gzip, deflate, br'
    }

    try:
        response = requests.post('https://suip.biz/ru/', params=params, files=files, proxies=proxy, headers=headers)
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


def get_subdomains(url: str):
    """
    Retrieves subdomains for a given URL either from a database or by making HTTP requests.

    Args:
    url (str): The URL to fetch subdomains for.

    Returns:
    Returns a list of subdomains if successful, or an HTTP status code if requests fail.
    """
    proxies = load_proxies()
    proxy = choice(proxies)

    try:
        normalized_url = url.removeprefix("http://").removeprefix("https://")
        first_subdomains_list = parse_suip_biz(normalized_url, "findomain", proxy)
        second_subdomains_list = parse_suip_biz(normalized_url, "subfinder", proxy)

        subdomains_list = set(first_subdomains_list + second_subdomains_list)

        return subdomains_list

    except requests.exceptions.RequestException as e:
        print(f'Request failed: {e}')
        return e.response.status_code
    except Exception as e:
        print(f'An error occurred: {e}')
        return []


if __name__ == '__main__':
    # print(parse_suip_biz("Layerzero.network", "findomain", load_proxies()))
    # print(parse_suip_biz("Layerzero.network", "subfinder", load_proxies()))
    print(get_subdomains("Layerzero.network"))
    # print(load_proxies())
    ...
