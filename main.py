import datetime
import os

import matplotlib.pyplot as plt
import requests
from dotenv import load_dotenv

from bot import SimpleDiscordBot
from create_image import draw
from discomfort import discomfort_emoji, discomfort_index
from weather_code import weather_emoji

load_dotenv()
DARK_GRAY = "#323339"
LIGHT_GRAY = "#7b7c84"

# 新宿の座標
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
LAT = os.getenv("LAT")
LON = os.getenv("LON")
USER_ID = os.getenv("USER_ID")
today = datetime.date.today().isoformat()

# Open-Meteo API（気温・湿度・天気コード取得）
API_URL = (
    "https://api.open-meteo.com/v1/forecast"
    f"?latitude={LAT}&longitude={LON}"
    "&hourly=temperature_2m,relative_humidity_2m,weathercode,precipitation"
    "&timezone=Asia%2FTokyo"
)

# グラフの出力先
GRAPH_PATH = os.path.abspath(os.path.join(__file__, os.pardir, "graph.png"))


def generate_weather_image():
    plt.rcParams["font.family"] = "Noto Color Emoji"
    data = requests.get(API_URL).json()

    hours = data["hourly"]["time"]
    temps = data["hourly"]["temperature_2m"]
    humidity = data["hourly"]["relative_humidity_2m"]
    precip = data["hourly"]["precipitation"]
    codes = data["hourly"]["weathercode"]

    # 今日のデータだけ抽出
    precip_today = []
    w_emojis = []
    di_emojis = []

    for t, temp, hum, pr, code in zip(hours, temps, humidity, precip, codes):
        if t.startswith(today):
            time = int(t[11:13])
            if time >= 8 and time <= 23:
                precip_today.append(pr)
                w_emojis.append(weather_emoji(code))
                di_emojis.append(discomfort_emoji(discomfort_index(temp, hum)))

    draw(precip_today, w_emojis, di_emojis, GRAPH_PATH)


if __name__ == "__main__":
    generate_weather_image()
    SimpleDiscordBot().send_image(GRAPH_PATH)
