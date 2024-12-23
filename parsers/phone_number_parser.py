import requests
import sys

sys.stdout.reconfigure(encoding='utf-8')

# Ваши ключи API DaData
API_TOKEN = "d7185ab2d01515744175976521d9890fc17cc77c"
API_SECRET = "d7d50d85ce089c06fd7c9cd436ab5b8e527ccb78"

API_URL = "https://dadata.ru/api/v2/clean/phone"

def get_phone_info(phone_number):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Token {API_TOKEN}",
        "X-Secret": API_SECRET  # Секретный ключ
    }
    data = [phone_number]  # API ожидает массив данных
    response = requests.post(API_URL, json=data, headers=headers)
    
    if response.status_code == 200:
        result = response.json()[0]
        return {
            "исходный номер": phone_number,
            "нормализованный номер": result.get("phone"),
            "оператор": result.get("provider"),
            "регион": result.get("region"),
            "страна": result.get("country"),
            "часовой пояс": result.get("timezone"),
        }
    else:
        return {"error": f"Ошибка {response.status_code}: {response.text}"}

# Пример использования
phone_number = "79872457647"
info = get_phone_info(phone_number)

if "error" in info:
    print(info["error"])
else:
    for key, value in info.items():
        print(f"{key}: {value}")