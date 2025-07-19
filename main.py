import requests
import time

TOKEN = "8064402986:AAF8Wh9hpykcJYawFmpocZAANBBEMNy47P4"
URL = f"https://api.telegram.org/bot{TOKEN}/"

OWNER_ID = 7817919248

TASK_TEXT = (
    "ЗАДАНИЯ 1 ПЕРЕЙДИТЕ ПО ССЫЛКЕ И ПОДПИШИТЕСЬ НА КАНАЛЫ "
    "И ОТПРАВЬТЕ СКРИН В БОТА\n"
    "https://t.me/patrickstarsrobot?start=7817919248"
)

# Переменная для хранения ID пользователя, которому владелец сейчас отвечает
reply_target_user_id = None
awaiting_reply_message = False

def send_message(chat_id, text, reply_markup=None):
    data = {
        "chat_id": chat_id,
        "text": text,
    }
    if reply_markup:
        data["reply_markup"] = reply_markup
    requests.post(URL + "sendMessage", json=data)

def forward_message(chat_id_to, chat_id_from, message_id, reply_markup=None):
    data = {
        "chat_id": chat_id_to,
        "from_chat_id": chat_id_from,
        "message_id": message_id,
    }
    if reply_markup:
        data["reply_markup"] = reply_markup
    requests.post(URL + "forwardMessage", data=data)

def get_updates(offset=None):
    params = {"timeout": 100}
    if offset:
        params["offset"] = offset
    resp = requests.get(URL + "getUpdates", params=params)
    return resp.json()

def main():
    global reply_target_user_id, awaiting_reply_message
    update_id = None
    print("Бот запущен")

    while True:
        result = get_updates(update_id)
        if not result["ok"]:
            time.sleep(1)
            continue

        updates = result["result"]
        for update in updates:
            update_id = update["update_id"] + 1

            if "message" in update:
                message = update["message"]
                chat_id = message["chat"]["id"]
                text = message.get("text", "")
                message_id = message["message_id"]

                # Если владелец отвечает на кнопку "Ответить"
                if chat_id == OWNER_ID:
                    # Проверяем callback_query - кнопки работают через callback_query, но здесь у нас обычная клавиатура,
                    # поэтому кнопка "Ответить" будет в сообщении в виде текста.
                    if text == "/start":
                        keyboard = {
                            "keyboard": [["📝 ЗАДАНИЕ"]],
                            "resize_keyboard": True
                        }
                        send_message(chat_id, "Привет, хозяин! Нажми кнопку 👇", keyboard)
                    elif text == "📝 ЗАДАНИЕ":
                        send_message(chat_id, TASK_TEXT)
                    elif text.startswith("Ответить "):
                        # Команда "Ответить <user_id>"
                        parts = text.split()
                        if len(parts) == 2 and parts[1].isdigit():
                            reply_target_user_id = int(parts[1])
                            awaiting_reply_message = True
                            send_message(chat_id, f"Теперь ваши сообщения будут отправляться пользователю {reply_target_user_id}. Напишите текст ответа.")
                        else:
                            send_message(chat_id, "Неверная команда для ответа. Используй: Ответить <user_id>")
                    elif awaiting_reply_message:
                        if reply_target_user_id is not None:
                            # Отправляем сообщение пользователю
                            send_message(reply_target_user_id, f"Ответ от владельца:\n\n{text}")
                            send_message(chat_id, "Сообщение отправлено.")
                            awaiting_reply_message = False
                            reply_target_user_id = None
                        else:
                            send_message(chat_id, "Нет пользователя для ответа. Используйте команду Ответить <user_id>.")
                    else:
                        send_message(chat_id, "Не понимаю команду 😅")

                else:
                    # Пользователь
                    if text == "/start":
                        keyboard = {
                            "keyboard": [["📝 ЗАДАНИЕ"]],
                            "resize_keyboard": True
                        }
                        send_message(chat_id, "Добро пожаловать! Нажми кнопку 👇", keyboard)
                    elif text == "📝 ЗАДАНИЕ":
                        send_message(chat_id, TASK_TEXT)
                    elif "photo" in message:
                        # Переслать фото владельцу с кнопкой "Ответить <user_id>"
                        forward_message(OWNER_ID, chat_id, message_id)

                        keyboard = {
                            "keyboard": [[f"Ответить {chat_id}"]],
                            "resize_keyboard": True,
                            "one_time_keyboard": True
                        }
                        send_message(OWNER_ID, f"Пользователь @{chat_id} отправил скрин. Нажмите кнопку, чтобы ответить.", keyboard)
                        send_message(chat_id, "Спасибо! Скрин отправлен владельцу.")
                    else:
                        send_message(chat_id, "Я тебя не понял 😅")

        time.sleep(1)

if __name__ == "__main__":
    main()