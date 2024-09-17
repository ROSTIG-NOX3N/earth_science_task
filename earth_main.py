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

# --- 그래프 탭 ---
if selected_tab == labels['section1_header']:
    st.header(labels['section1_header'])
    
    # 단위 선택 (초/년)
    time_unit = st.radio(labels['select_time_unit'], ('seconds', 'years'))

    # 입력 연대
    input_age = st.number_input(labels['input_age'], value=1, help=labels['input_age_help'])

    # 입력된 연대를 선택한 단위에 맞게 변환
    if time_unit == 'years':
        input_age_seconds = input_age * 31_536_000  # 1년 = 31,536,000초
    else:
        input_age_seconds = input_age  # 초 단위 그대로 사용

    # 초 단위 또는 년 단위로 반감기 데이터를 구분
    threshold = 31_536_000  # 1년을 초로 변환
    if time_unit == 'seconds':
        half_lives = [item[2] for item in isotope_data if item[2] < threshold]  # 초 단위 데이터
        y_label = 'Half-life (seconds)'  # 그래프 내부는 영어로 고정
    else:
        half_lives = [item[2] / threshold for item in isotope_data if item[2] >= threshold]  # 년 단위 데이터
        y_label = 'Half-life (years)'  # 그래프 내부는 영어로 고정

    # 입력된 연대와 반감기 비율이 1에 가장 가까운 동위원소 찾기
    ratios = [abs(input_age_seconds / half_life - 1) for half_life in [item[2] for item in isotope_data]]
    nearest_ratio_idx = np.argmin(ratios)
    nearest_isotope = isotope_data[nearest_ratio_idx][0]
    nearest_half_life = isotope_data[nearest_ratio_idx][2]

    # 1. 산포도 그리기
    fig, ax = plt.subplots(figsize=(15, 6))
    ax.scatter(range(len(half_lives)), half_lives, color='blue', label=y_label, s=10)

    # 입력된 연대와 반감기 비율이 1에 가장 가까운 동위원소 강조 (초록색 화살표)
    ax.annotate(f"Closest to input age / half-life ratio = 1: {nearest_isotope}", xy=(nearest_ratio_idx, nearest_half_life),
                xytext=(nearest_ratio_idx, nearest_half_life * 1.5),
                arrowprops=dict(facecolor='green', shrink=0.05))

    # 선택된 동위원소 강조 (주황색 원)
    ax.scatter(selected_idx, selected_half_life, color='orange', label=f"Selected Isotope: {selected_isotope}", s=50)

    # 입력된 연대를 기준으로 수평선 추가
    ax.axhline(y=input_age_seconds, color='gray', linestyle='--', label=f"Input Age: {input_age} {time_unit}")

    # x축 범위를 전체 데이터로 설정
    ax.set_xlim(0, len(half_lives) - 1)
    # y축 범위를 설정하여 데이터가 잘 보이도록 설정
    ax.set_ylim(min(half_lives) / 10, max(half_lives) * 10)

    # 라벨 및 제목 설정
    ax.set_xlabel('Isotope Index')  # 영어로 설정
    ax.set_ylabel(y_label)  # 영어로 설정
    ax.set_title('Scatter plot of Isotope Half-lives')  # 영어로 설정
    ax.set_yscale('log')
    ax.legend()

    # 그래프 출력
    st.pyplot(fig)

# --- 모원소-자원소 그래프 탭 ---
elif selected_tab == "Mother-Daughter Graph":
    st.header("모원소와 자원소의 변화 그래프")

    # 입력 연대 설정
    input_age_seconds = st.sidebar.number_input("Input Age (in seconds)", min_value=1, value=100)

    # 붕괴 상수 계산
    decay_constant = np.log(2) / selected_half_life

    # 시간 범위 설정 (0부터 입력된 연대까지)
    time = np.linspace(0, input_age_seconds, 500)

    # 모원소의 양 계산
    initial_mother_isotope = 100  # 초기 모원소 양 설정
    mother_isotope_amount = initial_mother_isotope * np.exp(-decay_constant * time)

    # 자원소의 양 계산
    daughter_isotope_amount = initial_mother_isotope - mother_isotope_amount

    # --- 그래프 그리기 ---
    fig, ax = plt.subplots(figsize=(10, 6))

    # 모원소의 양 그래프
    ax.plot(time, mother_isotope_amount, label='Mother Isotope', color='blue')

    # 자원소의 양 그래프
    ax.plot(time, daughter_isotope_amount, label='Daughter Isotope', color='red')

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
