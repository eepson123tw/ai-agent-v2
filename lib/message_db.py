from tinydb import TinyDB
from datetime import datetime
from time import time
from pathlib import Path
from datetime import datetime
import json

# 建立歷史記錄目錄
HISTORY_DIR = Path("history")
HISTORY_DIR.mkdir(parents=True, exist_ok=True)

# 格式化現在的時間為 "年_月_日_時分" 格式
current_time = datetime.now().strftime("%Y_%m_%d_%H%M%S")

db = TinyDB(
    HISTORY_DIR / f"message-{current_time}.json",
    encoding='utf-8',
    ensure_ascii=False,  # 確保中文不會被轉為 Unicode 跳脫序列
    indent=4  # 讓 JSON 檔案更易讀
)

def init_message(content=None):
    db.truncate()

    if content is not None:
        add_message(role="developer", content=content)


def add_message(content=None, role="user", **options):
    record = {
        "role": role,
        "content": content,
        "created_at": datetime.now().isoformat(),
    }

    if "tool_calls" in options:
        record["role"] = "assistant"
        record["content"] = None
        record["tool_calls"] = [
            tool_call.model_dump() for tool_call in options.get("tool_calls")
        ]

    if "tool_call_id" in options:
        record["role"] = "tool"
        record["tool_call_id"] = options.get("tool_call_id")
        if not isinstance(content, str) and content is not None:
            record["content"] = json.dumps(content)

    db.insert(record)
    return record

def get_messages():
    """
    回傳格式：
    [
      {"role": "developer", "content": "訊息內容"},
      {"role": "user", "content": "訊息內容"},
      {"role": "assistant", "content": "訊息內容"},
      {"role": "tool", "content": None, "tool_call_id": "call_9527"},
    ]
    """
    excluded_keys = {"id", "created_at"}

    messages = []
    for item in db.all():
        message = {k: v for k, v in item.items() if k not in excluded_keys}
        messages.append(message)

    return messages
