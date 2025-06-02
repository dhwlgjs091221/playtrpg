import streamlit as st
from supabase import create_client, Client

# Supabase 연결 정보
url = "https://csosixcrhclbitkagwjf.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNzb3NpeGNyaGNsYml0a2Fnd2pmIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDg4NDk5ODUsImV4cCI6MjA2NDQyNTk4NX0.JuQgk8RkPlcNV38yEhn9QF-o895l9rIeZNTcnemLdnQ"

supabase: Client = create_client(url, key)

st.title("TRPG 캐릭터 저장소")

name = st.text_input("캐릭터 이름")
hp = st.number_input("HP", 0, 100, 10)
mp = st.number_input("MP", 0, 100, 5)
desc = st.text_area("설명")

if st.button("저장하기"):
    data = {
        "name": name,
        "hp": hp,
        "mp": mp,
        "description": desc
    }
    res = supabase.table("characters").insert(data).execute()
    st.success("저장 완료!")
