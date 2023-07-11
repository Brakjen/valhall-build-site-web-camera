import utils

import pandas as pd
import streamlit as st

from PIL import Image
from streamlit_autorefresh import st_autorefresh


REFRESH_EVERY_N_MINUTES = 10

st.set_page_config(
    page_title="Valhall Build Site Web Camera",
    layout="wide",
    page_icon=Image.open("akerbp_logo.png")
)

# Apply some custom style formatting
st.markdown(utils.CUSTOM_STYLE_BIG_FONT, unsafe_allow_html=True)
st.markdown(utils.CUSTOM_STYLE_CENTERED_H2, unsafe_allow_html=True)
st.markdown(utils.CUSTOM_STYLE_CENTERED_H3, unsafe_allow_html=True)

# Start the autorefresh counter
counter = st_autorefresh(
    interval=1000 * 60 * REFRESH_EVERY_N_MINUTES,
    limit=None,
    key="webcam-counter"
)

# Add title and timestamps
now = pd.Timestamp.now(tz="CET")
next_query = (now + pd.Timedelta(minutes=REFRESH_EVERY_N_MINUTES)).replace(microsecond=0, tzinfo=None).strftime("%Y-%m-%d %H:%M")
last_capture = utils.get_capture_time()

st.markdown(f'<p class="big-font">Valhall Build Site Web Camera', unsafe_allow_html=True)
st.markdown(f"## Image taken {last_capture}{utils.whitespace(40)}{utils.whitespace(40)}Next query {next_query}")

# Try to fetch the latest image
try:
    utils.download_image()

    # Wrap in middle of three columns to emulate a centered image.
    # It works-ish
    with st.columns((0.1, 0.8, 0.1))[1]:
        st.image("build_site.jpg", width=1920)
except Exception:
    with st.columns((0.1, 0.8, 0.1))[1]:
        st.image("error.jpg", width=1920)

st.markdown("### Deployed to [Streamlit Cloud](https://streamlit.io/cloud). Visit code on [Github](https://github.com/Brakjen/valhall-build-site-web-camera).")