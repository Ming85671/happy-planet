import streamlit as st
import streamlit.components.v1 as components
from PIL import Image

st.set_page_config(layout="wide")


# =========================
# 1) 两侧少量飘落动画（不会挡住手机下滑）
#    关键：canvas 插到 window.top.document，不再把 iframe 固定覆盖页面
# =========================
falling_overlay_html = r"""
<!doctype html>
<html>
<head>
  <meta charset="utf-8" />
  <style>
    html, body { margin:0; padding:0; background:transparent; }
  </style>
</head>
<body>
<script>
(function () {
  // 防止 Streamlit 反复 rerun 生成多个 canvas
  const OVERLAY_ID = "hp-fall-overlay";

  let topWin = window;
  let topDoc = document;
  try {
    topWin = window.top;
    topDoc = window.top.document;
  } catch (e) {
    // 如果跨域访问失败，就直接不做全屏覆盖（避免影响滚动）
    return;
  }

  // 如果已存在，先移除
  const old = topDoc.getElementById(OVERLAY_ID);
  if (old) old.remove();

  // 创建覆盖层
  const overlay = topDoc.createElement("div");
  overlay.id = OVERLAY_ID;
  overlay.style.position = "fixed";
  overlay.style.inset = "0";
  overlay.style.zIndex = "9999";
  overlay.style.pointerEvents = "none";  // 不拦截触控/滚动
  overlay.style.background = "transparent";
  overlay.style.overflow = "hidden";

  const canvas = topDoc.createElement("canvas");
  canvas.style.width = "100%";
  canvas.style.height = "100%";
  canvas.style.pointerEvents = "none";
  overlay.appendChild(canvas);
  topDoc.body.appendChild(overlay);

  const ctx = canvas.getContext("2d");

  const symbols = ["🧧", "🪙", "💰", "✨"];
  const particles = [];

  // ✅ 少量 + 只在两侧
  const isMobile = topWin.matchMedia && topWin.matchMedia("(max-width: 768px)").matches;

  const DENSITY   = isMobile ? 10 : 16;     // 同屏数量
  const SPAWN_RATE= isMobile ? 0.045 : 0.06;// 生成频率
  const BASE_SPEED= isMobile ? 0.9 : 1.0;   // 速度
  const WIND      = 0.18;                   // 横向飘动
  const SIDE_BAND = isMobile ? 0.14 : 0.16; // 左右两侧各占屏幕宽度比例（越小越靠边）
  const CENTER_PROB = 0.0;                  // 中间概率（想完全不在中间就 0）

  function rand(a, b) { return a + Math.random() * (b - a); }

  function resize() {
    const dpr = topWin.devicePixelRatio || 1;
    canvas.width = Math.floor(topWin.innerWidth * dpr);
    canvas.height = Math.floor(topWin.innerHeight * dpr);
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  }

  function pickX() {
    if (Math.random() < CENTER_PROB) return rand(0, topWin.innerWidth);
    const left = Math.random() < 0.5;
    if (left) return rand(0, topWin.innerWidth * SIDE_BAND);
    return rand(topWin.innerWidth * (1 - SIDE_BAND), topWin.innerWidth);
  }

  function spawn(initial=false) {
    const s = symbols[Math.floor(Math.random() * symbols.length)];
    const size = rand(isMobile ? 16 : 18, isMobile ? 26 : 30);
    const x = pickX();
    const y = initial ? rand(0, topWin.innerHeight) : -rand(10, 80);
    const vy = rand(BASE_SPEED, BASE_SPEED + (isMobile ? 1.8 : 2.2));
    const vx = rand(-WIND, WIND);
    const rot = rand(-0.6, 0.6);
    const vr  = rand(-0.012, 0.012);
    const alpha = rand(0.75, 1.0);
    particles.push({ s, x, y, size, vy, vx, rot, vr, alpha });
  }

  function step() {
    ctx.clearRect(0, 0, topWin.innerWidth, topWin.innerHeight);

    const t = Date.now() * 0.001;
    const windNow = Math.sin(t) * 0.22;

    for (let i = particles.length - 1; i >= 0; i--) {
      const p = particles[i];
      p.x += p.vx + windNow;
      p.y += p.vy;
      p.rot += p.vr;

      ctx.save();
      ctx.globalAlpha = p.alpha;
      ctx.translate(p.x, p.y);
      ctx.rotate(p.rot);
      ctx.font = `${p.size}px "Apple Color Emoji","Segoe UI Emoji","Noto Color Emoji",sans-serif`;
      ctx.textAlign = "center";
      ctx.textBaseline = "middle";
      ctx.fillText(p.s, 0, 0);
      ctx.restore();

      if (p.y > topWin.innerHeight + 80 || p.x < -80 || p.x > topWin.innerWidth + 80) {
        particles.splice(i, 1);
      }
    }

    if (particles.length < DENSITY || Math.random() < SPAWN_RATE) spawn(false);
    topWin.requestAnimationFrame(step);
  }

  // 初始化
  resize();
  for (let i = 0; i < DENSITY; i++) spawn(true);

  // 被动监听，避免影响滚动
  topWin.addEventListener("resize", resize, { passive: true });

  step();
})();
</script>
</body>
</html>
"""

# 让组件只占 1px，不影响布局/滚动
components.html(falling_overlay_html, height=1)


# =========================
# 2) 图片读取 + EXIF 方向纠正
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
# 3) 样式 + 手机端竖排 + 可下滑
# =========================
st.markdown(
    """
    <style>
      .text  { font-size: 28px; color: #1f5cff; text-align: center; margin: 6px 0; }
      .img-spacer { height: 40px; }

      /* ✅ 手机端：把 columns 竖排 */
      @media (max-width: 768px) {
        div[data-testid="stHorizontalBlock"] {
          flex-direction: column !important;
          gap: 1rem !important;
        }
        div[data-testid="column"] {
          width: 100% !important;
          flex: 1 1 100% !important;
        }
      }
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
# 5) 正文 + 图片（桌面并排，手机竖排可下滑）
# =========================
st.markdown(
    """
    <div class="text">欢迎 Yang 来到 快乐星球 网站！</div>
    <div class="text">祝 Yang 元旦快乐，2026财源滚滚！</div>
    <div class="img-spacer"></div>
    """,
    unsafe_allow_html=True
)

image1 = load_image("images/Yang6.jpg")
image2 = load_image("images/Yang8.jpg")

col1, col2 = st.columns(2, gap="large")
with col1:
    st.image(image1, use_container_width=True)
with col2:
    st.image(image2, use_container_width=True)






