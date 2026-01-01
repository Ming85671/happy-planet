import streamlit as st
from PIL import Image

st.set_page_config(layout="wide")

st.markdown(
    """
    <style>
        .title { font-size: 64px; color: red; text-align: center; font-weight: 800; }
        .text  { font-size: 28px; color: blue; text-align: center; }
    </style>

    <div class="title">快乐星球 网站</div>
    <div class="text">欢迎 Yiwen 来到 快乐星球 网站！</div>
    <div class="text">祝 Yiwen 元旦快乐，2026财源滚滚！</div>
    """,
    unsafe_allow_html=True
)

@st.cache_data
def load_image(path: str):
    return Image.open(path)

col1, col2 = st.columns(2, gap="large")
with col1:
    st.image(load_image("images/Yiwen1.jpg"), use_container_width=True)
with col2:
    st.image(load_image("images/Yiwen2.jpg"), use_container_width=True)
