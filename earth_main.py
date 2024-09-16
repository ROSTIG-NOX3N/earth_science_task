import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import json
import openai
import random  # 무작위 선택을 위해 필요
from languages import get_labels  # languages.py에서 라벨 가져오기

# OpenAI API 키 설정
openai.api_key = st.secrets["OPENAI_API_KEY"]

# 방사성 동위원소 데이터 불러오기 함수
def load_isotope_data(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        # JSON 파일에서 동위원소 이름, 반감기 정보 가져오기
        isotope_data = [(entry["Isotope"], entry["Half Life"], entry["Computed Half Life"]) for entry in data]
        return isotope_data
    except Exception as e:
        st.error(f"Failed to load isotope data: {e}")
        return []

# 방사성 동위원소 데이터 불러오기
isotope_data = load_isotope_data('updated_isotope_data.json')

if not isotope_data:
    st.stop()

# 언어 선택 (한국어, 영어, 일본어 지원)
language = st.selectbox('언어를 선택해주세요 / Select language:', ['한국어', 'English', '日本語'])
labels = get_labels(language)  # 선택된 언어에 맞는 라벨 가져오기

# 언어 변경 시 채팅 기록 초기화 및 시스템 메시지 추가
if "prev_language" not in st.session_state or st.session_state.prev_language != language:
    st.session_state.prev_language = language
    st.session_state.messages = []
    st.session_state.messages.append({
        "role": "system",
        "content": f"You are a helpful assistant that communicates in {language}."
    })

# --- 섹션 1: 동위원소 산포도 ---
with st.expander(labels['section1_header'], expanded=True):
    # 입력 연대 (범위 제한 없음)
    input_age = st.number_input(labels['input_age'], value=1, help=labels['input_age_help'])

    # 동위원소 이름과 번호 분리
    isotope_names = [item.split('-')[0] for item in [entry[0] for entry in isotope_data]]
    isotope_numbers = [item.split('-')[1] if '-' in item else '' for item in [entry[0] for entry in isotope_data]]

    # 동위원소 이름 중복 제거
    unique_isotope_names = sorted(list(set(isotope_names)))

    # 1. 첫 번째 선택 칸: 동위원소 이름 선택
    selected_isotope_name = st.selectbox(labels['select_isotope_name'], unique_isotope_names)

    # 2. 두 번째 선택 칸: 선택된 동위원소의 번호 선택
    filtered_isotope_numbers = [num for name, num in zip(isotope_names, isotope_numbers) if name == selected_isotope_name]
    selected_isotope_number = st.selectbox(f'{selected_isotope_name} {labels["select_isotope_number"]}', filtered_isotope_numbers)

    # 선택된 동위원소 찾기
    selected_isotope = f'{selected_isotope_name}-{selected_isotope_number}'
    try:
        selected_idx = [entry[0] for entry in isotope_data].index(selected_isotope)
    except ValueError:
        st.error(labels['isotope_not_found'])
        st.stop()
    selected_half_life = isotope_data[selected_idx][2]

    # None 값을 제외하고 계산
    half_lives = [item[2] for item in isotope_data if item[2] is not None]

    # 입력된 연대와 가장 가까운 동위원소 찾기
    diffs = [abs(half_life - input_age) for half_life in half_lives]
    nearest_idx = np.argmin(diffs)
    nearest_isotope = isotope_data[nearest_idx][0]
    nearest_half_life = isotope_data[nearest_idx][2]

    # 반감기 값이 1초에 가장 가까운 동위원소 찾기
    diffs_from_one = [abs(half_life - 1) for half_life in half_lives]
    nearest_to_one_idx = np.argmin(diffs_from_one)
    nearest_to_one_isotope = isotope_data[nearest_to_one_idx][0]
    nearest_to_one_half_life = isotope_data[nearest_to_one_idx][2]

    # 1. 산포도 그리기 (그래프 내 텍스트는 영어로 고정)
    fig, ax = plt.subplots(figsize=(15, 6))
    ax.scatter(range(len(half_lives)), half_lives, color='blue', label='Half-life', s=10)

    # 입력된 연대에 가장 가까운 동위원소 강조
    ax.annotate(f"Closest to input age ({input_age} seconds): {nearest_isotope}", xy=(nearest_idx, nearest_half_life),
                xytext=(nearest_idx, nearest_half_life * 1.5),
                arrowprops=dict(facecolor='green', shrink=0.05))

    # 반감기 값이 1초에 가장 가까운 동위원소 강조
    ax.annotate(f"Isotope with Half-life closest to 1 second: {nearest_to_one_isotope}", xy=(nearest_to_one_idx, nearest_to_one_half_life),
                xytext=(nearest_to_one_idx, nearest_to_one_half_life * 1.5),
                arrowprops=dict(facecolor='red', shrink=0.05))

    # 선택된 동위원소 강조
    ax.scatter(selected_idx, selected_half_life, color='orange', label=f"Selected Isotope: {selected_isotope}", s=50)
    ax.axhline(y=input_age, color='gray', linestyle='--', label=f"Input Age: {input_age}")

    # x축 범위를 전체 데이터로 설정
    ax.set_xlim(0, len(half_lives) - 1)
    # y축 범위를 설정하여 데이터가 잘 보이도록 설정
    ax.set_ylim(min(half_lives)/10, max(half_lives)*10)

    # 라벨 및 제목 설정 (그래프 내부는 영어로 고정)
    ax.set_xlabel('Isotope Index')
    ax.set_ylabel('Half-life (seconds)')
    ax.set_title('Scatter plot of Isotope Half-lives')
    ax.set_yscale('log')
    ax.legend()

    # 그래프 출력
    st.pyplot(fig)

    # 동일한 이름의 동위원소만 산포도로 그리기 버튼
    if st.button(labels['plot_same_name']):
        # 선택한 동위원소의 인덱스 찾기
        filtered_isotopes = [(i, name, number, hl) for i, (name, number, hl) in enumerate(zip(isotope_names, isotope_numbers, [entry[2] for entry in isotope_data])) if name == selected_isotope_name and hl is not None]
        fig, ax = plt.subplots(figsize=(15, 6))
        for idx, (i, name, number, half_life) in enumerate(filtered_isotopes):
            ax.scatter(idx, half_life, color='blue', label=f'{name}-{number}' if idx == 0 else "", s=50)
        # 선택된 동위원소 강조
        selected_filtered_idx = next((idx for idx, (i, name, number, hl) in enumerate(filtered_isotopes) if number == selected_isotope_number), None)
        if selected_filtered_idx is not None:
            ax.scatter(selected_filtered_idx, selected_half_life, color='orange', label=f"Selected Isotope: {selected_isotope}", s=100)
        ax.set_xlabel('Isotope Index')
        ax.set_ylabel('Half-life (seconds)')
        ax.set_title(f"Scatter plot of all isotopes with the name {selected_isotope_name}")
        ax.set_yscale('log')
        # y축 범위를 설정하여 데이터가 잘 보이도록 설정
        half_lives_filtered = [hl for i, name, number, hl in filtered_isotopes]
        ax.set_ylim(min(half_lives_filtered)/10, max(half_lives_filtered)*10)
        ax.legend()
        st.pyplot(fig)

    # 결과 표시 (인터페이스 라벨은 선택된 언어로 표시)
    st.write(f"{labels['selected_isotope']}: **{selected_isotope}**")
    st.write(f"**{labels['selected_half_life']}: {selected_half_life} {labels['half_life_seconds']}**")
    st.write(f"{labels['nearest_isotope']}: **{nearest_isotope}** ({nearest_half_life} {labels['half_life_seconds']})")
    st.write(f"{labels['nearest_to_one']}: **{nearest_to_one_isotope}** ({nearest_to_one_half_life} {labels['half_life_seconds']})")

# --- 섹션 2: 챗봇 ---
with st.expander(labels['section2_header'], expanded=False):
    # 고정된 질문 버튼 (질문 3개)
    col1, col2, col3 = st.columns(3)

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

    with col1:
        if st.button(labels['question1']):
            user_input = random.choice(labels['paraphrases']['question1'])
            # 사용자의 메시지 추가
            st.session_state.messages.append({"role": "user", "content": user_input})

            # OpenAI API를 사용하여 응답 생성
            assistant_reply = generate_response()

            if assistant_reply:
                # 어시스턴트의 응답 추가
                st.session_state.messages.append({"role": "assistant", "content": assistant_reply})

    with col2:
        if st.button(labels['question2']):
            user_input = random.choice(labels['paraphrases']['question2'])
            # 사용자의 메시지 추가
            st.session_state.messages.append({"role": "user", "content": user_input})

            # OpenAI API를 사용하여 응답 생성
            assistant_reply = generate_response()

            if assistant_reply:
                # 어시스턴트의 응답 추가
                st.session_state.messages.append({"role": "assistant", "content": assistant_reply})

    with col3:
        if st.button(labels['question3']):
            user_input = random.choice(labels['paraphrases']['question3'])
            # 사용자의 메시지 추가
            st.session_state.messages.append({"role": "user", "content": user_input})

            # OpenAI API를 사용하여 응답 생성
            assistant_reply = generate_response()

            if assistant_reply:
                # 어시스턴트의 응답 추가
                st.session_state.messages.append({"role": "assistant", "content": assistant_reply})

    # 채팅 내역 표시
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f"**{labels['user']}:** {message['content']}")
        elif message["role"] == "assistant":
            st.markdown(f"**{labels['assistant']}:** {message['content']}")
