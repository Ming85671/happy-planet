import streamlit as st
from PIL import Image

st.set_page_config(layout="wide", initial_sidebar_state="expanded")

# —— 超显眼版本号：用来确认网页跑的是不是这份代码 ——
st.error("BUILD: 2026-01-01  (如果你看不到这行，说明没有跑到新代码)")

def fix_exif_orientation(img: Image.Image) -> Image.Image:
    # 函数内导入，避免任何 ImageOps 名称问题
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

# —— 控制条放在页面正文里：不依赖侧边栏入口，一定看得见 ——
st.subheader("Yiwen1 图片方向调整（试试 左转90° / 右转90° / 翻转）")
mode = st.selectbox(
    "选择 Yiwen1 的处理方式：",
    ["不额外处理", "左转90°", "右转90°", "旋转180°", "水平翻转", "垂直翻转"],
    index=0
)

# 标题与文字
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
