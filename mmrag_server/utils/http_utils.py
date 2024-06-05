import os
from urllib.parse import urljoin


def merge_url(host: str, url: str):
    if url.startswith("http://") or url.startswith("https://"):
        return url
    else:
        return urljoin(host, url)
    
    
def merge_path(host: str, url: str):
    return os.path.join(host, url)