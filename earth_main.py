import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import json
from languages import get_labels  # languages.py에서 라벨 가져오기

# 방사성 동위원소 데이터 불러오기 함수
def load_isotope_data(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        # JSON 파일에서 동위원소 이름, 번호, 반감기, 계산된 반감기 정보 가져오기
        isotope_data = [(entry["Isotope"], entry["Half Life"], entry["Computed Half Life"]) for entry in data]
        return isotope_data
    except Exception as e:
        st.error(f"Failed to load isotope data: {e}")
        return []

# 방사성 동위원소 데이터 불러오기
isotope_data = load_isotope_data('updated_isotope_data.json')

if not isotope_data:
    st.stop()

# 언어 선택 (한국어, 영어, 일본어 지원) - 그래프 외부 UI만 다국어 지원
language = st.selectbox('언어를 선택해주세요 / Select language:', ['English', '한국어', '日本語'])
labels = get_labels(language)  # 선택된 언어에 맞는 라벨 가져오기

# 입력 연대 (범위 제한 없음)
input_age = st.number_input(labels['input_age'], value=1, help=labels['input_age_help'])

# 동위원소 이름과 번호 분리
isotope_names = [item.split('-')[0] for item in [entry[0] for entry in isotope_data]]
isotope_numbers = [item.split('-')[1] if '-' in item else '' for item in [entry[0] for entry in isotope_data]]

# 동위원소 이름 중복 제거
unique_isotope_names = list(set(isotope_names))

# 1. 첫 번째 선택 칸: 동위원소 이름 선택
selected_isotope_name = st.selectbox(labels['select_isotope_name'], unique_isotope_names)

# 2. 두 번째 선택 칸: 선택된 동위원소의 번호 선택
filtered_isotope_numbers = [num for name, num in zip(isotope_names, isotope_numbers) if name == selected_isotope_name]
selected_isotope_number = st.selectbox(f'{selected_isotope_name} {labels["select_isotope_number"]}', filtered_isotope_numbers)

# 선택된 동위원소 찾기
selected_isotope = f'{selected_isotope_name}-{selected_isotope_number}'
selected_idx = [entry[0] for entry in isotope_data].index(selected_isotope)
selected_half_life = isotope_data[selected_idx][2]

# None 값을 제외하고 계산
half_lives = [item[2] for item in isotope_data if item[2] is not None]

# 입력된 연대와 가장 가까운 동위원소 찾기
diffs = [abs(half_life - input_age) for half_life in half_lives]
nearest_idx = np.argmin(diffs)
nearest_isotope = isotope_data[nearest_idx][0]
nearest_half_life = isotope_data[nearest_idx][2]

# 반감기 값이 1에 가장 가까운 동위원소 찾기
diffs_from_one = [abs(half_life - 1) for half_life in half_lives]
nearest_to_one_idx = np.argmin(diffs_from_one)
nearest_to_one_isotope = isotope_data[nearest_to_one_idx][0]
nearest_to_one_half_life = isotope_data[nearest_to_one_idx][2]

# 1. 산포도 그리기 (그래프 내 텍스트는 영어로 고정)
fig, ax = plt.subplots(figsize=(28, 6))
ax.scatter(range(len(half_lives)), half_lives, color='blue', label='Half-life', s=10)

# 입력된 연대에 가장 가까운 동위원소 강조
ax.annotate(f'Closest to input age ({input_age} years): {nearest_isotope}', xy=(nearest_idx, nearest_half_life),
            xytext=(nearest_idx, nearest_half_life * 1.5),
            arrowprops=dict(facecolor='green', shrink=0.05))

# 반감기 값이 1에 가장 가까운 동위원소 강조
ax.annotate(f'Closest to Half-life of 1: {nearest_to_one_isotope}', xy=(nearest_to_one_idx, nearest_to_one_half_life),
            xytext=(nearest_to_one_idx, nearest_to_one_half_life * 1.5),
            arrowprops=dict(facecolor='red', shrink=0.05))

# 선택된 동위원소 강조
ax.scatter(selected_idx, selected_half_life, color='orange', label=f'Selected Isotope: {selected_isotope}', s=50)
ax.axhline(y=input_age, color='gray', linestyle='--', label=f'Input Age: {input_age}')

# 라벨 및 제목 설정 (그래프 내부는 영어로 고정)
ax.set_xlabel('Isotope Index')
ax.set_ylabel('Half-life (years)')
ax.set_title('Scatter plot of Isotope Half-lives')
ax.set_yscale('log')
ax.legend()

# 그래프 출력
st.pyplot(fig)

# 동일한 이름의 동위원소만 산포도로 그리기 버튼
if st.button(labels['plot_same_name']):
    filtered_isotopes = [(name, number, half_life) for name, number, half_life in zip(isotope_names, isotope_numbers, half_lives) if name == selected_isotope_name]
    fig, ax = plt.subplots(figsize=(15, 6))
    for i, (name, number, half_life) in enumerate(filtered_isotopes):
        ax.scatter(i, half_life, color='blue', label=f'{name}-{number}' if i == 0 else "", s=50)
    ax.scatter(filtered_isotope_numbers.index(selected_isotope_number), selected_half_life, color='orange', label=f'Selected Isotope: {selected_isotope}', s=100)
    ax.set_xlabel('Isotope Index')
    ax.set_ylabel('Half-life (years)')
    ax.set_title(f'Scatter plot of all isotopes with the name {selected_isotope_name}')
    ax.set_yscale('log')
    ax.legend()
    st.pyplot(fig)

# 결과 표시 (UI는 언어에 따라 변경됨, 그래프 내부는 영어로 유지)
st.write(f"{labels['selected_isotope']} **{selected_isotope}**")
st.write(f"**{labels['selected_half_life']}: {selected_half_life} {labels['half_life_years']}**")
st.write(f"{labels['nearest_isotope']}: **{nearest_isotope}** ({nearest_half_life} {labels['half_life_years']})")
st.write(f"**{labels['nearest_to_one']}: {nearest_to_one_isotope}** ({nearest_to_one_half_life} {labels['half_life_years']})")
