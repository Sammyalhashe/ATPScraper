from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup as bs


def get_site_content(url):
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
        return None


def parse_with_soup(resp):
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


def get_parsed_site_content(url):
    """get_parsed_site_content
    Takes a url and returns the BeautifulSoup html parsed version

    :param url: url to parse
    """
    unparsed = get_site_content(url)
    parsed = parse_with_soup(unparsed)
    return parsed


def is_good_resp(resp):
    """is_good_resp
    Checks if the url response is valid

    :param resp: web request response
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200 and content_type is not None
            and content_type.find('html') > -1)


def logError(e):
    """logError
    Function to log any errors that occurr. The implementation should be
    flexible to whatever I want to do when logging errors

    :param e: Error Message
    """
    print(e)
