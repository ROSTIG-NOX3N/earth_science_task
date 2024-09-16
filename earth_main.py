import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import csv  # CSV 파일을 읽기 위해 필요
import openai
import random  # 무작위 선택을 위해 필요
from languages import get_labels  # languages.py에서 라벨 가져오기

# OpenAI API 키 설정
openai.api_key = st.secrets["OPENAI_API_KEY"]

# 방사성 동위원소 데이터 불러오기 함수 (CSV 파일을 읽도록 수정)
def load_isotope_data(file_path):
    try:
        isotope_data = []
        with open(file_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                isotope_name = row["Isotope"]
                half_life = float(row["Half Life"])
                computed_half_life = float(row["Computed Half Life"])
                isotope_data.append((isotope_name, half_life, computed_half_life))
        return isotope_data
    except Exception as e:
        st.error(f"Failed to load isotope data: {e}")
        return []

# 방사성 동위원소 데이터 불러오기
isotope_data = load_isotope_data('Formatted_Radioactive_Isotope_Half_Lives.csv')  # JSON이 아닌 CSV 파일 사용

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
    # 단위 선택 (초/년)
    time_unit = st.radio("단위를 선택하세요 (Select time unit):", ('seconds', 'years'))

    # 입력 연대 (범위 제한 없음)
    input_age = st.number_input(labels['input_age'], value=1, help=labels['input_age_help'])

    # 입력된 연대를 선택한 단위에 맞게 변환
    if time_unit == 'years':
        input_age_seconds = input_age * 31_536_000  # 1년 = 31,536,000초
    else:
        input_age_seconds = input_age  # 초 단위 그대로 사용

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

    # 초 단위 또는 년 단위로 반감기 데이터를 구분
    threshold = 31_536_000  # 1년을 초로 변환
    half_lives_seconds = [item[2] for item in isotope_data if item[2] < threshold]  # 초 단위 데이터
    half_lives_years = [item[2] / threshold for item in isotope_data if item[2] >= threshold]  # 년 단위 데이터

    # 입력된 연대와 가장 가까운 동위원소 찾기
    diffs = [abs(half_life - input_age_seconds) for half_life in [item[2] for item in isotope_data]]
    nearest_idx = np.argmin(diffs)
    nearest_isotope = isotope_data[nearest_idx][0]
    nearest_half_life = isotope_data[nearest_idx][2]

    # 반감기 값이 1초에 가장 가까운 동위원소 찾기
    diffs_from_one = [abs(half_life - 1) for half_life in [item[2] for item in isotope_data]]
    nearest_to_one_idx = np.argmin(diffs_from_one)
    nearest_to_one_isotope = isotope_data[nearest_to_one_idx][0]
    nearest_to_one_half_life = isotope_data[nearest_to_one_idx][2]

    # 1. 산포도 그리기 (그래프 내 텍스트는 영어로 고정)
    fig, ax = plt.subplots(figsize=(15, 6))
    ax.scatter(range(len(half_lives_seconds)), half_lives_seconds, color='blue', label='Half-life (seconds)', s=10)
    ax.scatter(range(len(half_lives_years)), half_lives_years, color='green', label='Half-life (years)', s=10)

    # 입력된 연대에 가장 가까운 동위원소 강조
    ax.annotate(f"Closest to input age ({input_age} {time_unit}): {nearest_isotope}", xy=(nearest_idx, nearest_half_life),
                xytext=(nearest_idx, nearest_half_life * 1.5),
                arrowprops=dict(facecolor='green', shrink=0.05))

    # 반감기 값이 1초에 가장 가까운 동위원소 강조
    ax.annotate(f"Isotope with Half-life closest to 1 second: {nearest_to_one_isotope}", xy=(nearest_to_one_idx, nearest_to_one_half_life),
                xytext=(nearest_to_one_idx, nearest_to_one_half_life * 1.5),
                arrowprops=dict(facecolor='red', shrink=0.05))

    # 선택된 동위원소 강조
    ax.scatter(selected_idx, selected_half_life, color='orange', label=f"Selected Isotope: {selected_isotope}", s=50)
    ax.axhline(y=input_age_seconds, color='gray', linestyle='--', label=f"Input Age: {input_age} {time_unit}")

    # x축 범위를 전체 데이터로 설정
    ax.set_xlim(0, len(half_lives_seconds) + len(half_lives_years) - 1)
    # y축 범위를 설정하여 데이터가 잘 보이도록 설정
    ax.set_ylim(min(half_lives_seconds + half_lives_years)/10, max(half_lives_seconds + half_lives_years)*10)

    # 라벨 및 제목 설정 (그래프 내부는 영어로 고정)
    ax.set_xlabel('Isotope Index')
    ax.set_ylabel('Half-life (seconds or years)')
    ax.set_title('Scatter plot of Isotope Half-lives')
    ax.set_yscale('log')
    ax.legend()

    # 그래프 출력
    st.pyplot(fig)

    # 결과 표시 (인터페이스 라벨은 선택된 언어로 표시)
    st.write(f"{labels['selected_isotope']}: **{selected_isotope}**")
    st.write(f"**{labels['selected_half_life']}: {selected_half_life} {labels['half_life_seconds']}**")
    st.write(f"{labels['nearest_isotope']}: **{nearest_isotope}** ({nearest_half_life} {labels['half_life_seconds']})")
    st.write(f"{labels['nearest_to_one']}: **{nearest_to_one_isotope}** ({nearest_to_one_half_life} {labels['half_life_seconds']})")
