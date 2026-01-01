import streamlit as st
from PIL import Image, ImageOps

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

def fix_exif_orientation(img: Image.Image) -> Image.Image:
    """优先用 Pillow 的 exif_transpose；不行就按 EXIF Orientation(274) 手动纠正。"""
    try:
        # 推荐方式：自动按 EXIF 修正方向
        return ImageOps.exif_transpose(img)
    except Exception:
        # 兜底：手动读取 EXIF Orientation
        try:
            exif = img.getexif()
            orientation = exif.get(274)  # 274 = Orientation
            if orientation == 3:
                return img.rotate(180, expand=True)
            elif orientation == 6:  # 需要顺时针 90°
                return img.rotate(-90, expand=True)
            elif orientation == 8:  # 需要逆时针 90°
                return img.rotate(90, expand=True)
        except Exception:
            pass
        return img

@st.cache_data
def load_image(path: str, rotate_ccw: int = 0) -> Image.Image:
    img = Image.open(path)
    img = fix_exif_orientation(img)
    if rotate_ccw:
        img = img.rotate(rotate_ccw, expand=True)  # 正数=逆时针；负数=顺时针
    return img

# 如果 Yiwen1 仍然不对，把 rotate_ccw 改成 90 或 -90 试一下
image1 = load_image("images/Yiwen1.jpg", rotate_ccw=0)
image2 = load_image("images/Yiwen2.jpg", rotate_ccw=0)

col1, col2 = st.columns(2, gap="large")
with col1:
    st.image(image1, use_container_width=True)
with col2:
    st.image(image2, use_container_width=True)
