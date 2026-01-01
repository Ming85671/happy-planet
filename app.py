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

def exif_orientation_value(img: Image.Image):
    """读取 EXIF Orientation（274），没有就返回 None"""
    try:
        exif = img.getexif()
        return exif.get(274)
    except Exception:
        return None

def fix_exif_orientation(img: Image.Image) -> Image.Image:
    """优先按 EXIF 自动纠正（能处理旋转+镜像）。如果失败就原样返回。"""
    try:
        from PIL import ImageOps
        return ImageOps.exif_transpose(img)
    except Exception:
        return img

def apply_transform(img: Image.Image, mode: str) -> Image.Image:
    """在 EXIF 纠正后，再进行手动旋转/翻转"""
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
        ori = exif_orientation_value(im)  # 读取原始 EXIF 值（仅用于显示/调试）
        im = fix_exif_orientation(im)
        im = apply_transform(im, mode)
        im = im.copy()
    return im

# —— 左侧给你一个开关，直接在线调到正确方向 ——
st.sidebar.header("Yiwen1 图片方向调整")
mode = st.sidebar.selectbox(
    "选择 Yiwen1 的处理方式（先试试 左转90° / 右转90°）：",
    ["不额外处理", "左转90°", "右转90°", "旋转180°", "水平翻转", "垂直翻转"],
    index=0
)

# 读取图片
with Image.open("images/Yiwen1.jpg") as tmp:
    ori_val = exif_orientation_value(tmp)

st.sidebar.caption(f"Yiwen1 EXIF Orientation(274) = {ori_val}")

image1 = load_image("images/Yiwen1.jpg", mode=mode)
image2 = load_image("images/Yiwen2.jpg", mode="不额外处理")

# 并排显示
col1, col2 = st.columns(2, gap="large")
with col1:
    st.image(image1, use_container_width=True)
with col2:
    st.image(image2, use_container_width=True)
