import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import json
from languages import get_labels
from chatbot import chatbot_ui  # 챗봇 UI 추가

# --- 사이드바 구성 --- 
# 언어 선택
language = st.sidebar.selectbox('언어를 선택해주세요 / Select language:', ['한국어', 'English', '日本語'])
labels = get_labels(language)  # 언어에 따라 라벨 불러오기

# --- 사이드바 탭 선택 ---
selected_tab = st.sidebar.radio(labels['select_tab'], [labels['section1_header'], labels['section2_header'], "Mother-Daughter Graph"])

# 방사성 동위원소 데이터 불러오기 함수
def load_isotope_data(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as jsonfile:
            isotope_data = json.load(jsonfile)
        # JSON 파일에서 동위원소 이름, 반감기 정보 가져오기
        isotope_data = [(entry["Isotope"], float(entry["Half Life"]), float(entry["Computed Half Life"])) for entry in isotope_data]
        return isotope_data
    except Exception as e:
        st.error(f"{labels['error_load_data']}: {e}")
        return []

# 방사성 동위원소 데이터 불러오기
isotope_data = load_isotope_data('Formatted_Radioactive_Isotope_Half_Lives.json')

if not isotope_data:
    st.stop()

# 동위원소 이름과 번호 분리
isotope_names = [item.split('-')[0] for item in [entry[0] for entry in isotope_data]]
isotope_numbers = [item.split('-')[1] if '-' in item else '' for item in [entry[0] for entry in isotope_data]]

# 동위원소 이름 중복 제거
unique_isotope_names = sorted(list(set(isotope_names)))

# 1. 첫 번째 선택 칸: 동위원소 이름 선택
selected_isotope_name = st.sidebar.selectbox(labels['select_isotope_name'], unique_isotope_names)

# 2. 두 번째 선택 칸: 선택된 동위원소의 번호 선택
filtered_isotope_numbers = [num for name, num in zip(isotope_names, isotope_numbers) if name == selected_isotope_name]
selected_isotope_number = st.sidebar.selectbox(f'{selected_isotope_name} {labels["select_isotope_number"]}', filtered_isotope_numbers)

# 선택된 동위원소 찾기
selected_isotope = f'{selected_isotope_name}-{selected_isotope_number}'
try:
    selected_idx = [entry[0] for entry in isotope_data].index(selected_isotope)
    selected_half_life = isotope_data[selected_idx][2]
except ValueError:
    st.error(labels['isotope_not_found'])
    st.stop()

# --- 모원소-자원소 그래프 탭 ---
if selected_tab == "Mother-Daughter Graph":
    st.header("모원소와 자원소의 변화 그래프")

    # 입력 연대 설정
    input_age = st.number_input("Input Age (in seconds)", min_value=1, value=100)

    # 붕괴 상수 계산
    decay_constant = np.log(2) / selected_half_life

    # 시간 범위 설정 (0부터 10 * 선택된 반감기까지)
    time = np.linspace(0, 10 * selected_half_life, 500)

    # 모원소의 양 계산
    initial_mother_isotope = 100  # 초기 모원소 양 설정
    mother_isotope_amount = initial_mother_isotope * np.exp(-decay_constant * time)

    # 자원소의 양 계산
    daughter_isotope_amount = initial_mother_isotope - mother_isotope_amount

    # 입력된 연대에서의 모원소와 자원소 양 계산
    mother_at_input_age = initial_mother_isotope * np.exp(-decay_constant * input_age)
    daughter_at_input_age = initial_mother_isotope - mother_at_input_age

    # --- 그래프 그리기 ---
    fig, ax = plt.subplots(figsize=(10, 6))

    # 모원소의 양 그래프
    ax.plot(time, mother_isotope_amount, label='Mother Isotope', color='blue')

    # 자원소의 양 그래프
    ax.plot(time, daughter_isotope_amount, label='Daughter Isotope', color='red')

    # 입력된 연대에서의 모원소와 자원소 양을 점으로 강조
    ax.scatter([input_age], [mother_at_input_age], color='blue', label='Mother at Input Age', s=100, zorder=5)
    ax.scatter([input_age], [daughter_at_input_age], color='red', label='Daughter at Input Age', s=100, zorder=5)

    # 그래프 설정
    ax.set_title(f'Amount of Mother and Daughter Isotopes over Time for {selected_isotope}')
    ax.set_xlabel('Time (seconds)')
    ax.set_ylabel('Isotope Amount')
    ax.grid(True)
    ax.legend()

    # 그래프 출력
    st.pyplot(fig)

# --- 챗봇 탭 ---
elif selected_tab == labels['section2_header']:
    chatbot_ui(language)  # 분리된 챗봇 기능 호출 시 언어 전달
