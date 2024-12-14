from urllib.parse import urljoin
import requests
from pathlib import Path

def fetch_file(base_url: str, file_url: str) -> Path:
    dest = Path(file_url)
    dest.parent.mkdir(parents=True, exist_ok=True)
    with dest.open("w") as fp:
        fp.write(requests.get(urljoin(base_url, file_url)).text)
    return dest

def file_contents(file_url: str) -> str:
    dest = Path(file_url)
    return dest.read_text()