import streamlit as st
import random
import openai
from languages import get_labels

# 챗봇 UI 함수
def chatbot_ui(language):
    labels = get_labels(language)

    # 언어 변경 시 대화 내역 초기화
    if "prev_language" not in st.session_state:
        st.session_state.prev_language = language

    if st.session_state.prev_language != language:
        st.session_state.messages = []  # 언어 변경 시 대화 내역 초기화
        st.session_state.prev_language = language

    # 세션 상태에서 'messages'가 존재하지 않을 경우 초기화
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # 다크모드/라이트모드에 따라 색상 설정
    theme_mode = st.get_option("theme.base")  # 'dark' 또는 'light' 반환

    # 채팅 배경 및 텍스트 색상 설정
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

    # 화면을 채팅 공간과 버튼 공간으로 나누기
    col1, col2 = st.columns([3, 1])  # 왼쪽에 채팅 (3배 너비), 오른쪽에 버튼 (1배 너비)

    # 왼쪽: 채팅 내역
    with col1:
        st.subheader("💬 Chatbot")

        # 채팅 기록을 출력
        for message in st.session_state.messages:
            if message["role"] == "user":
                st.markdown(f"<div style='background-color: {user_bg_color}; color: {user_text_color}; padding: 10px; border-radius: 10px; margin: 5px 0; max-width: 60%; text-align: right; float: right;'>{message['content']}</div>", unsafe_allow_html=True)
            elif message["role"] == "assistant":
                st.markdown(f"<div style='background-color: {assistant_bg_color}; color: {assistant_text_color}; padding: 10px; border-radius: 10px; margin: 5px 0; max-width: 60%; text-align: left; float: left;'>{message['content']}</div>", unsafe_allow_html=True)

        # 로딩 메시지 표시
        if "loading" in st.session_state and st.session_state.loading:
            st.markdown("<div style='color: grey;'>Loading...</div>", unsafe_allow_html=True)

    # 오른쪽: 질문 공간
    with col2:
        st.subheader("Questions")

        if st.button(labels['question1']):
            process_user_input(random.choice(labels['paraphrases']['question1']))

        if st.button(labels['question2']):
            process_user_input(random.choice(labels['paraphrases']['question2']))

        if st.button(labels['question3']):
            process_user_input(random.choice(labels['paraphrases']['question3']))

# 사용자 입력 처리 및 챗봇 응답
def process_user_input(user_input):
    st.session_state.messages.append({"role": "user", "content": user_input})

    # 로딩 상태 설정
    st.session_state.loading = True

    # GPT-3.5에게 질문을 보내고 답변 받기
    assistant_reply = generate_response()
    if assistant_reply:
        st.session_state.messages.append({"role": "assistant", "content": assistant_reply})

    # 로딩 상태 해제
    st.session_state.loading = False

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
