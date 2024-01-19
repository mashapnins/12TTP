import telebot
import numpy as np
#Чат-бот позволяющий повернуть матрицу на 90 градусов. Задание взято из файла "начальное задание2"
TOKEN = '6376183295:AAFw7YzJWmGrxj-Q9JfqGzIhWNxvJNRVR38'#Токен API для телеграмм бота
bot = telebot.TeleBot(TOKEN)

# Состояния бота
states = {}

# Команда для начала работы с ботом
@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Привет! Этот бот может поворачивать матрицу на 90 градусов.")

    # Инициализируем состояние пользователя
    states[chat_id] = {'matrix': None, 'direction': None}

# Команда для сброса состояния
@bot.message_handler(commands=['reset'])
def reset(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Состояние сброшено. Введите новую матрицу.")

    # Сбрасываем состояние пользователя
    states[chat_id] = {'matrix': None, 'direction': None}


# Обработка текстовых сообщений
@bot.message_handler(func=lambda message: True)
def handle_text(message):
    chat_id = message.chat.id
    current_state = states.get(chat_id, {})

    if message.text.lower() == '/reset':
        reset(message)
        return

    if current_state.get('matrix') is None:
        try:
            # Пытаемся преобразовать введенный текст в матрицу
            matrix = np.array([list(map(int, row.split())) for row in message.text.split('\n')])
            states[chat_id]['matrix'] = matrix

            bot.send_message(chat_id, "Матрица успешно принята. Выберите направление поворота: /clockwise или /counterclockwise")
        except ValueError:
            bot.send_message(chat_id, "Некорректный ввод матрицы. Попробуйте снова.")

    elif current_state.get('direction') is None:
        if message.text.lower() in ['/clockwise', '/counterclockwise']:
            states[chat_id]['direction'] = message.text.lower()
            rotated_matrix = rotate_matrix(states[chat_id]['matrix'], states[chat_id]['direction'])
            bot.send_message(chat_id, f"Повернутая матрица:\n{rotated_matrix}")
        else:
            bot.send_message(chat_id, "Выберите направление поворота: /clockwise или /counterclockwise")
            states[chat_id] = {'matrix': None, 'direction': None}

# Функция для поворота матрицы
def rotate_matrix(matrix, direction):
    if direction == '/clockwise':
        return np.rot90(matrix, -1)
    elif direction == '/counterclockwise':
        return np.rot90(matrix, 1)
    else:
        return matrix

if __name__ == "__main__":
    bot.polling(none_stop=True)
