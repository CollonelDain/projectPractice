import requests
from django.conf import settings
from django.http import JsonResponse


def get_food(table_id):
    NOCODB_API_KEY = 'W5lGHoDSDNQf7gBbXvqr8CyHWg3GukNWQhr3BH2I'
    NOCODB_BASE_URL = 'https://app.nocodb.com/api/v2/' 
    url = f'{NOCODB_BASE_URL}tables/{table_id}/records'
    headers = {'xc-token': NOCODB_API_KEY}
    params = {'limit': 25}  # Можно задать другие параметры запроса
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f'Ошибка при получении данных: {response.text}')



def get_nocodb_data(request):
    NOCODB_API_KEY = 'W5lGHoDSDNQf7gBbXvqr8CyHWg3GukNWQhr3BH2I'
    NOCODB_BASE_URL = 'https://app.nocodb.com/api/v2/' 
    url = f'{NOCODB_BASE_URL}tables/mibm6agaouy0jey/records'
    headers = {'xc-token': NOCODB_API_KEY}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()  
        records = data.get('list', [])

        response_data = {
            "nocodb-data": "http://localhost:8000/nocodb-data/",  # Ссылка на таблицу
            "records": records  # Данные таблицы
        }
        return JsonResponse(response_data, status=200)
    else:
        # Если произошла ошибка, возвращаем пустой JSON
        return JsonResponse({"error": "Не удалось получить данные из NocoDB"}, status=response.status_code)

