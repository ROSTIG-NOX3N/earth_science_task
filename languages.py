
def get_labels(language):
    if language == 'English':
        return {
            'input_age': 'Enter a comparison age:',
            'select_isotope': 'Select an isotope:',
            'scatter_plot_title': 'Scatter plot of Isotope Half-lives with Annotations',
            'half_life': 'Half-life (years)',
            'isotope_index': 'Isotope Index',
            'closest': 'Closest to',
            'selected': 'Selected Isotope:',
            'input_age_label': 'Input Age:',
            'annotate_closest': 'Closest to',
            'annotate_selected': 'Selected Isotope:',
            'half_life_of_selected_isotope': 'Half-life of selected isotope'
        }
    elif:  # 한국어
        if language == '한국어' :
          return {
            'input_age': '비교할 연대 입력:',
            'select_isotope': '동위원소 선택:',
            'scatter_plot_title': '동위원소 반감기의 산포도 및 주석',
            'half_life': '반감기 (년)',
            'isotope_index': '동위원소 인덱스',
            'closest': '입력된 연대에 가장 가까운',
            'selected': '선택된 동위원소:',
            'input_age_label': '입력된 연대:',
            'annotate_closest': '입력된 연대에 가장 가까운 동위원소',
            'annotate_selected': '선택된 동위원소:',
            'half_life_of_selected_isotope': '선택된 동위원소의 반감기'
        }

