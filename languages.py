# languages.py

def get_labels(language):
    if language == 'English':
        return {
            'input_age': 'Enter a comparison age:',
            'select_isotope': 'Select an isotope:',
            'scatter_plot_title': 'Scatter plot of Isotope Half-lives',  # 영어로 통일
            'half_life': 'Half-life (years)',  # 영어로 통일
            'isotope_index': 'Isotope Index',  # 영어로 통일
            'closest': 'Closest to',
            'selected': 'Selected Isotope:',
            'input_age_label': 'Input Age:',
            'annotate_closest': 'Closest to',
            'annotate_selected': 'Selected Isotope:',
            'half_life_of_selected_isotope': 'Half-life of selected isotope'
        }
    elif language == '한국어' :  # 한국어
        return {
            'input_age': '지질의 연대를 입력해주세요:',
            'select_isotope': '동위원소를 선택해주세요:',
            'scatter_plot_title': 'Scatter plot of Isotope Half-lives',  # 영어로 통일
            'half_life': 'Half-life (years)',  # 영어로 통일
            'isotope_index': 'Isotope Index',  # 영어로 통일
            'closest': '지질의 연대와 가장 가까운 동위원소',
            'selected': '선택된 동위원소 :',
            'input_age_label': 'Input Age:',
            'annotate_closest': 'Closest to',
            'annotate_selected': 'Selected Isotope:',
            'half_life_of_selected_isotope': '선택된 동위원소의 반감기(년)'
        }
