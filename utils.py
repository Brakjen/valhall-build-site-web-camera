import requests
import pandas as pd
from bs4 import BeautifulSoup

CUSTOM_STYLE_BIG_FONT = """
<style>
.big-font {
    text-align: center;
    font-size:80px;
}
</style>
"""

CUSTOM_STYLE_CENTERED_H2 = "<style>h2 {text-align: center;}</style>"
CUSTOM_STYLE_CENTERED_H3 = "<style>h3 {text-align: center;}</style>"
CUSTOM_STYLE_CENTERED_H4 = "<style>h4 {text-align: center;}</style>"

def download_image() -> None:
    """Download web camera image from hent-kamera."""
    url = "https://hent-kamera.no/webkamera/1718_Valhall/K_1/K_1_000M.jpg"
    r = requests.get(url)
    with open("build_site.jpg", "wb") as f:
        f.write(r.content)

def get_capture_time() -> str:
    """Get the Last modified timestamp one level up in the file system."""
    url = "https://hent-kamera.no/webkamera/1718_Valhall/K_1"
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    data = pd.read_html(str(soup.find("table")))[0]
    return data["Last modified"].iloc[2]

def whitespace(n):
    return "&nbsp;"*n