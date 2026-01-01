import streamlit as st
import streamlit.components.v1 as components
from PIL import Image

st.set_page_config(layout="wide")


# =========================
# 1) 全屏掉落动画（红包/金币）
# =========================
falling_html = """
<!doctype html>
<html>
<head>
  <meta charset="utf-8" />
  <style>
    html, body {
      margin: 0; padding: 0;
      width: 100%; height: 100%;
      background: transparent;
      overflow: hidden;
    }
    canvas {
      position: fixed;
      inset: 0;
      width: 100vw;
      height: 100vh;
      pointer-events: none; /* 不挡住页面点击 */
    }
  </style>
</head>
<body>
  <canvas id="c"></canvas>

  <script>
    // 让这个组件的 iframe 自己变成“全屏覆盖层”
    (function makeOverlay() {
      const fe = window.frameElement;
      if (!fe) return;
      fe.style.position = "fixed";
      fe.style.top = "0";
      fe.style.left = "0";
      fe.style.width = "100vw";
      fe.style.height = "100vh";
      fe.style.border = "0";
      fe.style.zIndex = "9999";
      fe.style.background = "transparent";
      fe.style.pointerEvents = "none"; // iframe 本身也不拦截
    })();

    const canvas = document.getElementById("c");
    const ctx = canvas.getContext("2d");

    const symbols = ["🧧", "🪙", "💰", "✨"];
    const particles = [];

    // 你可以调这些参数：
    const DENSITY = 55;         // 同屏数量（越大越密）
    const SPAWN_RATE = 0.65;    // 每帧生成概率（越大越频繁）
    const BASE_SPEED = 1.2;     // 基础下落速度
    const WIND = 0.35;          // 横向飘动强度

    function resize() {
      const dpr = window.devicePixelRatio || 1;
      canvas.width = Math.floor(innerWidth * dpr);
      canvas.height = Math.floor(innerHeight * dpr);
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    }
    window.addEventListener("resize", resize);
    resize();

    function rand(a, b) { return a + Math.random() * (b - a); }

    function spawn(initial=false) {
      const s = symbols[Math.floor(Math.random() * symbols.length)];
      const size = rand(20, 34);                 // 字号大小
      const x = rand(0, innerWidth);
      const y = initial ? rand(0, innerHeight) : -rand(10, 80);
      const vy = rand(BASE_SPEED, BASE_SPEED + 2.6);
      const vx = rand(-WIND, WIND);
      const rot = rand(-0.6, 0.6);
      const vr = rand(-0.015, 0.015);
      const alpha = rand(0.75, 1.0);

      particles.push({ s, x, y, size, vy, vx, rot, vr, alpha });
    }

    // 初始填充
    for (let i = 0; i < DENSITY; i++) spawn(true);

    function step() {
      ctx.clearRect(0, 0, innerWidth, innerHeight);

      // 轻微“风”随时间变化
      const t = Date.now() * 0.001;
      const windNow = Math.sin(t) * 0.35;

      for (let i = particles.length - 1; i >= 0; i--) {
        const p = particles[i];
        p.x += p.vx + windNow;
        p.y += p.vy;
        p.rot += p.vr;

        // 绘制 emoji
        ctx.save();
        ctx.globalAlpha = p.alpha;
        ctx.translate(p.x, p.y);
        ctx.rotate(p.rot);
        ctx.font = `${p.size}px "Apple Color Emoji","Segoe UI Emoji","Noto Color Emoji",sans-serif`;
        ctx.textAlign = "center";
        ctx.textBaseline = "middle";
        ctx.fillText(p.s, 0, 0);
        ctx.restore();

        // 出界就移除
        if (p.y > innerHeight + 80 || p.x < -80 || p.x > innerWidth + 80) {
          particles.splice(i, 1);
        }
      }

      // 持续生成保持密度
      if (particles.length < DENSITY || Math.random() < SPAWN_RATE) {
        spawn(false);
      }

      requestAnimationFrame(step);
    }

    step();
  </script>
</body>
</html>
"""

# height 给 1 就行，JS 会把 iframe 拉到全屏
components.html(falling_html, height=1)


# =========================
# 2) 读取图片 + 自动纠正方向
# =========================
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


# =========================
# 3) 页面样式
# =========================
st.markdown(
    """
    <style>
        .text  { font-size: 28px; color: #1f5cff; text-align: center; margin: 6px 0; }
        .img-spacer { height: 40px; }  /* ✅ 图片整体下移距离 */
    </style>
    """,
    unsafe_allow_html=True
)


# =========================
# 4) 弧形艺术字标题（SVG）
# =========================
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

      <!-- ✅ 开口向下（∩） -->
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
components.html(title_svg, height=260)


# =========================
# 5) 正文文字 + 图片
# =========================
st.markdown(
    """
    <div class="text">欢迎 Yiwen 来到 快乐星球 网站！</div>
    <div class="text">祝 Yiwen 元旦快乐，2026财源滚滚！</div>
    <div class="img-spacer"></div>
    """,
    unsafe_allow_html=True
)

image1 = load_image("images/Yiwen1.jpg")
image2 = load_image("images/Yiwen2.jpg")

col1, col2 = st.columns(2, gap="large")
with col1:
    st.image(image1, use_container_width=True)
with col2:
    st.image(image2, use_container_width=True)





