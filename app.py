import streamlit as st
from PIL import Image

st.set_page_config(layout="wide")

def exif_orientation_value(img: Image.Image):
    try:
        exif = img.getexif()
        return exif.get(274)
    except Exception:
        return None

def fix_exif_orientation(img: Image.Image) -> Image.Image:
    try:
        from PIL import ImageOps
        return ImageOps.exif_transpose(img)
    except Exception:
        return img

def apply_transform(img: Image.Image, mode: str) -> Image.Image:
    if mode == "不额外处理":
        return img
    if mode == "左转90°":
        return img.rotate(90, expand=True)
    if mode == "右转90°":
        return img.rotate(-90, expand=True)
    if mode == "旋转180°":
        return img.rotate(180, expand=True)
    if mode == "水平翻转":
        return img.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    if mode == "垂直翻转":
        return img.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
    return img

@st.cache_data
def load_image(path: str, mode: str) -> Image.Image:
    with Image.open(path) as im:
        im = fix_exif_orientation(im)
        im = apply_transform(im, mode)
        return im.copy()

# ✅ 把控制条放在页面上方（一定看得见）
st.subheader("Yiwen1 图片方向调整（试试 左转90° / 右转90°）")
mode = st.selectbox(
    "选择 Yiwen1 的处理方式：",
    ["不额外处理", "左转90°", "右转90°", "旋转180°", "水平翻转", "垂直翻转"],
    index=0
)

with Image.open("images/Yiwen1.jpg") as tmp:
    ori_val = exif_orientation_value(tmp)
st.caption(f"Yiwen1 EXIF Orientation(274) = {ori_val}")

# 标题与文字样式
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

image1 = load_image("images/Yiwen1.jpg", mode=mode)
image2 = load_image("images/Yiwen2.jpg", mode="不额外处理")

col1, col2 = st.columns(2, gap="large")
with col1:
    st.image(image1, use_container_width=True)
with col2:
    st.image(image2, use_container_width=True)
