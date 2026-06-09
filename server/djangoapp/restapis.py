# Uncomment the imports below before you add the function code
import requests
import os
from dotenv import load_dotenv
import urllib.parse

load_dotenv()

backend_url = os.getenv(
    'backend_url', default="http://localhost:3030")
sentiment_analyzer_url = os.getenv(
    'sentiment_analyzer_url',
    default="http://localhost:5050/")


def get_request(endpoint, **kwargs):
    params = ""
    if (kwargs):
        for key, value in kwargs.items():
            params = params+key+"="+value+"&"

    request_url = backend_url+endpoint+"?"+params

    print("GET from {} ".format(request_url))
    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(request_url)
        return response.json()
    except ImportError:
        # If any error occurs
        print("Network exception occurred")


def analyze_review_sentiments(text):
    # Защита от пустых отзывов (они тоже ломают ИИ)
    if not text:
        return {"sentiment": "neutral"}

    # Правильно кодируем текст (пробелы станут %20), чтобы не ломалась ссылка
    safe_text = urllib.parse.quote(text)

    # Собираем URL (с защитой от забытого слэша)
    base_url = sentiment_analyzer_url
    if not base_url.endswith('/'):
        base_url += '/'

    request_url = base_url + "analyze/" + safe_text
    # --- ДЕТЕКТИВНЫЙ БЛОК (ПЕЧАТАЕМ ВСЁ В ТЕРМИНАЛ) ---
    print("\n=== ЗАПРОС К ИИ ===")
    print(f"АДРЕС: {request_url}")

    try:
        response = requests.get(request_url)
        print(f"СТАТУС КОД: {response.status_code}")
        print(f"ОТВЕТ ИИ: {response.text}")
        print("===================\n")
        return response.json()
    except ImportError as e:
        print(f"КРИТИЧЕСКАЯ ОШИБКА: {e}")
        print("===================\n")
        # Возвращаем словарь-заглушку, чтобы сайт не падал с NoneType
        return {"sentiment": "neutral"}


def post_review(data_dict):
    request_url = backend_url+"/insert_review"
    try:
        response = requests.post(request_url, json=data_dict)
        print(response.json())
        return response.json()
    except ImportError:
        print("Network exception occurred")
