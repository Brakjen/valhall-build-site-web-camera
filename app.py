import datetime
import requests

import pandas as pd
import streamlit as st

from PIL import Image
from bs4 import BeautifulSoup
from streamlit_autorefresh import st_autorefresh

# TODO: It it possible to get the timestamp for when the image was taken?


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

st.set_page_config(
    page_title="Valhall Build Site Web Camera",
    layout="wide",
    page_icon=Image.open("akerbp_logo.png")
)

# Style for larger font size and center aligned text
st.markdown("""
<style>
.big-font {
    text-align: center;
    font-size:100px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("<style>h2 {text-align: center;}</style>", unsafe_allow_html=True)

# Start the autorefresh counter
counter = st_autorefresh(
    interval=10 * 1000,
    limit=None,
    key="webcam-counter"
)

# Get current time and write title
now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
st.markdown(f'<p class="big-font">Valhall Build Site Web Camera ({get_capture_time()})', unsafe_allow_html=True)
st.markdown(f"## Last check for new image: {now}")

# Try to fetch the latest image
try:
    download_image()
    with st.columns((0.1, 0.8, 0.1))[1]:
        st.image("build_site.jpg", width=1920 * 2)
except Exception:
    with st.columns((0.1, 0.8, 0.1))[1]:
        st.image("error.jpg", width=1920)