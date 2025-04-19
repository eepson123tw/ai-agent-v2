# 檔案：main.py
from message_db import init_message, add_message, get_messages
from lib import client
init_message("你是一位專門講關於貓的笑話大師，回答問題時請一律使用**台灣繁體中文**")

try:
    while True:
        user_question = input("請輸入你的問題(輸入 exit 可結束對話)：")

        if user_question.lower() == "exit":
            print("Bye!")
            break

        add_message(user_question.strip())  # 把 user prompt 存起來

        completion = client.chat.completions.create(
            model="gpt-4.1-nano",  # 選擇模型
            messages=get_messages(),
        )

        content = completion.choices[0].message.content
        add_message(content, role="assistant")  # 把 LLM 的回應也存起來

        print(content)
except EOFError:
    print("Bye!")
