from lib import client,init_message, add_message, get_messages
from tools import animeToolsConfig,get_anime
import json
from utils.spinner import spinner

init_message("你是一位聰明的助理，回答問題的時候請一律使用**台灣繁體中文**")
add_message("推薦我一個隨機動畫")  # 為求方便，先固定問題

AVAILABLE_TOOLS = {"get_anime": get_anime}


spinner.start()
completion = client.chat.completions.create(
    model="gpt-4.1-nano",  # 選擇模型
    messages=get_messages(),
    tools=animeToolsConfig,
    tool_choice="auto",
)
spinner.stop()

completion_message = completion.choices[0].message
tool_calls = completion_message.tool_calls

if tool_calls:
    add_message(tool_calls=tool_calls)

    for tool_call in tool_calls:
        function_name = tool_call.function.name
        arguments = tool_call.function.arguments

        fn = AVAILABLE_TOOLS.get(function_name)

        if fn is None:  # 如果沒有可執行函數就跳過
            continue

        try:
            args = json.loads(arguments)
        except json.JSONDecodeError:
            args = {}

        result = fn(**args)
        add_message(result, tool_call_id=tool_call.id)
    spinner.succeed("取得動畫資料")

    # 準備把結果交給 LLM 組織答案
    spinner.start()
    response = client.chat.completions.create(
        model='gpt-4.1-nano',
        messages=get_messages(),
    )
    spinner.stop()
    print(response.choices[0].message.content)
else:
    print(completion_message.content)
