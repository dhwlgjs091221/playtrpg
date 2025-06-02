import streamlit as st
from supabase import create_client

# Supabase 연결
url = "https://csosixcrhclbitkagwjf.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNzb3NpeGNyaGNsYml0a2Fnd2pmIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDg4NDk5ODUsImV4cCI6MjA2NDQyNTk4NX0.JuQgk8RkPlcNV38yEhn9QF-o895l9rIeZNTcnemLdnQ"
supabase = create_client(url, key)

st.title("🧙 CoC 캐릭터 관리 앱")

menu = st.sidebar.selectbox("메뉴 선택", ["캐릭터 만들기", "캐릭터 불러오기"])

# 캐릭터 생성
if menu == "캐릭터 만들기":
    name = st.text_input("이름")
    hp = st.number_input("HP", 0, 99, 10)
    mp = st.number_input("MP", 0, 99, 10)
    san = st.number_input("SAN", 0, 99, 50)
    desc = st.text_area("설명")

    if st.button("💾 저장하기"):
        data = {
            "name": name,
            "hp": hp,
            "mp": mp,
            "san": san,
            "description": desc
        }
        supabase.table("characters").insert(data).execute()
        st.success("저장 완료!")

# 캐릭터 불러오기
elif menu == "캐릭터 불러오기":
    res = supabase.table("characters").select("*").execute()
    characters = res.data

    if characters:
        names = [char['name'] for char in characters]
        selected_name = st.selectbox("불러올 캐릭터를 선택하세요", names)

        selected_char = next((c for c in characters if c["name"] == selected_name), None)
        if selected_char:
            st.subheader(f"🔍 {selected_char['name']} 님의 캐릭터 정보")
            st.text(f"HP: {selected_char['hp']}")
            st.text(f"MP: {selected_char['mp']}")
            st.text(f"SAN: {selected_char['san']}")
            st.markdown(f"**설명**\n{selected_char['description']}")
    else:
        st.warning("저장된 캐릭터가 없습니다.")
