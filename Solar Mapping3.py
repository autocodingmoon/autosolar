import streamlit as st
import requests
import folium
from streamlit_folium import st_folium

VWORLD_API_KEY = "3EF5EC0C-5706-3665-ADBA-BEAFFD4B74CC"

st.set_page_config(page_title="브이월드 주소 지도 서비스", layout="centered")

st.title("브이월드 주소 → 지도 표시")
st.write("아래에 주소를 입력하고 '조회'를 눌러주세요.")

address = st.text_input("주소 입력 (예: 서울특별시 중구 세종대로 110)")

def get_coordinates(address):
    url = "http://api.vworld.kr/req/address"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    for addr_type in ["road", "parcel"]:
        params = {
            "service": "address",
            "request": "getcoord",
            "format": "json",
            "crs": "EPSG:4326",
            "key": VWORLD_API_KEY,
            "address": address,
            "type": addr_type
        }
        try:
            response = requests.get(url, params=params, headers=headers, timeout=5)
            data = response.json()
            if data.get("response", {}).get("status") == "OK":
                result = data["response"]["result"]["point"]
                lon = float(result["x"])
                lat = float(result["y"])
                return lat, lon
        except Exception as e:
            continue
    return None

if "coords" not in st.session_state:
    st.session_state["coords"] = None

if st.button("조회"):
    if address:
        coords = get_coordinates(address)
        st.session_state["coords"] = coords
        if coords:
            st.success(f"좌표: {coords}")
        else:
            st.error("❌ 해당 주소를 찾을 수 없습니다. 도로명 또는 지번 주소를 정확히 입력해주세요.")
    else:
        st.warning("주소를 입력해주세요.")

coords = st.session_state["coords"]

if coords:
    m = folium.Map(location=coords, zoom_start=16)
    folium.Marker(location=coords, popup=address, tooltip="여기입니다!").add_to(m)
    st_folium(m, width=700, height=500)

