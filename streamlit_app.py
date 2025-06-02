# streamlit_app.py
import streamlit as st
from supabase import create_client
import streamlit.components.v1 as components

# Supabase 연결
SUPABASE_URL = "https://csosixcrhclbitkagwjf.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNzb3NpeGNyaGNsYml0a2Fnd2pmIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDg4NDk5ODUsImV4cCI6MjA2NDQyNTk4NX0.JuQgk8RkPlcNV38yEhn9QF-o895l9rIeZNTcnemLdnQ"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

st.set_page_config(page_title="TRPG CoC 앱", layout="centered")

st.title("🔮 TRPG 도우미 (CoC 룰)")
tab1, tab2, tab3 = st.tabs(["🧙 캐릭터 생성", "📜 캐릭터 목록", "💬 실시간 채팅"])

with tab1:
    st.header("캐릭터 생성")
    name = st.text_input("이름")
    strength = st.number_input("힘", min_value=1, max_value=100, step=1)
    dexterity = st.number_input("민첩성", min_value=1, max_value=100, step=1)
    intelligence = st.number_input("지능", min_value=1, max_value=100, step=1)
    delete_password = st.text_input("삭제용 비밀번호", type="password")

    if st.button("📝 저장하기"):
        data = {
            "name": name,
            "strength": strength,
            "dexterity": dexterity,
            "intelligence": intelligence,
            "delete_password": delete_password
        }
        try:
            supabase.table("characters").insert(data).execute()
            st.success("저장 완료!")
        except Exception as e:
            st.error(f"저장 실패: {e}")

with tab2:
    st.header("저장된 캐릭터들")
    try:
        result = supabase.table("characters").select("id, name, strength, dexterity, intelligence").execute()
        for c in result.data:
            st.write(f"🧍 이름: {c['name']}, 힘: {c['strength']}, 민첩성: {c['dexterity']}, 지능: {c['intelligence']}")
    except Exception as e:
        st.error(f"불러오기 실패: {e}")

with tab3:
    st.header("💬 실시간 채팅")
    components.html("""
    <script>
      const ws = new WebSocket("ws://localhost:8000/ws");
      ws.onmessage = function(event) {
        const chatBox = document.getElementById("chat-box");
        chatBox.innerHTML += "<p>" + event.data + "</p>";
      };

      function sendMessage() {
        const input = document.getElementById("msg");
        if (input.value) {
          ws.send(input.value);
          input.value = "";
        }
      }
    </script>

    <div id="chat-box" style="height:300px; overflow:auto; border:1px solid #ccc; padding: 10px;"></div>
    <input id="msg" type="text" placeholder="메시지 입력" style="width: 80%" />
    <button onclick="sendMessage()">전송</button>
    """, height=400)
