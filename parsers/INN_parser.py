import requests
import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

# URL для получения данных по ИНН
BASE_URL = "https://egrul.itsoft.ru/"

def get_company_info(inn):
    url = f"{BASE_URL}{inn}.json"
    
    response = requests.get(url)
    
    if response.status_code == 200:
        try:
            result = response.json()
            return result
        except json.JSONDecodeError:
            return {"error": "Не удалось декодировать JSON."}
    else:
        return {"error": f"Ошибка {response.status_code}: {response.text}"}

def extract_legal_entity_info(data):
    if not data:
        return {"error": "Нет данных"}

    structured_data = []
    
    # Проверяем наличие ключа 'СвЮЛ' в данных
    if 'СвЮЛ' in data:
        свюл = data['СвЮЛ']
        
        # Извлекаем различные разделы данных
        свнаимюл = свюл.get('СвНаимЮЛ', {})
        свадресюл = свюл.get('СвАдресЮЛ', {})
        сврегорг = свюл.get('СвРегОрг', {})
        своквед = свюл.get('СвОКВЭД', {})
        свлицензия = свюл.get('СвЛицензия', [])
        свусткап = свюл.get('СвУстКап', {})
        
        # Извлекаем основные данные
        name = свнаимюл.get('СвНаимЮЛПолн', 'Не указано')
        inn = свюл.get('@attributes', {}).get('ИНН', 'Не указан')
        ogrn = свюл.get('@attributes', {}).get('ОГРН', 'Не указан')
        kpp = свюл.get('@attributes', {}).get('КПП', 'Не указан')
        
        # Извлекаем адрес юридического лица
        address = свадресюл.get('АдресРФ', {}).get('@attributes', {}).get('Индекс', 'Не указан')
        region = свадресюл.get('Регион', 'Не указан')
        street = свадресюл.get('Улица', {}).get('@attributes', {}).get('НаимУлица', 'Не указана')
        
        # Извлекаем информацию о регистрации
        registration_authority = сврегорг.get('@attributes', {}).get('НаимНО', 'Не указано')
        
        # Извлекаем дату регистрации
        registration_date = свюл.get('@attributes', {}).get('ДатаОГРН', 'Не указана')
        
        # Извлекаем ОКВЭД
        main_okved_code = своквед.get('СвОКВЭДОсн', {}).get('@attributes', {}).get('КодОКВЭД', 'Не указан')
        additional_okved = своквед.get('СвОКВЭДДоп', [])
        additional_okved_count = len(additional_okved)  # Количество дополнительных ОКВЭД
        
        # Извлекаем уставной капитал
        capital_name = свусткап.get('@attributes', {}).get('НаимВидКап', 'Не указан')
        capital_amount = свусткап.get('@attributes', {}).get('СумКап', 'Не указан')
        
        # Формируем структурированные данные
        structured_data.append(f"Наименование: {name}")
        structured_data.append(f"ИНН: {inn}")
        structured_data.append(f"ОГРН: {ogrn}")
        structured_data.append(f"КПП: {kpp}")
        structured_data.append(f"Адрес: {address}, {region}, {street}")
        structured_data.append(f"Орган регистрации: {registration_authority}")
        structured_data.append(f"Дата регистрации: {registration_date}")
        structured_data.append(f"Основной ОКВЭД (код): {main_okved_code}")
        structured_data.append(f"Количество дополнительных ОКВЭД: {additional_okved_count}")
        structured_data.append(f"{capital_name}: {capital_amount}")
        
        if additional_okved_count > 0:
            structured_data.append("Дополнительные ОКВЭД:")
            for i, item in enumerate(additional_okved, 1):
                okved_code = item.get('@attributes', {}).get('КодОКВЭД', 'Не указан')
                structured_data.append(f"{i}. {okved_code}")
        
        # Лицензии
        licenses = []
        for license_item in свлицензия:
            license_number = license_item.get('@attributes', {}).get('НомЛиц', 'Не указан')
            license_date = license_item.get('@attributes', {}).get('ДатаЛиц', 'Не указана')
            license_start = license_item.get('@attributes', {}).get('ДатаНачЛиц', 'Не указана')
            license_end = license_item.get('@attributes', {}).get('ДатаОкончЛиц', 'Не указана')
            license_activity = license_item.get('НаимЛицВидДеят', 'Не указана')
            licenses.append(f"Лицензия № {license_number}, Дата начала: {license_start}, Дата окончания: {license_end}, Вид деятельности: {license_activity}")
        
        if licenses:
            structured_data.append("Лицензии:")
            for license_info in licenses:
                structured_data.append(license_info)
        
    else:
        return {"error": "Не удалось найти раздел СвЮЛ в данных"}

    return structured_data

def extract_individual_info(data):
    if not data:
        return {"error": "Нет данных"}

    structured_data = []

    # Проверяем наличие ключа 'СвИП' в данных
    if 'СвИП' in data:
        свип = data['СвИП']

        # Извлекаем различные разделы данных
        свфл = свип.get('СвФЛ', {})
        свадр = свип.get('СвАдрЭлПочты', {})

        # Извлекаем основные данные
        name_ip = свип.get('@attributes', {}).get('НаимВидИП', 'Не указано')
        inn = свип.get('@attributes', {}).get('ИННФЛ', 'Не указан')
        ogrnip = свип.get('@attributes', {}).get('ОГРНИП', 'Не указан')

        # Извлекаем ФИО (Фамилия, Имя, Отчество)
        fio = свфл.get('ФИОРус', {}).get('@attributes', {})
        last_name = fio.get('Фамилия', 'Не указана')
        first_name = fio.get('Имя', 'Не указано')
        middle_name = fio.get('Отчество', 'Не указано')

        # Извлекаем электронную почту
        email = свадр.get('@attributes', {}).get('E-mail', 'Не указан')

        # Извлекаем основной ОКВЭД
        оквэд = свип.get('СвОКВЭД', {}).get('СвОКВЭДОсн', {}).get('@attributes', {})
        okved_code = оквэд.get('КодОКВЭД', 'Не указан')
        okved_name = оквэд.get('НаимОКВЭД', 'Не указано')

        # Извлекаем неосновные ОКВЭД
        additional_okveds = свип.get('СвОКВЭД', {}).get('СвОКВЭДДоп', [])
        if isinstance(additional_okveds, dict):  # Если только один неосновной ОКВЭД
            additional_okveds = [additional_okveds]
        additional_okved_codes = [
            okved.get('@attributes', {}).get('КодОКВЭД', 'Не указан')
            for okved in additional_okveds
        ]

        # Извлекаем дату регистрации
        registration_date = свип.get('@attributes', {}).get('ДатаОГРНИП', 'Не указана')

        # Формируем структурированные данные
        structured_data.append(f"Тип: {name_ip}")
        structured_data.append(f"ИНН: {inn}")
        structured_data.append(f"ОГРНИП: {ogrnip}")
        structured_data.append(f"ФИО: {last_name} {first_name} {middle_name}")
        structured_data.append(f"Электронная почта: {email}")
        structured_data.append(f"Основной ОКВЭД: {okved_code} ({okved_name})")
        structured_data.append(f"Дата регистрации: {registration_date}")
        structured_data.append(f"Коды неосновных ОКВЭД: {', '.join(additional_okved_codes)}")

    else:
        return {"error": "Не удалось найти раздел СвИП в данных"}

    return structured_data

def extract_info(data):
    if not data:
        return {"error": "Нет данных"}

    # Проверяем, какой тип данных у нас и извлекаем информацию в зависимости от типа
    if 'СвИП' in data:
        return extract_individual_info(data)  # ИП
    elif 'СвЮЛ' in data:
        return extract_legal_entity_info(data)  # Юридическое лицо
    else:
        return {"error": "Не удалось определить тип организации"}


# Пример использования
# 772390884423 - пчел
# 7730588444 - ООО
inn = "7730588444"
company_info = get_company_info(inn)

# Выводим результат
if "error" in company_info:
    print(company_info["error"])
else:
    # Выводим структурированную информацию
    structured_info = extract_info(company_info)
    for item in structured_info:
        print(item)
