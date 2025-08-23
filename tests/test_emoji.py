from discomfort import discomfort_emoji


def test_di_emoji():
    assert discomfort_emoji(-1) == "❄️❄️"
    assert discomfort_emoji(-10) == "❄️❄️"
    assert discomfort_emoji(59) == "❄️"
    assert discomfort_emoji(69) == "😊"
    assert discomfort_emoji(85) == "🔥🔥🔥"
    assert discomfort_emoji(100) == "🔥🔥🔥"
