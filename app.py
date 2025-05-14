import streamlit as st
import geemap.foliumap as geemap
import ee
from streamlit_folium import st_folium
from google.oauth2 import service_account

# === GEE Initialization with Service Account ===
import ee
import streamlit as st
import json
from google.oauth2 import service_account

SERVICE_ACCOUNT = st.secrets["SERVICE_ACCOUNT"]
credentials_dict = json.loads(st.secrets["CREDENTIALS_JSON"])
credentials = service_account.Credentials.from_service_account_info(credentials_dict)
ee.Initialize(credentials)

# === CONFIG ===
province_name = "Chai Nat"
esa = ee.Image("ESA/WorldCover/v200/2021")
esa_palette = ['006400', 'ffbb22', 'ffff4c', 'f096ff', 'fa0000',
               'b4b4b4', 'f0f0f0', '0064c8', '0096a0', '00cf75',
               'fae6a0', '58481f', '0096ff', '9f6fff', 'fa00fa', 'c5f0ff', 'ffff00']

# === Load จังหวัดชัยนาท ===
roi = ee.FeatureCollection("FAO/GAUL_SIMPLIFIED_500m/2015/level1") \
         .filter(ee.Filter.eq('ADM1_NAME', province_name))
geometry = roi.geometry()

# === พื้นที่ว่างเปล่า (Bare: 80, Grassland: 30 แต่ไม่ใช่ป่า: 10) ===
vacant_mask = esa.eq(80).Or(esa.eq(30)).And(esa.neq(10))
vacant = esa.updateMask(vacant_mask)

# === คำนวณพื้นที่ ===
total_area = geometry.area().divide(1e6)  # ตารางเมตร -> ตารางกิโลเมตร
vacant_area = vacant.multiply(ee.Image.pixelArea()).reduceRegion(
    reducer=ee.Reducer.sum(), geometry=geometry, scale=30, maxPixels=1e9)
vacant_area_km2 = vacant_area.getNumber('Map').divide(1e6)

# === UI ===
st.set_page_config(layout="wide")
st.title("🌾 ระบบจัดหาพื้นที่รกร้างว่างเปล่า จังหวัดชัยนาท")
st.markdown("ข้อมูลจาก **ESA WorldCover 2020**")

col1, col2, col3 = st.columns(3)
col1.metric("📏 พื้นที่จังหวัด (ตร.กม.)", f"{total_area.getInfo():,.2f}")
col2.metric("🌿 พื้นที่ว่างเปล่า (ตร.กม.)", f"{vacant_area_km2.getInfo():,.2f}")
col3.metric("📊 คิดเป็นร้อยละ", f"{(vacant_area_km2.getInfo() / total_area.getInfo()) * 100:.2f} %")

# === แสดงแผนที่ ===
Map = geemap.Map(center=[15.2, 100.1], zoom=9)
Map.addLayer(esa, {"min": 10, "max": 100, "palette": esa_palette}, "🌍 ESA WorldCover 2020")
Map.addLayer(vacant, {"palette": ["red"]}, "พื้นที่ว่างเปล่า")
Map.addLayer(roi.style(color='blue', fillColor='00000000', width=2), {}, "ขอบเขตจังหวัด")
Map.add_legend(title="WorldCover Legend", builtin_legend='ESA_WorldCover')

st.subheader("🗺️ แผนที่พื้นที่ว่างเปล่า")
st_folium(Map, width=700, height=500)
