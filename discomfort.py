EMOJIS = [
    ["cold", "cold"],  # ~5❄️❄️
    ["cold", "cold"],  # ~10❄️❄️
    ["cold", "cold"],  # ~15❄️❄️
    ["cold", "cold"],  # ~20❄️❄️
    ["cold", "cold"],  # ~25❄️❄️
    ["cold", "cold"],  # ~30❄️❄️
    ["cold", "cold"],  # ~35❄️❄️
    ["cold", "cold"],  # ~40❄️❄️
    ["cold", "cold"],  # ~45❄️❄️
    ["cold", "cold"],  # ~50❄️❄️
    ["cold", "cold"],  # ~55❄️❄️
    ["cold"],  # ~60❄️
    ["normal"],  # ~65😐
    ["good"],  # ~70😊
    ["normal"],  # ~75😐
    ["fire"],  # ~80🔥
    ["fire", "fire"],  # ~85🔥🔥
    ["fire", "fire", "fire"],  # ~85🔥🔥🔥
]


# 不快指数の計算
def discomfort_index(temp, hum):
    return round(0.81 * temp + 0.01 * hum * (0.99 * temp - 14.3) + 46.3, 1)


def discomfort_emoji(di: int):
    di = int(di)
    if di < 0:
        return EMOJIS[0]
    di //= 5
    if di >= len(EMOJIS):
        return EMOJIS[-1]
    return EMOJIS[di]
