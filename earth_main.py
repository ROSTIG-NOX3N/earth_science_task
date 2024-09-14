import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import json
from languages import get_labels

# 방사성 동위원소 데이터 읽기 및 파싱
def parse_isotope_data(data):
    isotope_data = []
    if isinstance(data, list) and data[0] == "Dataset":
        for entry in data[1]:
            if entry[0] == "Association":
                isotope_name = None
                half_life = None
                
                # 각 Association 내부의 Rule을 확인하여 Isotope와 Half Life 추출
                for rule in entry[1:]:
                    if rule[0] == "Rule":
                        key = rule[1].strip("'")  # 키에서 따옴표 제거
                        value = rule[2].strip("'") if isinstance(rule[2], str) else rule[2]  # 값에서 따옴표 제거
                        
                        if key == "Isotope":
                            isotope_name = value
                        elif key == "Half Life":
                            half_life = float(value)

                # Isotope와 Half Life가 모두 존재할 경우 리스트에 추가
                if isotope_name and half_life:
                    isotope_data.append((isotope_name, half_life))
                else:
                    st.warning(f"Missing 'Isotope' or 'Half Life' in entry: {entry}")
    return isotope_data

# 방사성 동위원소 데이터 불러오기
def load_isotope_data(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        return parse_isotope_data(data)
    except Exception as e:
        st.error(f"Failed to load isotope data: {e}")
        return []

# 방사성 동위원소 데이터 불러오기
isotope_data = load_isotope_data('Formatted-Radioactive-Isotope-Half-Lives.json')

if not isotope_data:
    st.stop()  # 데이터 로드에 실패하면 앱 중지

# 언어 선택
language = st.selectbox('Select language:', ['English', '한국어'])
labels = get_labels(language)

# 입력 연대
input_age = st.number_input('Enter a comparison age:', min_value=1, value=1)  # 그래프 관련 입력 영어로 고정

# 반감기 값을 추출
half_lives = [item[1] for item in isotope_data]
isotope_names = [item[0] for item in isotope_data]

# 입력된 나이에 가장 가까운 반감기 찾기
diffs = [abs(half_life - input_age) for half_life in half_lives]
nearest_idxs = np.argsort(diffs)[:35]  # 상위 35개의 가장 가까운 반감기 찾기

# 상위 35개의 동위원소와 반감기만 추출
nearest_half_lives = [half_lives[i] for i in nearest_idxs]
nearest_isotopes = [isotope_names[i] for i in nearest_idxs]

# 히스토그램 그리기
fig, ax = plt.subplots(figsize=(15, 6))
ax.hist(nearest_half_lives, bins=10, color='blue', alpha=0.7)

# 그래프 라벨은 영어로 고정
ax.set_xlabel('Isotope Index')
ax.set_ylabel('Half-life (years)')
ax.set_title('Histogram of Isotope Half-lives')

# 그래프 출력
st.pyplot(fig)

# 결과 표시 (언어에 따라 표시되는 부분)
st.write(f"Closest isotope: **{nearest_isotopes[0]}**")
st.write(f"Half-life of closest isotope: **{nearest_half_lives[0]}** years")
