import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import json

# --- 사이드바 구성 ---
# 언어 선택
language = st.sidebar.selectbox('언어를 선택해주세요 / Select language:', ['한국어', 'English', '日本語'])

# --- 방사성 동위원소 데이터 불러오기 ---
def load_isotope_data(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as jsonfile:
            isotope_data = json.load(jsonfile)
        # JSON 파일에서 동위원소 이름, 반감기 정보 가져오기
        isotope_data = [(entry["Isotope"], float(entry["Half Life"]), float(entry["Computed Half Life"])) for entry in isotope_data]
        return isotope_data
    except Exception as e:
        st.error(f"데이터를 불러오는 중 오류 발생: {e}")
        return []

# 방사성 동위원소 데이터 로드
isotope_data = load_isotope_data('Formatted_Radioactive_Isotope_Half_Lives.json')

if not isotope_data:
    st.stop()

# --- 모원소-자원소 그래프 탭 ---
st.sidebar.title("모원소-자원소 그래프")

# 동위원소 이름과 번호 분리
isotope_names = [item.split('-')[0] for item in [entry[0] for entry in isotope_data]]
isotope_numbers = [item.split('-')[1] if '-' in item else '' for item in [entry[0] for entry in isotope_data]]

# 동위원소 이름 중복 제거
unique_isotope_names = sorted(list(set(isotope_names)))

# 1. 첫 번째 선택 칸: 동위원소 이름 선택
selected_isotope_name = st.sidebar.selectbox('동위원소 이름을 선택하세요:', unique_isotope_names)

# 2. 두 번째 선택 칸: 선택된 동위원소의 번호 선택
filtered_isotope_numbers = [num for name, num in zip(isotope_names, isotope_numbers) if name == selected_isotope_name]
selected_isotope_number = st.sidebar.selectbox(f'{selected_isotope_name} 동위원소 번호를 선택하세요:', filtered_isotope_numbers)

# 선택된 동위원소 찾기
selected_isotope = f'{selected_isotope_name}-{selected_isotope_number}'
try:
    selected_idx = [entry[0] for entry in isotope_data].index(selected_isotope)
except ValueError:
    st.error('선택한 동위원소를 찾을 수 없습니다.')
    st.stop()

selected_half_life = isotope_data[selected_idx][2]

# 입력된 연대와 초기 모원소의 양
input_age = st.sidebar.number_input('연대를 입력하세요 (초 단위):', min_value=1, value=100)
initial_mother_isotope = st.sidebar.number_input('초기 모원소 양을 입력하세요:', min_value=1, value=100)

# 붕괴 상수 계산 (λ = ln(2) / 반감기)
decay_constant = np.log(2) / selected_half_life

# 시간 범위 설정 (입력된 연대를 기준으로 0에서 입력된 연대까지)
time = np.linspace(0, input_age, 500)

# 모원소의 양 계산
mother_isotope = initial_mother_isotope * np.exp(-decay_constant * time)

# 자원소의 양 계산 (자원소는 모원소의 감소량만큼 증가)
daughter_isotope = initial_mother_isotope - mother_isotope

# --- 그래프 그리기 ---
st.header('모원소와 자원소의 변화 그래프')

fig, ax = plt.subplots(figsize=(10, 6))

# 모원소의 양 그래프
ax.plot(time, mother_isotope, label='Mother Isotope', color='blue')

# 자원소의 양 그래프
ax.plot(time, daughter_isotope, label='Daughter Isotope', color='red')

# 그래프 설정
ax.set_title(f'Amount of Mother and Daughter Isotopes over Time for {selected_isotope}')
ax.set_xlabel('Time (seconds)')
ax.set_ylabel('Isotope Amount')
ax.grid(True)
ax.legend()

# 그래프 출력
st.pyplot(fig)
