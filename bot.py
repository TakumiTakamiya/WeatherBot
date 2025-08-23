import os

import requests
from dotenv import load_dotenv

load_dotenv()


class SimpleDiscordBot:
    def __init__(self, token_env: str = "DISCORD_TOKEN"):
        self._token = os.getenv(token_env, None)
        self._user_id = os.getenv("USER_ID", None)  # 送信相手のユーザーID

        if not self._token or not self._user_id:
            print("[SimpleDiscordBot] Missing environment variables.")
            self._valid = False
        else:
            self._valid = True

    def _get_dm_channel(self) -> str | None:
        """ユーザーとのDMチャネルを取得（なければ作成）"""
        try:
            url = "https://discord.com/api/v10/users/@me/channels"
            headers = {"Authorization": f"Bot {self._token}"}
            data = {"recipient_id": self._user_id}
            r = requests.post(url, headers=headers, json=data)
            if r.status_code == 200 or r.status_code == 201:
                return r.json()["id"]
            else:
                print(f"[SimpleDiscordBot] DM channel error: {r.status_code} {r.text}")
                return None
        except Exception as e:
            print(f"[SimpleDiscordBot] _get_dm_channel error: {e}")
            return None

    def send_text(self, message: str) -> bool:
        """DMでテキストメッセージ送信"""
        if not self._valid:
            return False
        try:
            channel_id = self._get_dm_channel()
            if not channel_id:
                return False
            url = f"https://discord.com/api/v10/channels/{channel_id}/messages"
            headers = {"Authorization": f"Bot {self._token}"}
            data = {"content": message}
            r = requests.post(url, headers=headers, json=data)
            return r.status_code in (200, 201)
        except Exception as e:
            print(f"[SimpleDiscordBot] send_text error: {e}")
            return False

    def send_image(self, filepath: str, message: str = "") -> bool:
        """DMで画像付きメッセージ送信"""
        if not self._valid:
            return False
        try:
            channel_id = self._get_dm_channel()
            if not channel_id:
                return False
            url = f"https://discord.com/api/v10/channels/{channel_id}/messages"
            headers = {"Authorization": f"Bot {self._token}"}
            with open(filepath, "rb") as f:
                files = {"file": (os.path.basename(filepath), f)}
                data = {"content": message}
                r = requests.post(url, headers=headers, data=data, files=files)
            return r.status_code in (200, 201)
        except Exception as e:
            print(f"[SimpleDiscordBot] send_image error: {e}")
            return False
