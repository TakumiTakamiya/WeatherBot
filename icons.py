# pip install selenium webdriver-manager
import os

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# 文字列リスト
texts = ["☀️", "🌤️", "☁️", "🔥", "🌧️", "⛈️", "❓", "❄️", "😐", "😊", "🔥", "🌂", "☂️", "☔"]

# 保存先ディレクトリ
SAVED_DIRECTORY = os.path.abspath(os.path.join(__file__, os.pardir, "text_images"))
HTML_PATH = os.path.join(SAVED_DIRECTORY, "tmp.html")
os.makedirs(SAVED_DIRECTORY, exist_ok=True)

# 背景色
BG_COLOR = "#323339"

# Chrome 起動
options = webdriver.ChromeOptions()
# options.add_argument("--headless=new")
# options.add_argument("--disable-gpu")
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()), options=options
)

for idx, text in enumerate(texts):
    html = f"""
    <html>
      <body style="margin:0; padding:0; background-color:{BG_COLOR}; display:flex; justify-content:center; align-items:center; height:32px;">
        <div id="holder" style="width:20px;height:20px;justify-content:center; align-items:center;" >
        <div id="text" style="font-size:16px; font-family:'Noto Sans', 'Noto Color Emoji', sans-serif;" >{text}</div>
        </div>
      </body>
    </html>
    """
    with open(HTML_PATH, mode="w", encoding="utf-8") as f:
        f.write(html)
    driver.get(HTML_PATH)

    # 要素取得
    elem = driver.find_element(By.ID, "holder")

    # 要素サイズに合わせてウィンドウサイズ調整
    driver.set_window_size(400, 400)  # 少し余白を追加

    # スクショ保存
    elem.screenshot(f"text_images/text_{idx}.png")
    print(f"Saved text_{idx}.png: {text}")

driver.quit()
