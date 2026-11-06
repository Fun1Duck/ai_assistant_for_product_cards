from texts import system_promt
from config import bot_hub_API
from openai import OpenAI
import json
import sys


client_bot_hub = OpenAI(api_key=bot_hub_API,
                base_url='https://openai.bothub.chat/v1')

def func(user_text, history):
    if history:
        history = history[-6:]

    history.append({"role": "user", "content": user_text})

    messages = [
        {"role": "system", "content": system_promt},
        *history
    ]

    try:
        reply = client_bot_hub.chat.completions.create(
        messages=messages,
        # model='deepseek-chat-v3-0324',
        model='deepseek-v4-flash').choices[0].message.content.replace("```json", "").replace("```", "").strip()
        history.append({"role": "assistant", "content": reply})
        return history
    except Exception as e:
        print(f"🔴 Ошибка запроса к LLM: {e}")
        print('К сожалению не получилось обработать информацию. Попробуйте еще раз.')

history = []
print("Введите данные о товаре в формате JSON (для окончания нажмите Enter 2 раза:")
while True:
    user_text = []
    while True:
        line = input()
        if not line.strip():
            break
        user_text.append(line)

    user_text = ''.join(user_text)

    if not user_text:
        continue

    if user_text.lower() == 'выход':
        print("Хорошего дня!")
        break

    history = func(user_text, history)
    try:
        reply = history[-1]['content']
        json_reply = json.loads(reply)
        if json_reply['status'] == 'error':
            print(json_reply['error_message'])
        else:
            print(json.dumps(json_reply, indent=2, ensure_ascii=False))
            history = []
    except json.JSONDecodeError:
        print("🔴 Не получилось обработать JSON. Ответ модели:")
        print(reply)
    except Exception as e:
        print(f"🔴 Ошибка: {e}")
        print('Не получилось обработать JSON. Повторите попытку.')

    print("Введите данные о товаре в формате JSON (для окончания нажмите Enter 2 раза:")
