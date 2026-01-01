import streamlit as st
from PIL import Image

st.set_page_config(layout="wide", initial_sidebar_state="expanded")

# ✅ 用来验证网页确实跑的是新代码
st.error("BUILD: 2026-01-01")

def fix_exif_orientation(img: Image.Image) -> Image.Image:
    # 放函数里导入，最稳
    from PIL import ImageOps as _ImageOps
    try:
        return _ImageOps.exif_transpose(img)
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

# ✅ 下拉框放在正文里：一定看得到
st.subheader("Yiwen1 图片方向调整（试试 左转90° / 右转90° / 翻转）")
mode = st.selectbox(
    "选择 Yiwen1 的处理方式：",
    ["不额外处理", "左转90°", "右转90°", "旋转180°", "水平翻转", "垂直翻转"],
    index=0
)

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

