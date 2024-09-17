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
        st.session_state.messages = []  # 대화 내용 초기화
        st.session_state.prev_language = language  # 이전 언어 업데이트

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

    # 챗봇 탭
    st.header(labels['chatbot_header'])

    # CSS 스타일을 사용하여 가로 배치
    st.markdown("""
        <style>
            .chat-container {
                height: 450px;
                overflow-y: auto;
                border: 1px solid #ccc;
                border-radius: 10px;
                padding: 10px;
                display: flex;
                flex-direction: column;
            }
            .user-message {
                background-color: """ + user_bg_color + """;
                color: """ + user_text_color + """;
                padding: 10px;
                border-radius: 10px;
                margin: 5px 0;
                max-width: 60%;
                align-self: flex-end;
            }
            .assistant-message {
                background-color: """ + assistant_bg_color + """;
                color: """ + assistant_text_color + """;
                padding: 10px;
                border-radius: 10px;
                margin: 5px 0;
                max-width: 60%;
                align-self: flex-start;
            }
        </style>
    """, unsafe_allow_html=True)

    # 스크롤 가능한 채팅 기록 영역
    chat_messages = ""
    for message in st.session_state.messages:
        if message["role"] == "user":
            chat_messages += f"<div class='user-message'><b>User:</b> {message['content']}</div>"
        elif message["role"] == "assistant":
            chat_messages += f"<div class='assistant-message'><b>Assistant:</b> {message['content']}</div>"

    st.markdown(f"<div class='chat-container'>{chat_messages}</div>", unsafe_allow_html=True)

    # 챗봇 시작하기 버튼과 질문 버튼 배치
    col1, col2 = st.columns([2, 1])  # 두 개의 열로 나누기

    with col1:
        # 챗봇 시작하기 버튼
        if st.button(labels['start_chatbot']):
            initial_question = "방사성 동위원소에 대해 궁금한 점이 있습니다."
            st.session_state.messages.append({"role": "user", "content": initial_question})

            assistant_reply = generate_response()
            if assistant_reply:
                st.session_state.messages.append({"role": "assistant", "content": assistant_reply})

        # 질문 버튼 세로 배치
        if st.button(labels['question1']):
            user_input = random.choice(labels['paraphrases']['question1']) if language == '한국어' else random.choice(labels['paraphrases']['question1_en'])
            st.session_state.messages.append({"role": "user", "content": user_input})

            assistant_reply = generate_response()
            if assistant_reply:
                st.session_state.messages.append({"role": "assistant", "content": assistant_reply})

        if st.button(labels['question2']):
            user_input = random.choice(labels['paraphrases']['question2']) if language == '한국어' else random.choice(labels['paraphrases']['question2_en'])
            st.session_state.messages.append({"role": "user", "content": user_input})

            assistant_reply = generate_response()
            if assistant_reply:
                st.session_state.messages.append({"role": "assistant", "content": assistant_reply})

        if st.button(labels['question3']):
            user_input = random.choice(labels['paraphrases']['question3']) if language == '한국어' else random.choice(labels['paraphrases']['question3_en'])
            st.session_state.messages.append({"role": "user", "content": user_input})

            assistant_reply = generate_response()
            if assistant_reply:
                st.session_state.messages.append({"role": "assistant", "content": assistant_reply})

    with col2:
        # 두 번째 열은 빈 공간으로 두거나 다른 기능 추가 가능
        st.write("")  # 이 부분을 다른 내용으로 대체할 수 있습니다.

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
