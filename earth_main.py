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
        # JSON 파일에서 동위원소 이름, 반감기, 계산된 반감기 정보 가져오기
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
language = st.selectbox('언어를 선택해주세요 / Select language:', ['English', '한국어', '日本語'])
labels = get_labels(language)  # 선택된 언어에 맞는 라벨 가져오기

# 입력 연대 (범위 제한 없음)
input_age = st.number_input(labels['input_age'], value=1, help=labels['input_age_help'])

# 동위원소 이름 목록 만들기
isotope_names = [entry[0] for entry in isotope_data]
unique_isotope_names = list(set(isotope_names))

# 동위원소 이름 선택
selected_isotope_name = st.selectbox(labels['select_isotope_name'], unique_isotope_names)

# 선택된 동위원소의 반감기 계산
selected_isotopes = [entry for entry in isotope_data if entry[0] == selected_isotope_name]
selected_isotope = selected_isotopes[0] if selected_isotopes else None
selected_half_life = selected_isotope[2] if selected_isotope else None

# None 값을 제외하고 계산
half_lives = [item[2] for item in isotope_data if item[2] is not None]
diffs = [abs(half_life - input_age) for half_life in half_lives]

# 입력된 연대에 가장 가까운 동위원소 찾기
nearest_idx = np.argmin(diffs)
nearest_isotope = isotope_data[nearest_idx][0]
nearest_half_life = isotope_data[nearest_idx][2]

# 1. 산포도 그리기
fig, ax = plt.subplots(figsize=(15, 6))
ax.scatter(range(len(half_lives)), half_lives, color='blue', label='Half-life', s=10)

# 입력된 연대에 가장 가까운 동위원소 강조
ax.annotate(f'Closest to input age ({input_age} years): {nearest_isotope}', xy=(nearest_idx, nearest_half_life),
            xytext=(nearest_idx, nearest_half_life * 1.5),
            arrowprops=dict(facecolor='green', shrink=0.05))

# 선택된 동위원소 강조
if selected_half_life:
    ax.scatter(unique_isotope_names.index(selected_isotope_name), selected_half_life, color='orange', s=50)
ax.axhline(y=input_age, color='gray', linestyle='--')

ax.set_xlabel('Isotope Index')
ax.set_ylabel('Half-life (years)')
ax.set_yscale('log')
st.pyplot(fig)

st.write(f"{labels['selected_isotope']} **{selected_isotope_name}**")
st.write(f"**{labels['selected_half_life']}: {selected_half_life} {labels['half_life_years']}**")
