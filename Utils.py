from requests import get
from requests.exceptions import RequestException
from contextlib import closing

def get_site_content(url):
    try:
        with closing(get(url, stream=True)) as res:
            if is_good_resp(res):
                return res.content
            else:
                return None
    except RequestException as e:
        logError(e)
        return None

def is_good_resp(resp):
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200 and content_type is not None and content_type.find('html') > -1)

def logError(e):
    print(e)
