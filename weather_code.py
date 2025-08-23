import os

LOG_PATH = os.path.abspath(os.path.join(__file__, os.pardir, "INVALID_CODES.txt"))


def weather_emoji(code):
    if code == 0:
        return ["sun"]  # 晴天☀️
    elif code in [1, 2]:
        return ["sun_cloud"]  # 晴れ🌤️
    elif code in [3, 45, 48]:
        return ["cloud"]  # 曇り☁️
    elif (51 <= code <= 67) or (80 <= code <= 82):
        return ["rain"]  # 雨🌧️
    elif code in [95, 96, 99]:
        return ["thunder"]  # 雷雨⛈️
    else:
        with open(LOG_PATH, mode="a") as f:
            f.write(f"{code}\n")
        return ["question"]
