import pandas as pd

# Чтение данных из CSV файла
data = pd.read_csv('data/base_data.csv')

# # МинМакс дата
# data["Дата регистрации"] = pd.to_datetime(data["Дата регистрации"], format='mixed', dayfirst=True, errors='coerce')
# min_date = data["Дата регистрации"].min()
# max_date = data["Дата регистрации"].max()

# # уникальные элементы
# unique_values = data["Система налогообложения"].unique()

# min_date = data["Кол-во сотрудников"].min()
# max_date = data["Кол-во сотрудников"].max()
# print(f'Min: {min_date}')
# print(f'Max: {max_date}')