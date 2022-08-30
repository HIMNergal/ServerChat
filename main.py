from flask import Flask, request, render_template  # Подключить Фласк
from datetime import datetime
import json

# json.load - загрузить данные из файла
# json.dump - сохранить данные в файл

app = Flask(__name__)

MESSAGES_FILENAME = "messages_file.json" # Имя файла с сообщением

# Загружеат сообщения из файла
def load_messages():
    # 1. Открыть файл
    message_file = open(MESSAGES_FILENAME, "r")
    # 2. Прочитать структуру данных из файла
    data = json.load(message_file)
    # 3. Взять сообщение из структуры
    return data["messages"] # Возвращаем пустой список в качестве заглушки

all_messages = load_messages()  # Список всех сообщений



# Сохранять все сообщения в файл
def save_messages():
    # 1. Открыть файл
    message_file = open(MESSAGES_FILENAME, "w")
    # 2. Приготовить стуктуру данных
    data = {
        "messages": all_messages
    }
     # 3. Структуру данных записать в файл
    json.dump(data, message_file)


# Функция добавления нового сообщения
# Пирмер: add_message("Вася", "Оставь мне свой контакный номер")
def add_message(sender, text):
    # <= начинается с отступа код внутри этой функции
    # Создавать новое сообщение (новую структуру - словарь)
    new_message = {
        "text": text,
        "sender": sender,
        "time": datetime.now().strftime("%H:%M"), # "часы:минуты"
    }
    # Добавлять сообщения в список
    all_messages.append(new_message)
    save_messages()

# Функция вывода всех сообщений
def print_all():
    for msg in all_messages:
        print(f'[{msg["sender"]}]: {msg["text"]} / {msg["time"]}')


# Пример вызова функции без параметров
print_all()


@app.route("/")
def main_page():
    return "Welcome to ChatServer"


@app.route("/get_messages")
def get_messages():
    return {"messages": all_messages}

def filter_text(text):
    if 1000 < len(text) < 2:
        return "%FILTERED%"
    else:
        return text

def filter_name(name):
    if 100 < len(name) < 3:
        return "%FILTERED%"
    else:
        return name
@app.route("/send_message")
def send_message():
    text = filter_text(request.args["text"])
    name = filter_name(request.args["name"])
    add_message(name, text)
    return "ok"

@app.route("/chat")
def chat():
    return render_template("form.html") # Отображаем визуальный интерфейс из файла form.html

# Добавление сообщения
# UI: поля для ввода имени и текста и кнопки "отправить"

app.run(host="0.0.0.0", port=80)