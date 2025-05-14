import streamlit as st
from streamlit_folium import st_folium
import folium
import pandas as pd
import altair as alt
import requests

st.set_page_config(layout="wide", page_title="🌿 Eucalyptus AI Dashboard")

# === Style ===
st.markdown("""
<style>
    .big-title { font-size: 2.5em; font-weight: bold; color: #2E7D32; }
    .metric-box {
        border: 1px solid #ddd; padding: 15px;
        border-radius: 15px; background-color: #f1f8e9;
        box-shadow: 2px 2px 8px #ccc;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# === Header ===
col1, col2 = st.columns([1, 5])
with col1:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/f/f7/SCG_Packaging_logo.svg/512px-SCG_Packaging_logo.svg.png", width=80)
with col2:
    st.markdown("<div class='big-title'>Eucalyptus Land Suitability AI</div>", unsafe_allow_html=True)

st.markdown("## 🌱 ระบบประเมินพื้นที่ปลูกไม้เศรษฐกิจแบบแม่นยำด้วย AI และภาพถ่ายดาวเทียม")

# === Animation (Lottie) ===
lottie_url = "https://assets3.lottiefiles.com/packages/lf20_touohxv0.json"
lottie_json = requests.get(lottie_url).json()
st.components.v1.html(f"""
<div style="width:150px; margin:auto;">
    <script src="https://unpkg.com/@lottiefiles/lottie-player@latest/dist/lottie-player.js"></script>
    <lottie-player src="{lottie_url}" background="transparent" speed="1" style="width: 150px; height: 150px;" loop autoplay></lottie-player>
</div>
""", height=160)

# === Summary Cards ===
col1, col2, col3 = st.columns(3)
with col1: st.markdown("<div class='metric-box'><h4>Suitability</h4><h2>84</h2></div>", unsafe_allow_html=True)
with col2: st.markdown("<div class='metric-box'><h4>พื้นที่เป้าหมาย</h4><h2>7,500 ไร่</h2></div>", unsafe_allow_html=True)
with col3: st.markdown("<div class='metric-box'><h4>จังหวัด</h4><h2>กาญจนบุรี</h2></div>", unsafe_allow_html=True)

# === Map ===
st.markdown("### 🗺️ แผนที่พื้นที่เหมาะสม")
m = folium.Map(
    location=[14.02, 99.53],
    zoom_start=8,
    tiles="https://api.maptiler.com/maps/hybrid/256/{z}/{x}/{y}.jpg?key=sBsPycUuqDYYrp3htoRi",
    attr="MapTiler"
)
folium.Marker([14.02, 99.53], popup="พื้นที่เป้าหมาย", icon=folium.Icon(color="green")).add_to(m)
st_data = st_folium(m, width=1100, height=500)

# === Chart ===
st.markdown("### 📊 พื้นที่เป้าหมายเปรียบเทียบ")
df = pd.DataFrame({
    "จังหวัด": ["กาญจนบุรี", "ราชบุรี", "ขอนแก่น", "ชัยนาท"],
    "พื้นที่ (ไร่)": [7500, 6400, 8300, 5900]
})
chart = alt.Chart(df).mark_bar().encode(x="จังหวัด", y="พื้นที่ (ไร่)", color="จังหวัด").properties(height=300)
st.altair_chart(chart, use_container_width=True)

