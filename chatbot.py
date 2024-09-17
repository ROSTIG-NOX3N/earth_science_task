import streamlit as st
import random
import openai
from languages import get_labels

# 챗봇 UI 함수
def chatbot_ui(language):
    labels = get_labels(language)

    # --- 언어 변경 시 대화 내역 초기화 ---
    if "prev_language" not in st.session_state:
        st.session_state.prev_language = language

    if st.session_state.prev_language != language:
        st.session_state.messages = []
        st.session_state.prev_language = language

    # --- 챗봇 탭 ---
    st.header(labels['chatbot_header'])

    # OpenAI API 호출 함수 정의
    def generate_response():
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=st.session_state.messages
            )
            assistant_reply = response.choices[0].message.content
            return assistant_reply
        except openai.error.OpenAIError as e:
            error_code = getattr(e, 'code', 'N/A')
            error_message = str(e)
            st.error(f"{labels['error_message']} (Error Code: {error_code}): {error_message}")
            return None

    # 'messages'가 존재하지 않으면 초기화
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # 채팅 말풍선 스타일 적용을 위한 HTML/CSS
    user_message_style = """
        <div style='background-color: #dcf8c6; padding: 10px; border-radius: 10px; margin: 5px 0; max-width: 60%;'>
            <b>User:</b> {}</div>
    """

    assistant_message_style = """
        <div style='background-color: #f1f0f0; padding: 10px; border-radius: 10px; margin: 5px 0; max-width: 60%; text-align: left;'>
            <b>Assistant:</b> {}</div>
    """

    # 채팅 기록 표시
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(user_message_style.format(message['content']), unsafe_allow_html=True)
        elif message["role"] == "assistant":
            st.markdown(assistant_message_style.format(message['content']), unsafe_allow_html=True)

    # 질문 버튼 3개 생성 및 랜덤 질문
    col1, col2, col3 = st.columns(3)

    # 각 버튼에서 랜덤 질문 생성
    with col1:
        if st.button(labels['question1']):
            user_input = random.choice(labels['paraphrases']['question1'])
            st.session_state.messages.append({"role": "user", "content": user_input})

            assistant_reply = generate_response()
            if assistant_reply:
                st.session_state.messages.append({"role": "assistant", "content": assistant_reply})

    with col2:
        if st.button(labels['question2']):
            user_input = random.choice(labels['paraphrases']['question2'])
            st.session_state.messages.append({"role": "user", "content": user_input})

            assistant_reply = generate_response()
            if assistant_reply:
                st.session_state.messages.append({"role": "assistant", "content": assistant_reply})

    with col3:
        if st.button(labels['question3']):
            user_input = random.choice(labels['paraphrases']['question3'])
            st.session_state.messages.append({"role": "user", "content": user_input})

            assistant_reply = generate_response()
            if assistant_reply:
                st.session_state.messages.append({"role": "assistant", "content": assistant_reply})

