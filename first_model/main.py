import streamlit as st
import pandas as pd
from model import predict_risk
import numpy as np

# Функция для отображения анимации фона
def set_background_color(risk_level):
    color = f"rgba({int(255 * risk_level)}, {int(255 * (1 - risk_level))}, 0, 0.5)"
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: linear-gradient(90deg, {color} 0%, {color} 100%);
            background-size: 400% 400%;
            animation: gradientBG 15s ease infinite;
        }}
        @keyframes gradientBG {{
            0% {{ background-position: 0% 50%; }}
            50% {{ background-position: 100% 50%; }}
            100% {{ background-position: 0% 50%; }}
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Анкета с Input ячейками
st.write("# Комплаенс-система для банка")

inn = st.sidebar.text_input("ИНН") or None
registration_date = st.sidebar.date_input("Дата регистрации") or None
capital = st.sidebar.text_input("Уставной капитал (руб)") or None
address = st.sidebar.text_input("Адрес") or None
ceo_name = st.sidebar.text_input("ФИО Генерального директора") or None
ceo_birthdate = st.sidebar.date_input("Дата рождения Генерального директора") or None
beneficiary_name = st.sidebar.text_input("ФИО Бенефициара") or None
main_okved = st.sidebar.text_input("Основной ОКВЭД") or None
additional_okved_count = st.sidebar.text_input("Кол-во дополнительных ОКВЭДОВ") or None
employee_count = st.sidebar.text_input("Кол-во сотрудников") or None
website = st.sidebar.text_input("Сайт") or None
phone_number = st.sidebar.text_input("Номер телефона") or None
provider = st.sidebar.text_input("Провайдер") or None
tax_system = st.sidebar.text_input("Система налогообложения") or None
client_activity = st.sidebar.text_input("Деятельность клиента") or None
client_activity_words = st.sidebar.text_input("Деятельность клиента со слов клиента") or None
employee_count_words = st.sidebar.text_input("Кол-во сотрудников со слов клиента") or None
planned_turnover_form = st.sidebar.text_input("Планируемый оборот по анкете (руб)") or None
planned_turnover_statement = st.sidebar.text_input("Планируемый оборот по снятию д/с (руб)") or None
income = st.sidebar.text_input("Доходы (тыс, руб.)") or None
zsk = st.sidebar.text_input("ЗСК") or None
negative_info = st.sidebar.text_input("Негативная информация") or None
negative_info_ceo = st.sidebar.text_input("Негатив относительно ГД") or None
fraudsters = st.sidebar.text_input("Мошенники") or None
registrar_services = st.sidebar.text_input("Сервисы регистраторы") or None
sim_lifetime_from_change = st.sidebar.text_input("Срок жизни SIM-карты/номера (от даты замены e/SIM-карты)") or None
sim_lifetime_current_device = st.sidebar.text_input("Срок жизни SIM в текущем пользовательском устройстве") or None
sim_lifetime_from_contract = st.sidebar.text_input("Срок жизни SIM-карты/номера (количество дней/часов/минут, которое прошло от даты заключения договора)") or None
tax_burden = st.sidebar.text_input("Налоговая нагрузка") or None

# Преобразование для отправки в model.py
data = pd.DataFrame(
    {
        "ИНН": [inn],
        "Дата регистрации": [registration_date],
        "Уставной капитал (руб)": [capital],
        "Адрес": [address],
        "ФИО Генерального директора": [ceo_name],
        "Дата рождения Генерального директора": [ceo_birthdate],
        "ФИО Бенефициара": [beneficiary_name],
        "Основной ОКВЭД": [main_okved],
        "Кол-во дополнительных ОКВЭДОВ": [additional_okved_count],
        "Кол-во сотрудников": [employee_count],
        "Сайт": [website],
        "Номер телефона": [phone_number],
        "Провайдер": [provider],
        "Система налогообложения": [tax_system],
        "Деятельность клиента": [client_activity],
        "Деятельность клиента со слов клиента": [client_activity_words],
        "Кол-во сотрудников со слов клиента": [employee_count_words],
        "Планируемый оборот по анкете (руб)": [planned_turnover_form],
        "Планируемый оборот по снятию д/с (руб)": [planned_turnover_statement],
        "Доходы (тыс, руб.)": [income],
        "ЗСК": [zsk],
        "Негативная информация": [negative_info],
        "Негатив относительно ГД": [negative_info_ceo],
        "Мошенники": [fraudsters],
        "Сервисы регистраторы": [registrar_services],
        "Срок жизни SIM-карты/номера (от даты замены e/SIM-карты)": [sim_lifetime_from_change],
        "Срок жизни SIM в текущем пользовательском устройстве": [sim_lifetime_current_device],
        "Срок жизни SIM-карты/номера (количество дней/часов/минут, которое прошло от даты заключения договора)": [sim_lifetime_from_contract],
        "Налоговая нагрузка": [tax_burden],
    }
)

# Предсказываем риск и выводим комментарий
if st.sidebar.button("Предсказать риск", type="primary"):
    risk_level = predict_risk(data)
    set_background_color(risk_level)
    st.header("Результаты прогнозирования")
    st.write(f"Уровень риска: {risk_level:.2f}")
    if risk_level < 0.3:
        st.write("Комментарий: Клиент имеет низкий уровень риска.")
    elif risk_level < 0.7:
        st.write("Комментарий: Клиент имеет средний уровень риска.")
    else:
        st.write("Комментарий: Клиент имеет высокий уровень риска.")
