import streamlit as st
from PIL import Image  # 这里只保留 Image，ImageOps 放到函数里再导入，最稳

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
    # ✅ 函数内导入，避免 ImageOps 未定义/被覆盖
    from PIL import ImageOps as _ImageOps

    try:
        return _ImageOps.exif_transpose(img)  # 按 EXIF 自动修正方向
    except Exception:
        # 兜底：手动读 EXIF Orientation
        try:
            exif = img.getexif()
            orientation = exif.get(274)  # 274 = Orientation
            if orientation == 3:
                return img.rotate(180, expand=True)
            elif orientation == 6:  # 顺时针 90°
                return img.rotate(-90, expand=True)
            elif orientation == 8:  # 逆时针 90°
                return img.rotate(90, expand=True)
        except Exception:
            pass
        return img

@st.cache_data
def load_image(path: str, rotate_ccw: int = 0) -> Image.Image:
    # 用 with 确保文件句柄关闭；copy() 确保图像数据读入内存，缓存更稳
    with Image.open(path) as im:
        im = fix_exif_orientation(im)
        if rotate_ccw:
            im = im.rotate(rotate_ccw, expand=True)  # 正数=逆时针；负数=顺时针
        return im.copy()

# 如果 Yiwen1 方向向右歪，一般用逆时针 90° 纠正：把 0 改成 90
image1 = load_image("images/Yiwen1.jpg", rotate_ccw= -90 )
image2 = load_image("images/Yiwen2.jpg", rotate_ccw=0)

col1, col2 = st.columns(2, gap="large")
with col1:
    st.image(image1, use_container_width=True)
with col2:
    st.image(image2, use_container_width=True)
