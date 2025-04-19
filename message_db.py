# 檔案：message_db.py

from tinydb import TinyDB
from datetime import datetime
from time import time
from pathlib import Path


# 建立歷史記錄目錄
HISTORY_DIR = Path("history")
HISTORY_DIR.mkdir(parents=True, exist_ok=True)

# 使用直接設定參數的方式初始化 TinyDB
db = TinyDB(
    HISTORY_DIR / f"message-{int(time())}.json",
    encoding='utf-8',
    ensure_ascii=False,  # 確保中文不會被轉為 Unicode 跳脫序列
    indent=4  # 讓 JSON 檔案更易讀
)


def init_message(content=None):
    db.truncate()

    if content is not None:
        add_message(role="developer", content=content)


def add_message(content=None, role="user"):
    if content is not None:
        return db.insert(
            {
                "role": role,
                "content": content,
                "created_at": datetime.now().isoformat(),
            }
        )


def get_messages():
    """
    回傳格式：
    [
      {"role": "developer", "content": "訊息內容"},
      {"role": "user", "content": "訊息內容"},
      ...
    ]
    """
    return [
        {
            "role": item["role"],
            "content": item["content"],
        }
        for item in db.all()
    ]
