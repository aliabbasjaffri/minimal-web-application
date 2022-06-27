import string
import random
from urllib.parse import urlparse


BASEURL = "http://short.est/"


def random_string_generator(size: int = 6) -> str:
    """
    This function generates a 6 digit random string that serves as a
    temporary hash for this URL. This is NOT A SECURE hash at all and
    serves as a placeholder for now.
    It generates quite a unique string for every URL that it receives.
    26 letters + 10 numbers + 26 letters = 62 total characters
    62 P 6 = 62^6 = almost 57 billion unique values
    :param size: size of the random string being generated
    :return: the random string of size
    """
    return "".join(
        random.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase)
        for _ in range(size)
    )


def valid_base_url(url: str) -> bool:
    """
    This function checks the provided url for valid scheme and
    network location. For more information on these, please check
    the following docs:
    https://docs.python.org/3/library/urllib.parse.html#url-parsing
    :param url: param that needs to be checked for validity
    :return: returns a boolean if the scheme and netloc matches the BASEURL
    """
    return (
        urlparse(BASEURL).scheme == urlparse(url).scheme
        and urlparse(BASEURL).netloc == urlparse(url).netloc
    )
