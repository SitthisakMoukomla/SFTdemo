import streamlit as st
from streamlit_folium import st_folium
import folium
import altair as alt
import pandas as pd

# === CONFIG ===
st.set_page_config(layout="wide", page_title="Eucalyptus Land Suitability AI")
st.markdown("""
    <style>
        .main { background-color: #f9f9f9; }
        .block-container { padding-top: 1rem; padding-bottom: 1rem; }
        .stButton>button {
            color: white;
            background-color: #4CAF50;
            border-radius: 8px;
            padding: 0.5em 1em;
        }
    </style>
""", unsafe_allow_html=True)

# === TITLE ===
st.title("🛰️ Eucalyptus Land Suitability AI Dashboard")

# === SIDEBAR ===
with st.sidebar:
    st.header("🔎 เงื่อนไขการค้นหา")
    province = st.selectbox("📍 เลือกจังหวัด", ["กาญจนบุรี", "ราชบุรี", "ขอนแก่น", "ชัยนาท"])
    slope = st.slider("⛰️ ความลาดชัน (%)", 0, 30, (0, 15))
    ndvi = st.slider("🌿 NDVI", 0.0, 1.0, 0.5)
    st.markdown("---")
    st.markdown("👈 ปรับค่าทางซ้ายมือ แล้วดูผลบนแผนที่")

# === CENTER COORDINATES ===
center = {
    "กาญจนบุรี": [14.02, 99.53],
    "ราชบุรี": [13.53, 99.82],
    "ขอนแก่น": [16.43, 102.83],
    "ชัยนาท": [15.18, 100.13]
}[province]

# === MAPTILER ===
MAPTILER_API_KEY = "sBsPycUuqDYYrp3htoRi"  # ✅ ใส่ API key จริง
m = folium.Map(
    location=center,
    zoom_start=9,
    tiles=f"https://api.maptiler.com/maps/hybrid/256/{{z}}/{{x}}/{{y}}.jpg?key={MAPTILER_API_KEY}",
    attr='MapTiler Satellite',
)

# === MARKER MOCK ===
folium.Marker(
    location=center,
    popup=f"พื้นที่เหมาะสมใน {province}",
    icon=folium.Icon(color="green", icon="ok-sign")
).add_to(m)
folium.LayerControl().add_to(m)

# === SHOW MAP ===
st.markdown("## 🗺️ แผนที่พื้นที่เป้าหมาย")
st_data = st_folium(m, width=1200, height=600)

# === ON-CLICK ===
if st_data.get("last_clicked"):
    latlon = st_data["last_clicked"]
    st.success(f"📍 คุณคลิกที่พิกัด: ({latlon['lat']:.4f}, {latlon['lng']:.4f})")

# === SUMMARY ===
st.markdown("## 📊 สรุปเบื้องต้น")
col1, col2, col3 = st.columns(3)
col1.metric("จังหวัด", province)
col2.metric("พื้นที่เป้าหมาย", "ประมาณ 7,500 ไร่")
col3.metric("Suitability Score", "83")

# === CHART SECTION ===
st.markdown("## 📈 การวิเคราะห์พื้นที่")

data = pd.DataFrame({
    "จังหวัด": ["กาญจนบุรี", "ราชบุรี", "ขอนแก่น", "ชัยนาท"],
    "พื้นที่ (ไร่)": [7500, 6400, 8300, 5900],
    "คะแนนความเหมาะสม": [83, 76, 88, 72]
})

# === Bar Chart ===
bar = alt.Chart(data).mark_bar(cornerRadiusTopLeft=5, cornerRadiusTopRight=5).encode(
    x=alt.X('จังหวัด', sort='-y'),
    y='พื้นที่ (ไร่)',
    color=alt.Color('จังหวัด', legend=None)
).properties(
    title="พื้นที่เป้าหมายแต่ละจังหวัด",
    width=500,
    height=300
)

# === Pie Chart ===
pie_data = data.copy()
pie_data["สัดส่วน"] = pie_data["พื้นที่ (ไร่)"] / pie_data["พื้นที่ (ไร่)"].sum()
pie = alt.Chart(pie_data).mark_arc(innerRadius=40).encode(
    theta=alt.Theta(field="สัดส่วน", type="quantitative"),
    color=alt.Color(field="จังหวัด", type="nominal"),
    tooltip=["จังหวัด", "พื้นที่ (ไร่)"]
).properties(
    title="สัดส่วนพื้นที่เป้าหมาย",
    width=300,
    height=300
)

# === Show Charts ===
col1, col2 = st.columns(2)
col1.altair_chart(bar, use_container_width=True)
col2.altair_chart(pie, use_container_width=True)

