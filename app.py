import streamlit as st
import streamlit.components.v1 as components
from PIL import Image

st.set_page_config(layout="wide")

def fix_exif_orientation(img: Image.Image) -> Image.Image:
    from PIL import ImageOps as _ImageOps
    try:
        return _ImageOps.exif_transpose(img)
    except Exception:
        return img

@st.cache_data
def load_image(path: str) -> Image.Image:
    with Image.open(path) as im:
        im = fix_exif_orientation(im)
        return im.copy()

# ====== 样式（文字 + 图片下移间距） ======
st.markdown(
    """
    <style>
        .text  { font-size: 28px; color: #1f5cff; text-align: center; margin: 6px 0; }
        .img-spacer { height: 40px; } /* ✅ 图片整体下移距离：这里改 60/80 都行 */
    </style>
    """,
    unsafe_allow_html=True
)

# ====== 弧形艺术字标题（用 components.html 渲染 SVG，避免被转义） ======
title_svg = """
<div style="display:flex;justify-content:center;margin-top:10px;">
  <svg viewBox="0 0 1000 300" style="width:min(1100px,96vw);height:240px;">
    <defs>
      <linearGradient id="grad" x1="0%" y1="0%" x2="100%" y2="0%">
        <stop offset="0%"  stop-color="#ff2d2d"/>
        <stop offset="55%" stop-color="#ff7a18"/>
        <stop offset="100%" stop-color="#ffd000"/>
      </linearGradient>

      <filter id="shadow" x="-20%" y="-20%" width="140%" height="140%">
        <feDropShadow dx="0" dy="6" stdDeviation="6" flood-color="rgba(0,0,0,0.35)"/>
      </filter>

      <!-- 开口向下（∩）：两端低，中间高；整体下移避免裁切 -->
      <path id="arcPath" d="M 70 220 Q 500 50 930 220" />
    </defs>

    <text font-size="126"
          font-family="Trebuchet MS, Arial Black, 'Microsoft YaHei', sans-serif"
          font-weight="900"
          fill="url(#grad)"
          stroke="#ffffff"
          stroke-width="7"
          paint-order="stroke fill"
          filter="url(#shadow)">
      <textPath href="#arcPath" startOffset="50%" text-anchor="middle">
        快乐星球 网站
      </textPath>
    </text>
  </svg>
</div>
"""

components.html(title_svg, height=250)

# ====== 正文文字 ======
st.markdown(
    """
    <div class="text">欢迎 Yiwen 来到 快乐星球 网站！</div>
    <div class="text">祝 Yiwen 元旦快乐，2026财源滚滚！</div>
    <div class="img-spacer"></div>
    """,
    unsafe_allow_html=True
)

# ====== 图片（两列并排） ======
image1 = load_image("images/Yiwen1.jpg")
image2 = load_image("images/Yiwen2.jpg")

col1, col2 = st.columns(2, gap="large")
with col1:
    st.image(image1, use_container_width=True)
with col2:
    st.image(image2, use_container_width=True)




