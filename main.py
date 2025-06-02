import streamlit as st
import json
import random

# --- 캐릭터 입력 ---
st.title("CoC 캐릭터 시트")

name = st.text_input("이름")
job = st.text_input("직업")
str_stat = st.number_input("STR", min_value=1, max_value=100, value=50)
dex_stat = st.number_input("DEX", min_value=1, max_value=100, value=50)
san_stat = st.number_input("SAN", min_value=1, max_value=100, value=50)

character = {
    "name": name,
    "job": job,
    "STR": str_stat,
    "DEX": dex_stat,
    "SAN": san_stat
}

st.write(f"**{name}** ({job}) - STR: {str_stat}, DEX: {dex_stat}, SAN: {san_stat}")

# --- 저장 기능 ---
st.subheader("💾 캐릭터 저장하기")
char_json = json.dumps(character, indent=4)
st.download_button("캐릭터 저장 (JSON)", data=char_json, file_name=f"{name}_character.json", mime="application/json")

# --- 불러오기 기능 ---
st.subheader("📂 캐릭터 불러오기")
uploaded_file = st.file_uploader("JSON 파일 업로드", type="json")

if uploaded_file is not None:
    loaded_char = json.load(uploaded_file)
    st.success("캐릭터 불러오기 성공!")
    
    # 불러온 값으로 입력값 업데이트
    st.session_state["name"] = loaded_char.get("name", "")
    st.session_state["job"] = loaded_char.get("job", "")
    st.session_state["str_stat"] = loaded_char.get("STR", 50)
    st.session_state["dex_stat"] = loaded_char.get("DEX", 50)
    st.session_state["san_stat"] = loaded_char.get("SAN", 50)

    st.write(f"불러온 캐릭터: **{loaded_char['name']}** ({loaded_char['job']})")
    st.write(f"STR: {loaded_char['STR']}, DEX: {loaded_char['DEX']}, SAN: {loaded_char['SAN']}")

# --- 판정 기능 ---
st.header("🎲 능력치 판정")
selected_stat = st.selectbox("판정할 능력치 선택", options=["STR", "DEX", "SAN"])
if st.button("판정 굴리기 (1d100)"):
    roll = random.randint(1, 100)
    target = character[selected_stat]
    result = "성공" if roll <= target else "실패"
    st.write(f"🎲 주사위 결과: {roll} → **{result}**!")
