import random
import pandas as pd
from date_reg import date_reg_prob
from neg_gd import neg_gd_prob
from neg_inf import neg_inf_prob
from nalog_per import nalog_per_prob

# проверка на None и преобразование в float
def check_None(col):
    if col == col:
        return float(col.replace(',', '.'))
    return None

def checks(row):
    if row != row:
        return None
    return row

# Основной сборщик кластеров
def predict_risk(data):
    '''
    Основной подсчёт вероятностей ансаблей и передача в main
    '''
    # метрика для вычисления итоговой вероятности указана в metrics.png
    # только не len(input а вывод модели)
    res = [
        date_reg_prob(data["Дата регистрации"]),
        neg_inf_prob(data["Негативная информация"]),
        neg_gd_prob(data["Негатив относительно ГД"]),
        check_None(data["Мошенники"]),
        checks(data["Сервисы регистраторы"]),
        nalog_per_prob(data["Система налогообложения"]),
        None # чтобы метрика не обнуляла пользователя со всеми данными, иначе он 0% рисков
    ]
    # проверка итоговых вероятностей print(res)
    # сумма заполненных значений
    inputs = sum(1 for x in res if x is not None)
    # веса, если у клиента мало информации значит подозрительный
    weights = (len(res) - inputs) / (len(res) - 1) # т.к 1 дата

    filtered_data = [x for x in res if x is not None]

    total_sum = sum(filtered_data)

    metrics = total_sum * weights

    # risk_level = random.uniform(0, 1)
    # data.to_csv('zeros.csv', index=False)
    return metrics
