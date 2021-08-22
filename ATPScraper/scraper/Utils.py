from requests import get
from requests.models import Response
from functools import lru_cache
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup as bs
from json import loads
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def get_site_content(url: str) -> str:
    """get_site_content
    returns unparsed html from the url specified

    :param url: the web url
    """
    try:
        with closing(get(url, stream=True)) as res:
            if is_good_resp(res):
                return res.content
            else:
                return None
    except RequestException as e:
        logError(e)
        raise RequestException("Something went wrong with the request")


def get_api_call_content(url: str) -> str:
    try:
        print("url to follow", flush=True)
        print(url, flush=True)
        with closing(get(url, stream=True)) as res:
            if is_good_nonHTML_resp(res):
                logError(res.content.decode("utf-8"))
                return loads(res.content.decode('utf-8'))
            else:
                return None
    except RequestException as e:
        logError(e)
        raise RequestException("Something went wrong with the request")


def parse_with_soup(resp: str) -> bs:
    """parse_with_soup
    Uses BeautifulSoup to parse the html, returns the parsed version
    :param resp: response content from get_site_content
    """
    if resp is not None:
        parsed = bs(resp, 'html.parser')
        return parsed
    else:
        logError("Response is not valid")
        return None

def parse_with_soup_html5lib(resp: str) -> bs:
    """parse_with_soup
    Uses BeautifulSoup to parse the html, returns the parsed version
    with html5lib parser
    :param resp: response content from get_site_content
    """
    if resp is not None:
        parsed = bs(resp, 'html5lib')
        return parsed
    else:
        logError("Response is not valid")
        return None


import logging
logger = logging.getLogger(__name__)

@lru_cache()
def get_parsed_site_content(url: str, default: bool = True) -> bs:
    """get_parsed_site_content
    Takes a url and returns the BeautifulSoup html parsed version

    :param url: url to parse
    """
    logger.debug("THIS IS A URL " + url)
    unparsed = get_site_content(url)
    if default:
        parsed = parse_with_soup(unparsed)
    else:
        parsed = parse_with_soup_html5lib(unparsed)
    return parsed


def is_good_resp(resp: Response) -> bool:
    """is_good_resp
    Checks if the url response is valid

    :param resp: web request response
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200 and content_type is not None
            and content_type.find('html') > -1)


def is_good_nonHTML_resp(resp: Response) -> bool:
    content_type = resp.headers['Content-Type'].lower()
    print(content_type, flush=True)
    print("status code to follow", flush=True)
    print(resp.status_code, flush=True)
    return (resp.status_code == 200 and content_type is not None)


def logError(e):
    """logError
    Function to log any errors that occurr. The implementation should be
    flexible to whatever I want to do when logging errors

    :param e: Error Message
    """
    print(e, flush=True)

def stripContent(s):
    return s.replace('\r', '').replace('\n', '').strip()
