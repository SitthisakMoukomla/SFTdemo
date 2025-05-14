import streamlit as st
import geemap.foliumap as geemap
import ee
import json
from google.oauth2 import service_account
from streamlit_folium import st_folium

# === Load credentials from secrets ===
SERVICE_ACCOUNT = "sftdemo@tidy-daylight-459410-a4.iam.gserviceaccount.com"
with open("credentials.json") as f:
    credentials_dict = json.load(f)

credentials = service_account.Credentials.from_service_account_info(credentials_dict)
ee.Initialize(credentials)

# === CONFIG ===
province_name = "Chai Nat"
esa = ee.Image("ESA/WorldCover/v100/2020")
esa_palette = ['006400', 'ffbb22', 'ffff4c', 'f096ff', 'fa0000',
               'b4b4b4', 'f0f0f0', '0064c8', '0096a0', '00cf75',
               'fae6a0', '58481f', '0096ff', '9f6fff', 'fa00fa', 'c5f0ff', 'ffff00']

roi = ee.FeatureCollection("FAO/GAUL_SIMPLIFIED_500m/2015/level1") \
         .filter(ee.Filter.eq('ADM1_NAME', province_name))
geometry = roi.geometry()

vacant_mask = esa.eq(80).Or(esa.eq(30)).And(esa.neq(10))
vacant = esa.updateMask(vacant_mask)

total_area = geometry.area().divide(1e6)
vacant_area = vacant.multiply(ee.Image.pixelArea()).reduceRegion(
    reducer=ee.Reducer.sum(), geometry=geometry, scale=30, maxPixels=1e9)
vacant_area_km2 = vacant_area.getNumber('Map').divide(1e6)

st.set_page_config(layout="wide")
st.title("🌾 ระบบจัดหาพื้นที่รกร้างว่างเปล่า จังหวัดชัยนาท")
st.markdown("\u0e02\u0e49\u0e2d\u0e21\u0e39\u0e25\u0e08\u0e32\u0e01 **ESA WorldCover 2020**")

col1, col2, col3 = st.columns(3)
col1.metric("\ud83d\udccf \u0e1e\u0e37\u0e49\u0e19\u0e17\u0e35\u0e48\u0e08\u0e31\u0e07\u0e2b\u0e27\u0e31\u0e14 (\u0e15\u0e23.\u0e01\u0e21.)", f"{total_area.getInfo():,.2f}")
col2.metric("\ud83c\udf3f \u0e1e\u0e37\u0e49\u0e19\u0e17\u0e35\u0e48\u0e27\u0e48\u0e32\u0e07\u0e40\u0e1b\u0e25\u0e48\u0e32 (\u0e15\u0e23.\u0e01\u0e21.)", f"{vacant_area_km2.getInfo():,.2f}")
col3.metric("\ud83d\udcca \u0e04\u0e34\u0e14\u0e40\u0e1b\u0e47\u0e19\u0e23\u0e49\u0e2d\u0e22\u0e25ะ", f"{(vacant_area_km2.getInfo() / total_area.getInfo()) * 100:.2f} %")

Map = geemap.Map(center=[15.2, 100.1], zoom=9)
Map.addLayer(esa, {"min": 10, "max": 100, "palette": esa_palette}, "\ud83c\udf0d ESA WorldCover 2020")
Map.addLayer(vacant, {"palette": ["red"]}, "\u0e1e\u0e37\u0e49\u0e19\u0e17\u0e35\u0e48\u0e27\u0e48\u0e32\u0e07\u0e40\u0e1b\u0e25\u0e48\u0e32")
Map.addLayer(roi.style(color='blue', fillColor='00000000', width=2), {}, "\u0e02\u0e2d\u0e1a\u0e40\u0e02\u0e15\u0e08\u0e31\u0e07\u0e2b\u0e27\u0e31\u0e14")
Map.add_legend(title="WorldCover Legend", builtin_legend='ESA_WorldCover')

st.subheader("\ud83d\uddd8\ufe0f \u0e41\u0e1c\u0e19\u0e17\u0e35\u0e48\u0e1e\u0e37\u0e49\u0e19\u0e17\u0e35\u0e48\u0e27\u0e48\u0e32\u0e07\u0e40\u0e1b\u0e25\u0e48\u0e32")
st_folium(Map, width=700, height=500)

