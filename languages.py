def get_labels(language):
    if language == 'English':
        return {
            'input_age': 'Enter a comparison age:',
            'select_isotope_name': 'Select Isotope Name:',
            'select_isotope_number': 'Select Isotope Number:',
            'scatter_plot_title': 'Scatter plot of Isotope Half-lives',
            'half_life': 'years (Half-life)',
            'isotope_index': 'Isotope Index',
            'closest_to_age': 'Closest to input age',
            'selected_isotope': 'Selected Isotope:',
            'plot_same_name': 'Plot Isotopes with the same name',
            'input_age_label': 'Input Age',
            'selected_half_life': 'Half-life of selected isotope',
            'nearest_isotope': 'Closest Isotope to Input Age',
            'half_life_years': 'years (Half-life)'
        }
    elif language == '한국어':
        return {
            'input_age': '지질의 연대를 입력해주세요:',
            'select_isotope_name': '동위원소 이름을 선택해주세요:',
            'select_isotope_number': '동위원소 넘버를 선택해주세요:',
            'scatter_plot_title': '동위원소 반감기 산포도',
            'half_life': '년 (반감기)',
            'isotope_index': '동위원소 인덱스',
            'closest_to_age': '입력된 연대와 가장 가까운 동위원소',
            'selected_isotope': '선택된 동위원소:',
            'plot_same_name': '동일한 이름의 동위원소 산포도 보기',
            'input_age_label': '입력 연대',
            'selected_half_life': '선택된 동위원소의 반감기',
            'nearest_isotope': '입력된 연대와 가장 가까운 동위원소',
            'half_life_years': '년 (반감기)'
        }
    elif language == '日本語':
        return {
            'input_age': '地質時代を入力してください:',
            'select_isotope_name': '同位体名を選択してください:',
            'select_isotope_number': '同位体番号を選択してください:',
            'scatter_plot_title': '同位体の半減期の散布図',
            'half_life': '年 (半減期)',
            'isotope_index': '同位体インデックス',
            'closest_to_age': '入力された時代に最も近い同位体',
            'selected_isotope': '選択された同位体:',
            'plot_same_name': '同じ名前の同位体をプロットする',
            'input_age_label': '入力された時代',
            'selected_half_life': '選択された同位体の半減期',
            'nearest_isotope': '入力された時代に最も近い同位体',
            'half_life_years': '年 (半減期)'
        }
