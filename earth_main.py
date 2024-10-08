import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import json
from languages import get_labels
from chatbot import chatbot_ui  # 챗봇 UI 추가

# 방사성 동위원소 데이터 불러오기 함수
def load_isotope_data(file_path):
    """
    JSON 파일로부터 방사성 동위원소 데이터를 로드합니다.
    
    Parameters:
        file_path (str): 데이터 파일의 경로.
    
    Returns:
        list: 동위원소 이름, 반감기, 계산된 반감기 정보가 포함된 리스트.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as jsonfile:
            isotope_data = json.load(jsonfile)
        # JSON 파일에서 동위원소 이름, 반감기 정보 가져오기
        isotope_data = [(entry["Isotope"], float(entry["Half Life"]), float(entry["Computed Half Life"])) for entry in isotope_data]
        return isotope_data
    except Exception as e:
        st.error(f"Failed to load data: {e}")
        return []

# 동위원소 번호 필터링 함수
def get_filtered_isotope_numbers(isotope_names, isotope_numbers, selected_name):
    """
    선택된 동위원소 이름에 해당하는 번호 목록을 반환합니다.
    
    Parameters:
        isotope_names (list): 모든 동위원소 이름 목록.
        isotope_numbers (list): 모든 동위원소 번호 목록.
        selected_name (str): 선택된 동위원소 이름.
    
    Returns:
        list: 선택된 동위원소 이름에 해당하는 번호 목록.
    """
    return [num for name, num in zip(isotope_names, isotope_numbers) if name == selected_name]

# 산포도 그래프 그리기 함수 (레이블 고정: 영어)
def plot_scatter(isotope_data, selected_idx, input_age_seconds, time_unit):
    """
    방사성 동위원소의 반감기를 산포도로 시각화합니다.
    
    Parameters:
        isotope_data (list): 동위원소 데이터 리스트.
        selected_idx (int): 선택된 동위원소의 인덱스.
        input_age_seconds (float): 입력된 연대(초 단위).
        time_unit (str): 시간 단위 ('seconds' 또는 'years').
    """
    threshold = 31_536_000  # 1년을 초로 변환
    if time_unit == "seconds":
        half_lives = [item[2] for item in isotope_data if item[2] < threshold]
        y_label = "Half-life (seconds)"
    else:
        half_lives = [item[2] / threshold for item in isotope_data if item[2] >= threshold]  # years로 변환
        y_label = "Half-life (years)"
    
    # 입력된 연대와 반감기 비율이 1에 가장 가까운 동위원소 찾기
    ratios = [abs(input_age_seconds / half_life - 1) for half_life in [item[2] for item in isotope_data]]
    nearest_ratio_idx = np.argmin(ratios)
    nearest_isotope = isotope_data[nearest_ratio_idx][0]
    nearest_half_life = isotope_data[nearest_ratio_idx][2]

    # 산포도 그리기
    fig, ax = plt.subplots(figsize=(15, 6))
    ax.scatter(range(len(half_lives)), half_lives, color='blue', label=y_label, s=10)

    # 가장 가까운 동위원소 강조
    if time_unit == "years":
        nearest_half_life_display = nearest_half_life / threshold  # 변환된 반감기
    else:
        nearest_half_life_display = nearest_half_life  # 원래 반감기

    ax.annotate(
        f"Closest Isotope: {nearest_isotope}\n(Half-life: {nearest_half_life_display:.2f} {y_label})",
        xy=(nearest_ratio_idx, nearest_half_life_display if time_unit == "years" else nearest_half_life),
        xytext=(nearest_ratio_idx, (nearest_half_life_display if time_unit == "years" else nearest_half_life) * 1.5),
        arrowprops=dict(facecolor='green', shrink=0.05, linewidth=2, edgecolor='black'),  # 강조 표시
        fontsize=12, color='green', weight='bold'  # 강조된 텍스트
    )

    # 선택된 동위원소 강조
    selected_half_life = isotope_data[selected_idx][2]
    ax.scatter(selected_idx, selected_half_life / threshold if time_unit == "years" else selected_half_life, 
               color='orange', label=f"Selected Isotope: {isotope_data[selected_idx][0]}", s=50)

    # 입력 연대 기준 수평선 추가
    if time_unit == "years":
        input_age_display = input_age_seconds / threshold  # 변환된 입력 연대
    else:
        input_age_display = input_age_seconds  # 초 단위 그대로 사용

    ax.axhline(y=input_age_display, color='gray', linestyle='--', label=f"Input Age: {input_age_display:.2f} {y_label}")

    # 축 설정
    ax.set_xlim(0, len(half_lives) - 1)
    ax.set_ylim(min(half_lives) / 10, max(half_lives) * 10)
    ax.set_xlabel("Isotope Index", fontsize=12)
    ax.set_ylabel(y_label, fontsize=12)
    ax.set_title("Scatter Plot of Isotope Half-lives", fontsize=14)
    ax.set_yscale('log')
    ax.legend()

    # 그래프 출력
    st.pyplot(fig)

    # 가장 가까운 동위원소와 반감기 정보 표시
    st.markdown(f"### Closest Isotope: {nearest_isotope}")
    st.markdown(f"**Half-life:** {nearest_half_life_display:.2f} {y_label}")

# 모원소-자원소 그래프 그리기 함수
def plot_mother_daughter_graph(selected_half_life, selected_isotope, labels):
    """
    모원소와 자원소의 비율 변화를 그래프로 시각화합니다.
    
    Parameters:
        selected_half_life (float): 선택된 동위원소의 반감기(초 단위).
        selected_isotope (str): 선택된 동위원소의 이름.
        labels (dict): 다국어 라벨 딕셔너리.
    """
    decay_constant = np.log(2) / selected_half_life
    time = np.linspace(0, 1, 500)  # 시간 범위 설정 (0부터 1초)
    
    initial_mother_isotope = 100  # 초기 모원소 양 설정
    mother_isotope_amount = initial_mother_isotope * np.exp(-decay_constant * time)
    daughter_isotope_amount = initial_mother_isotope - mother_isotope_amount
    
    mother_ratio = mother_isotope_amount / initial_mother_isotope
    daughter_ratio = daughter_isotope_amount / initial_mother_isotope
    
    # 1초 시점 비율 계산
    mother_at_1_second = initial_mother_isotope * np.exp(-decay_constant * 1)
    daughter_at_1_second = initial_mother_isotope - mother_at_1_second
    mother_ratio_at_1_second = round((mother_at_1_second / initial_mother_isotope) * 100, 6)
    daughter_ratio_at_1_second = round((daughter_at_1_second / initial_mother_isotope) * 100, 6)
    
    # 사이드바에 비율 표시
    st.sidebar.markdown(f"**{labels.get('mother_ratio_1s', 'Mother Isotope Ratio at 1 second')}:** {mother_ratio_at_1_second}%")
    st.sidebar.markdown(f"**{labels.get('daughter_ratio_1s', 'Daughter Isotope Ratio at 1 second')}:** {daughter_ratio_at_1_second}%")
    
    # 그래프 그리기
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(time, mother_ratio * 100, label="Mother Isotope Ratio (%)", color='blue')
    ax.plot(time, daughter_ratio * 100, label="Daughter Isotope Ratio (%)", color='red')
    
    # 1초 시점 비율 강조
    ax.scatter([1], [mother_ratio_at_1_second], color='blue', label="Mother Isotope Ratio at 1 second", s=100, zorder=5)
    ax.scatter([1], [daughter_ratio_at_1_second], color='red', label="Daughter Isotope Ratio at 1 second", s=100, zorder=5)
    
    # 그래프 설정
    ax.set_title(f"Mother-Daughter Graph - {selected_isotope}", fontsize=14)
    ax.set_xlabel("Time (seconds)", fontsize=12)
    ax.set_ylabel("Isotope Ratio (%)", fontsize=12)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 100)
    ax.grid(True)
    ax.legend()
    
    # 그래프 출력
    st.pyplot(fig)

# 메인 함수
def main():
    st.set_page_config(page_title="방사성 동위원소 분석기", layout="wide")
    
    # --- 사이드바 구성 ---
    # 언어 선택
    language = st.sidebar.selectbox('언어를 선택해주세요 / Select language:', ['한국어', 'English', '日本語'])
    labels = get_labels(language)  # 언어에 따라 라벨 불러오기
    
    # 사이드바 탭 선택
    selected_tab = st.sidebar.radio(
        labels.get('select_tab', '탭 선택'), 
        [
            labels.get('section1_header', '산포도 그래프'),  # 산포도 그래프 탭
            labels.get('section2_header', '챗봇'),        # 챗봇 탭
            "Mother-Daughter Graph"                     # 모자원소 그래프 탭
        ]
    )
    
    # 방사성 동위원소 데이터 불러오기
    isotope_data = load_isotope_data('Formatted_Radioactive_Isotope_Half_Lives.json')
    
    if not isotope_data:
        st.stop()
    
    # 동위원소 이름과 번호 분리
    isotope_names = [item.split('-')[0] for item in [entry[0] for entry in isotope_data]]
    isotope_numbers = [item.split('-')[1] if '-' in item else '' for item in [entry[0] for entry in isotope_data]]
    
    # 고유한 동위원소 이름 목록
    unique_isotope_names = sorted(list(set(isotope_names)))
    
    # 동위원소 이름 선택
    selected_isotope_name = st.sidebar.selectbox(
        labels.get("select_isotope_name", "동위원소 이름 선택"), 
        unique_isotope_names, 
        key="isotope_name_select"
    )
    
    # 동위원소 번호 선택
    filtered_isotope_numbers = get_filtered_isotope_numbers(isotope_names, isotope_numbers, selected_isotope_name)
    selected_isotope_number = st.sidebar.selectbox(
        f'{selected_isotope_name} 번호 선택', 
        filtered_isotope_numbers, 
        key="isotope_number_select"
    )
    
    # 선택된 동위원소 찾기
    selected_isotope = f'{selected_isotope_name}-{selected_isotope_number}'
    try:
        selected_idx = [entry[0] for entry in isotope_data].index(selected_isotope)
        selected_half_life = isotope_data[selected_idx][2]
    except ValueError:
        st.error(labels.get("isotope_not_found", "선택한 동위원소를 찾을 수 없습니다."))
        selected_idx = None
    
    # 선택한 동위원소의 반감기 값을 사이드바에 표시
    if selected_idx is not None:
        st.sidebar.markdown(f"**{labels.get('selected_half_life', 'Half-life of selected isotope')}:** {selected_half_life} seconds")
    
    # --- 탭별 기능 분기 ---
    if selected_tab == labels.get('section1_header', '산포도 그래프'):
        # 산포도 그래프 탭
        st.header("Scatter Plot of Isotope Half-lives")
        
        if selected_idx is None:
            st.error("Please select a valid isotope.")
        else:
            # 단위 선택
            time_unit = st.radio(
                labels.get("select_time_unit", "Select time unit:"), 
                ("seconds", "years"), 
                key="time_unit_select"
            )
            
            # 입력 연대
            input_age = st.number_input(
                labels.get("input_age", "Enter a comparison age:"),
                value=1.0,  # 정수를 실수로 변경
                min_value=0.0,
                help=labels.get("input_age_help", "Please enter an age to compare isotopes."),
                key="age_input"
            )
            
            if input_age <= 0:
                st.warning(labels.get("positive_age_warning", "Please enter a positive value."))
            else:
                # 입력 연대 변환
                if time_unit == "years":
                    input_age_seconds = input_age * 31_536_000  # 1년 = 31,536,000초
                else:
                    input_age_seconds = input_age  # 초 단위 그대로 사용
                
                # 산포도 그래프 그리기
                plot_scatter(isotope_data, selected_idx, input_age_seconds, time_unit)
    
    elif selected_tab == labels.get('section2_header', '챗봇'):
        # 챗봇 탭
        chatbot_ui(language)  # 챗봇 UI 호출
    
    elif selected_tab == "Mother-Daughter Graph":
        # 모자원소 그래프 탭
        st.header("Mother-Daughter Graph")
        
        if selected_idx is None:
            st.error("Please select a valid isotope.")
        else:
            # 모자원소 그래프 그리기
            plot_mother_daughter_graph(selected_half_life, selected_isotope, labels)

if __name__ == "__main__":
    main()
