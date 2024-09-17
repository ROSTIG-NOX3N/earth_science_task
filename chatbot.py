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
        st.session_state.messages = []  # 언어 변경 시 대화 내역 초기화
        st.session_state.prev_language = language

    # --- 세션 상태에서 'messages'가 존재하지 않을 경우 초기화 ---
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # --- 다크모드/라이트모드에 따라 색상 설정 ---
    theme_mode = st.get_option("theme.base")  # 'dark' 또는 'light' 반환

    if theme_mode == "dark":
        user_bg_color = "#2e2e2e"  # 어두운 배경색
        user_text_color = "#ffffff"  # 밝은 텍스트 색상
        assistant_bg_color = "#3e3e3e"  # 어두운 배경색
        assistant_text_color = "#ffffff"  # 밝은 텍스트 색상
    else:
        user_bg_color = "#dcf8c6"  # 연한 초록색 배경 (라이트모드)
        user_text_color = "#000000"  # 검은 텍스트 색상
        assistant_bg_color = "#f1f0f0"  # 연한 회색 배경 (라이트모드)
        assistant_text_color = "#000000"  # 검은 텍스트 색상

    # --- 채팅 말풍선 스타일 적용 ---
    user_message_style = f"""
        <div style='background-color: {user_bg_color}; color: {user_text_color}; padding: 10px; 
        border-radius: 10px; margin: 5px 0; max-width: 60%; text-align: right; float: right; clear: both;'>
            <b>User:</b> {{}}</div>
    """

    assistant_message_style = f"""
        <div style='background-color: {assistant_bg_color}; color: {assistant_text_color}; padding: 10px; 
        border-radius: 10px; margin: 5px 0; max-width: 60%; text-align: left; float: left; clear: both;'>
            <b>Assistant:</b> {{}}</div>
    """

    # --- 채팅 탭 ---
    st.markdown("<h2 style='text-align: center;'>💬 Chatbot</h2>", unsafe_allow_html=True)

    # 채팅 기록을 연속적으로 표시
    chat_messages = ""
    for message in st.session_state.messages:
        if message["role"] == "user":
            chat_messages += user_message_style.format(message['content'])
        elif message["role"] == "assistant":
            chat_messages += assistant_message_style.format(message['content'])

    # 채팅 기록 출력
    st.markdown(chat_messages, unsafe_allow_html=True)

    # 질문 버튼 화면 하단 고정
    st.markdown(
        """
        <style>
        .fixed-buttons {
            position: fixed;
            bottom: 10px;
            width: 100%;
            text-align: center;
            background-color: white;
            padding-top: 10px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # 질문 버튼 배치 (하단 고정)
    st.markdown('<div class="fixed-buttons">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
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
    st.markdown('</div>', unsafe_allow_html=True)

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
        st.error(f"Failed to generate response (Error Code: {error_code}): {error_message}")
        return None
