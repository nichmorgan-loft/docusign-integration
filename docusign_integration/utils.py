from typing import Any, Dict
import urllib.parse as urlparse


def get_url_params(url: str) -> Dict[str, Any]:
    return urlparse.parse_qs(urlparse.urlparse(url).query)
