import streamlit as st

# 用 markdown 和 CSS 自定义样式
st.markdown(
    """
    <style>
        .title { font-size: 100px; color: red; text-align: center; }
        .text { font-size: 40px; color: blue; text-align: center; }
        .photo-container { display: flex; justify-content: center; gap: 20px; }
        .photo-container img { width: 45%; }
    </style>
    <div class="title">快乐星球 网站</div>
    <div class="text">欢迎 Yiwen 来到 快乐星球 网站！</div>
    <div class="text">祝 Yiwen 元旦快乐，2026财源滚滚！</div>

    <!-- 两张图片并排放置 -->
    <div class="photo-container">
        <img src="images/Yiwen1.jpg" alt="Yiwen1">
        <img src="images/Yiwen2.jpg" alt="Yiwen2">
    </div>
    """,
    unsafe_allow_html=True
)

# 使用 st.cache_data() 缓存图片资源
@st.cache_data
def load_image(image_path):
    return image_path

# 显示图片并调整大小以适应列宽
image1 = load_image('images/Yiwen1.jpg')
image2 = load_image('images/Yiwen2.jpg')

st.image(image1, use_column_width=True)
st.image(image2, use_column_width=True)
