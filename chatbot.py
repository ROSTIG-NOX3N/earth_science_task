import streamlit as st
import random
import openai
from languages import get_labels

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

    # 챗봇 탭 헤더
    st.header(labels.get('chatbot_header', '챗봇'))

    # CSS 스타일을 사용하여 채팅 메시지 스타일링
    st.markdown(f"""
        <style>
            .chat-container {{
                height: 450px;
                overflow-y: auto;
                border: 1px solid #ccc;
                border-radius: 10px;
                padding: 10px;
                display: flex;
                flex-direction: column;
            }}
            .user-message {{
                background-color: {user_bg_color};
                color: {user_text_color};
                padding: 10px;
                border-radius: 10px;
                margin: 5px 0;
                max-width: 60%;
                align-self: flex-end;
            }}
            .assistant-message {{
                background-color: {assistant_bg_color};
                color: {assistant_text_color};
                padding: 10px;
                border-radius: 10px;
                margin: 5px 0;
                max-width: 60%;
                align-self: flex-start;
            }}
        </style>
    """, unsafe_allow_html=True)

    # 스크롤 가능한 채팅 기록 영역
    chat_messages = ""
    for message in st.session_state.messages:
        if message["role"] == "user":
            chat_messages += f"<div class='user-message'><b>{labels.get('user', '사용자')}:</b> {message['content']}</div>"
        elif message["role"] == "assistant":
            chat_messages += f"<div class='assistant-message'><b>{labels.get('assistant', '어시스턴트')}:</b> {message['content']}</div>"

    st.markdown(f"<div class='chat-container'>{chat_messages}</div>", unsafe_allow_html=True)

    # 챗봇 인터랙션 요소 배치
    col1, col2 = st.columns([2, 1])  # 두 개의 열로 나누기

    with col1:
        # 챗봇 시작하기 버튼
        if st.button(labels.get('start_chatbot', '챗봇 시작하기(답변이 안나와도 누르세요)')):
            initial_question = "방사성 동위원소에 대해 궁금한 점이 있습니다."
            st.session_state.messages.append({"role": "user", "content": initial_question})

            assistant_reply = generate_response(labels)
            if assistant_reply:
                st.session_state.messages.append({"role": "assistant", "content": assistant_reply})

        # 사전 정의된 질문 버튼 세로 배치
        for i in range(1, 4):
            question_key = f'question{i}'
            if st.button(labels.get(question_key, f'질문 {i}')):
                # 파라프레이즈 선택
                user_input = random.choice(labels['paraphrases'][question_key])
                st.session_state.messages.append({"role": "user", "content": user_input})

                assistant_reply = generate_response(labels)
                if assistant_reply:
                    st.session_state.messages.append({"role": "assistant", "content": assistant_reply})

        # 자유 질문 입력 필드
        user_question = st.text_input(labels.get("free_question_label", "자유 질문을 입력하세요:"))
        if st.button(labels.get("ask_button", "질문하기")):
            if user_question.strip():
                st.session_state.messages.append({"role": "user", "content": user_question.strip()})
                assistant_reply = generate_response(labels)
                if assistant_reply:
                    st.session_state.messages.append({"role": "assistant", "content": assistant_reply})
            else:
                st.warning(labels.get("input_age_help", "질문을 입력해 주세요."))

    with col2:
        # 두 번째 열은 빈 공간으로 두거나 다른 기능 추가 가능
        st.write("")  # 이 부분을 다른 내용으로 대체할 수 있습니다.

# OpenAI API 호출 함수 정의
def generate_response(labels):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=st.session_state.messages
        )
        assistant_reply = response.choices[0].message.content
        return assistant_reply
    except openai.error.OpenAIError as e:
        st.error(labels.get("error_message", "죄송합니다, 답변을 생성하는 데 실패했습니다."))
        return None

# OpenAI API 키 설정
openai.api_key = st.secrets["OPENAI_API_KEY"]
