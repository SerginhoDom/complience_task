import asyncio
import requests
import json
import sys

sys.stdout.reconfigure(encoding="utf-8")


async def get_company_info(itpn: str):
    url = f"https://egrul.itsoft.ru/{itpn}.json"

    response = requests.get(url)

    if response.status_code == 200:
        try:
            result = response.json()
            return result
        except json.JSONDecodeError:
            return {"error": "Could not decode JSON."}
    else:
        return {"error": f"Error {response.status_code}: {response.text}"}


async def extract_legal_entity_info(data):
    if not data:
        return {"error": "No data"}

    structured_data = list()

    # Проверяем наличие ключа 'СвЮЛ' в данных
    if "СвЮЛ" in data:
        ie_props = data["СвЮЛ"]

        # Извлекаем различные разделы данных
        le_name = ie_props.get("СвНаимЮЛ", {})
        le_address = ie_props.get("СвАдресЮЛ", {})
        ogr_reg = ie_props.get("СвРегОрг", {})
        okved = ie_props.get("СвОКВЭД", {})
        licence = ie_props.get("СвЛицензия", [])
        share_cap = ie_props.get("СвУстКап", {})

        # Извлекаем основные данные
        name = le_name.get("СвНаимЮЛПолн", "Не указано")
        itpn = ie_props.get("@attributes", {}).get("ИНН", "Не указан")
        ogrn = ie_props.get("@attributes", {}).get("ОГРН", "Не указан")
        kpp = ie_props.get("@attributes", {}).get("КПП", "Не указан")

        # Извлекаем адрес юридического лица
        address = (
            le_address.get("АдресРФ", {})
            .get("@attributes", {})
            .get("Индекс", "Не указан")
        )
        region = le_address.get("Регион", "Не указан")
        street = (
            le_address.get("Улица", {})
            .get("@attributes", {})
            .get("НаимУлица", "Не указана")
        )

        # Извлекаем информацию о регистрации
        registration_authority = ogr_reg.get("@attributes", {}).get(
            "НаимНО", "Не указано"
        )

        # Извлекаем дату регистрации
        registration_date = ie_props.get("@attributes", {}).get(
            "ДатаОГРН", "Не указана"
        )

        # Извлекаем ОКВЭД
        main_okved_code = (
            okved.get("СвОКВЭДОсн", {})
            .get("@attributes", {})
            .get("КодОКВЭД", "Не указан")
        )
        additional_okved = okved.get("СвОКВЭДДоп", [])
        additional_okved_count = len(
            additional_okved
        )  # Количество дополнительных ОКВЭД

        # Извлекаем уставной капитал
        capital_name = share_cap.get("@attributes", {}).get(
            "НаимВидКап", "Не указан"
        )
        capital_amount = share_cap.get("@attributes", {}).get(
            "СумКап", "Не указан"
        )

        # Формируем структурированные данные
        structured_data.append(f"Наименование: {name}")
        structured_data.append(f"ИНН: {itpn}")
        structured_data.append(f"ОГРН: {ogrn}")
        structured_data.append(f"КПП: {kpp}")
        structured_data.append(f"Адрес: {address}, {region}, {street}")
        structured_data.append(f"Орган регистрации: {registration_authority}")
        structured_data.append(f"Дата регистрации: {registration_date}")
        structured_data.append(f"Основной ОКВЭД (код): {main_okved_code}")
        structured_data.append(
            f"Количество дополнительных ОКВЭД: {additional_okved_count}"
        )
        structured_data.append(f"{capital_name}: {capital_amount}")

        if additional_okved_count > 0:
            structured_data.append("Дополнительные ОКВЭД:")
            for i, item in enumerate(additional_okved, 1):
                okved_code = item.get("@attributes", {}).get(
                    "КодОКВЭД", "Не указан"
                )
                structured_data.append(f"{i}. {okved_code}")

        # Лицензии
        licenses = []
        for license_item in licence:
            license_number = license_item.get("@attributes", {}).get(
                "НомЛиц", "Не указан"
            )
            license_date = license_item.get("@attributes", {}).get(
                "ДатаЛиц", "Не указана"
            )
            license_start = license_item.get("@attributes", {}).get(
                "ДатаНачЛиц", "Не указана"
            )
            license_end = license_item.get("@attributes", {}).get(
                "ДатаОкончЛиц", "Не указана"
            )
            license_activity = license_item.get("НаимЛицВидДеят", "Не указана")
            licenses.append(
                f"Лицензия № {license_number},"
                f"Дата начала: {license_start},"
                f"Дата окончания: {license_end},"
                f"Вид деятельности: {license_activity}"
            )

        if licenses:
            structured_data.append("Лицензии:")
            for license_info in licenses:
                structured_data.append(license_info)

    else:
        return {"error": "Could not find legal entity data"}

    return structured_data


async def extract_individual_info(data):
    if not data:
        return {"error": "No data"}

    structured_data = []

    # Проверяем наличие ключа 'СвИП' в данных
    if "СвИП" in data:
        ie = data["СвИП"]

        # Извлекаем различные разделы данных
        fl = ie.get("СвФЛ", {})
        email = ie.get("СвАдрЭлПочты", {})

        # Извлекаем основные данные
        ie_name = ie.get("@attributes", {}).get("НаимВидИП", "Не указано")
        itpn = ie.get("@attributes", {}).get("ИННФЛ", "Не указан")
        ogrn_ie = ie.get("@attributes", {}).get("ОГРНИП", "Не указан")

        # Извлекаем ФИО (Фамилия, Имя, Отчество)
        full_name = fl.get("ФИОРус", {}).get("@attributes", {})
        last_name = full_name.get("Фамилия", "Не указана")
        first_name = full_name.get("Имя", "Не указано")
        middle_name = full_name.get("Отчество", "Не указано")

        # Извлекаем электронную почту
        email = email.get("@attributes", {}).get("E-mail", "Не указан")

        # Извлекаем основной ОКВЭД
        okved = (
            ie.get("СвОКВЭД", {}).get("СвОКВЭДОсн", {}).get("@attributes", {})
        )
        okved_code = okved.get("КодОКВЭД", "Не указан")
        okved_name = okved.get("НаимОКВЭД", "Не указано")

        # Извлекаем неосновные ОКВЭД
        additional_okveds = ie.get("СвОКВЭД", {}).get("СвОКВЭДДоп", [])
        if isinstance(
            additional_okveds, dict
        ):  # Если только один неосновной ОКВЭД
            additional_okveds = [additional_okveds]
        additional_okved_codes = [
            okved.get("@attributes", {}).get("КодОКВЭД", "Не указан")
            for okved in additional_okveds
        ]

        # Извлекаем дату регистрации
        registration_date = ie.get("@attributes", {}).get(
            "ДатаОГРНИП", "Не указана"
        )

        # Формируем структурированные данные
        structured_data.append(f"Тип: {ie_name}")
        structured_data.append(f"ИНН: {itpn}")
        structured_data.append(f"ОГРНИП: {ogrn_ie}")
        structured_data.append(f"ФИО: {last_name.capitalize()} {first_name.capitalize()} {middle_name.capitalize()}")
        structured_data.append(f"Электронная почта: {email.lower()}")
        structured_data.append(f"Основной ОКВЭД: {okved_code} ({okved_name})")
        structured_data.append(f"Дата регистрации: {registration_date}")
        structured_data.append(
            f"Коды неосновных ОКВЭД: {', '.join(additional_okved_codes)}"
        )

    else:
        return {"error": "Could not find IE data"}

    return structured_data


async def extract_info(data):
    if not data:
        return {"error": "No data"}

    # Проверяем, какой тип данных у нас и извлекаем информацию в зависимости от типа
    if "СвИП" in data:
        return await extract_individual_info(data)  # ИП
    elif "СвЮЛ" in data:
        return await extract_legal_entity_info(data)  # Юридическое лицо
    else:
        return {"error": "Could not load org type"}

async def get_ogrn_by_itpn(itpn):
    company_info = await get_company_info(itpn)

    if "error" in company_info:
        print(company_info["error"])
    else:
        structured_info = await extract_info(company_info)
        return structured_info[2].split(": ")[1]


if __name__ == "__main__":
    itpn = "9404013080"
    print(asyncio.run(get_ogrn_by_itpn(itpn)))
