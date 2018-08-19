import urllib.request
import ssl
import json


def load_from_url(url):
    ssl._create_default_https_context = ssl._create_unverified_context
    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read().decode())
    return data
