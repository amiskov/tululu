import backoff
import requests


@backoff.on_exception(backoff.expo,
                      (requests.ConnectionError, requests.Timeout))
def make_request(url: str, params=None) -> requests.Response:
    """Return response of the request to the given `url`.

    Fails if redirect happens.
    """
    resp = requests.get(url, params=params)
    resp.raise_for_status()

    # former `check_for_redirect` function
    if resp.history:
        raise requests.HTTPError('Redirects not allowed.')

    return resp
