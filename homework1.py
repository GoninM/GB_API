import requests
import json
from config import GIT_USERNAME, GIT_TOKEN


if __name__ == "__main__":
    url = f"https://api.github.com/users/{GIT_USERNAME}/repos"
    response = requests.get(url).json()
    print(json.dumps(response, indent=4))

    print('1. Посмотреть документацию к API GitHub, '
          'разобраться как вывести список репозиториев для конкретного пользователя, '
          'сохранить JSON-вывод в файле *.json.')

    file = "homework1_task1_result.json"
    with open(file, "w") as f:
        for r in response:
            f.write(f'folder_name: {r["name"]}, url: {r["html_url"]}\n')

    print('2. Изучить список открытых API (https://www.programmableweb.com/category/all/apis). '
          'Найти среди них любое, требующее авторизацию (любого типа). '
          'Выполнить запросы к нему, пройдя авторизацию. Ответ сервера записать в файл.')

    file = "homework1_task2_result.txt"
    headers = {'Authorization': 'token ' + GIT_TOKEN}
    login = requests.get(url, headers=headers)
    print(login)
    print(json.dumps(login.json(), indent=4))

    with open(file, "w") as f:
        for r in response:
            f.write(json.dumps(login.json(), indent=4))
