import requests


animeToolsConfig = [
    {
        "type": "function",
        "function": {
            "name": "get_anime",
            "description": "取得隨機的動畫訊息",
            "parameters": {
                "type": "object",
                "properties": {
                    "anime": {
                        "type": "string",
                        "description": "需要將輸入轉換成動畫的英文名稱，如 ReLife",
                    }
                },
                "additionalProperties": False,
                "required": ["anime"],
            },
        },
    }
]


def get_anime(anime):
    BASE_URL = "https://api.animechan.io/v1/quotes/random"
    response = requests.get(BASE_URL)

    if response.status_code == 200:
        data = response.json()['data']
        id = data["anime"]["id"]
        name = data['anime']["name"]
        characterId = data['character']["id"]
        character = data['character']["name"]

        return {
            "id": id,
            "name": name,
            "characterId": characterId,
            "character": character,
        }
    else:
        return "❌ 無法取得動漫資料"
