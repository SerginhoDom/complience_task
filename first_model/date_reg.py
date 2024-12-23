from datetime import datetime

def date_reg_prob(data):
    input_date_str = data
    input_date = datetime.strptime(input_date_str, "%m/%d/%Y").date()

    # MinMax взяты из preprocessin.py
    min_date = datetime.strptime("2021-01-01", "%Y-%m-%d").date()
    max_date = datetime.strptime("2024-12-22", "%Y-%m-%d").date()

    total_days = (max_date - min_date).days
    input_days = (input_date - min_date).days

    normalized_value = input_days / total_days

    return normalized_value