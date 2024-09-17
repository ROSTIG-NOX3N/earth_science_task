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
        st.session_state.messages = []
        st.session_state.prev_language = language

    # 메시지가 없을 경우 초기화
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # 다크모드/라이트모드에 따라 색상 설정
    theme_mode = st.get_option("theme.base")  # 'dark' 또는 'light' 반환

    if theme_mode == "dark":
        user_bg_color = "#2e2e2e"
        user_text_color = "#ffffff"
        assistant_bg_color = "#3e3e3e"
        assistant_text_color = "#ffffff"
    else:
        user_bg_color = "#dcf8c6"
        user_text_color = "#000000"
        assistant_bg_color = "#f1f0f0"
        assistant_text_color = "#000000"

    # 채팅 말풍선 스타일 적용
    user_message_style = f"""
        <div style='background-color: {user_bg_color}; color: {user_text_color}; padding: 10px; 
        border-radius: 10px; margin: 5px 0; max-width: 60%; text-align: right;'>
            <b>User:</b> {{}}</div>
    """

    assistant_message_style = f"""
        <div style='background-color: {assistant_bg_color}; color: {assistant_text_color}; padding: 10px; 
        border-radius: 10px; margin: 5px 0; max-width: 60%; text-align: left;'>
            <b>Assistant:</b> {{}}</div>
    """

    # 챗봇 탭
    st.header(labels['chatbot_header'])

    # 두 개의 열로 나누기 (비율 조정)
    col1, col3, col2 = st.columns([2.5, 0.1, 1])  # col1과 col2 사이에 col3 (세로선) 추가

    with col1:
        # 채팅 기록을 출력
        for message in st.session_state.messages:
            if message["role"] == "user":
                st.markdown(user_message_style.format(message['content']), unsafe_allow_html=True)
            elif message["role"] == "assistant":
                st.markdown(assistant_message_style.format(message['content']), unsafe_allow_html=True)

    with col3:
        # 세로선 표시
        st.markdown("<div style='width: 1px; background-color: #ccc; height: 650px;'></div>", unsafe_allow_html=True)

    with col2:
        # 챗봇 시작하기 버튼
        if st.button(labels['start_chatbot']):
            initial_question = "방사성 동위원소에 대해 궁금한 점이 있습니다."
            st.session_state.messages.append({"role": "user", "content": initial_question})

            assistant_reply = generate_response()
            if assistant_reply:
                st.session_state.messages.append({"role": "assistant", "content": assistant_reply})

        # 질문 버튼 세로 배치
        if st.button(labels['question1']):
            user_input = random.choice(labels['paraphrases']['question1'])
            st.session_state.messages.append({"role": "user", "content": user_input})

            assistant_reply = generate_response()
            if assistant_reply:
                st.session_state.messages.append({"role": "assistant", "content": assistant_reply})

        if st.button(labels['question2']):
            user_input = random.choice(labels['paraphrases']['question2'])
            st.session_state.messages.append({"role": "user", "content": user_input})

            assistant_reply = generate_response()
            if assistant_reply:
                st.session_state.messages.append({"role": "assistant", "content": assistant_reply})

        if st.button(labels['question3']):
            user_input = random.choice(labels['paraphrases']['question3'])
            st.session_state.messages.append({"role": "user", "content": user_input})

            assistant_reply = generate_response()
            if assistant_reply:
                st.session_state.messages.append({"role": "assistant", "content": assistant_reply})

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

# OpenAI API 키 설정
openai.api_key = st.secrets["OPENAI_API_KEY"]
