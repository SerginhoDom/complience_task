def nalog_per_prob(data):
    # Протестить, правильно ли работает и верные ли оценки
    if data != data:
        return None

    priority_mapping = {
        'ОСН': 0.6,
        'УСН 15%': 0.3,
        'УСН 6%': 0.2,
        'ПСН (только для ИП)': 0.2,
        'АУСН': 0.4,
        'НПД': 0.1,
        'УСН 6% + ПСН': 0.3,
        'УСН 15% + ПСН': 0.5
    }

    return priority_mapping[data]