import os

from PIL import Image, ImageDraw, ImageFont

# 背景色
BG_COLOR = "#323339"
LINE_COLOR = "#3a3b41"
RAIN_COLOR = "#7bb0f5"
TEXT_COLOR = "#ffffff"

RAIN_ZERO = 150
RAIN_MAX = 20
RAIN_UNIT = (RAIN_ZERO - RAIN_MAX) / 15

EMOJIS_IMAGE_FOLDER = os.path.abspath(os.path.join(__file__, os.pardir, "emoji_images"))
EMOJI_IMAGE_SIZE = 20

HOUR_UP = 160

WEATHER_UP = 180

DISCOMFORT_UP = WEATHER_UP + EMOJI_IMAGE_SIZE + 4


def create_canvas(
    width: int,
    height: int,
) -> Image.Image:
    """
    幅・高さ・背景色指定でRGBAキャンバス作成。
    bg_color は (R,G,B) か (R,G,B,A)
    """
    return Image.new("RGB", (width, height), BG_COLOR)


def draw_rounded_rectangle(
    img: Image.Image, xy: tuple, radius: int, fill=None, outline=None, outline_width=1
):
    """
    xy = (left, top, right, bottom)
    radius = 角丸半径
    fill = 塗り色 (R,G,B) か (R,G,B,A) または None
    outline = 線色
    """
    draw = ImageDraw.Draw(img)
    # ImageDraw の rounded_rectangle を使う（Pillow 5.0以上）
    draw.rounded_rectangle(
        xy, radius=radius, fill=fill, outline=outline, width=outline_width
    )


def draw_line(img: Image.Image, xy: tuple, color=(0, 0, 0, 255), width=1):
    """
    xy = (x1,y1,x2,y2)
    color = (R,G,B) or (R,G,B,A)
    """
    draw = ImageDraw.Draw(img)
    draw.line(xy, fill=color, width=width)


def paste_png(img: Image.Image, png_path: str, topleft: tuple):
    """
    png_path を読み込んで、座標 topleft (x,y) に貼り付ける。
    透過は保持。拡大縮小はしない。
    """
    with Image.open(png_path) as im:
        im = im.convert("RGBA")
        img.paste(im, topleft, im)  # mask を指定して透過を保持


def draw_text(
    img: Image.Image,
    position: tuple,
    text: str,
    font_path: str = None,
    font_size: int = 20,
    fill=(0, 0, 0, 255),
):
    """
    ASCIIテキストを描画。font_path を指定しなければ Pillow のデフォルトフォントを使用（小さい）。
    position = (x,y)
    """
    draw = ImageDraw.Draw(img)
    if font_path and os.path.exists(font_path):
        font = ImageFont.truetype(font_path, font_size)
    else:
        try:
            # 可能であれば DejaVuSans 系を使用（環境によっては存在）
            font = ImageFont.truetype("DejaVuSans.ttf", font_size)
        except Exception:
            font = ImageFont.load_default()
    draw.text(position, text, font=font, fill=fill)


def example_usage():
    # キャンバス作成
    canvas = create_canvas(800, 600)

    # 角丸長方形を描画（左上100,100 右下400,300、角丸半径20、塗り=青、線=濃い青）
    draw_rounded_rectangle(
        canvas,
        (100, 100, 400, 300),
        radius=20,
        fill=(100, 150, 255, 255),
        outline=(30, 60, 180, 255),
        outline_width=3,
    )

    # 別の角丸長方形（半透明）を重ねる
    draw_rounded_rectangle(
        canvas,
        (350, 200, 700, 500),
        radius=40,
        fill=(255, 200, 100, 200),
        outline=(200, 120, 30, 255),
        outline_width=4,
    )

    # 線分（座標指定、太さ指定）
    draw_line(canvas, (50, 50, 750, 50), color=(0, 0, 0, 255), width=2)
    draw_line(canvas, (50, 75, 750, 200), color=(120, 40, 200, 255), width=6)

    # PNG画像を貼る（透過PNGを想定）。座標は左上。
    # test_overlay.png は同じフォルダに用意しておくこと
    overlay_path = "test_overlay.png"
    if os.path.exists(overlay_path):
        paste_png(canvas, overlay_path, (500, 20))
    else:
        # 無ければ小さいサンプルを自作して貼ってみる（透明背景）
        tmp = Image.new("RGBA", (120, 80), (0, 0, 0, 0))
        draw_tmp = ImageDraw.Draw(tmp)
        draw_tmp.ellipse(
            (10, 10, 110, 70), fill=(255, 0, 0, 200), outline=(255, 255, 255, 255)
        )
        canvas.paste(tmp, (500, 20), tmp)

    # ASCII テキストを描画
    draw_text(
        canvas, (120, 320), "Hello, Pillow!", font_size=28, fill=(10, 10, 10, 255)
    )

    # 保存
    out_path = "output_example.png"
    canvas.convert("RGB").save(out_path, "PNG")  # 透過不要ならRGBに変換しても良い
    print(f"Saved example to {out_path}")


def hour_text(i):
    period = "AM" if i < 12 else "PM"
    dh = f"{i%12}" if i % 10 < i else f" {i%12}"
    return f"{period}{dh}:00"


def draw(
    rains: list[int],
    weathers: list[list[str]],
    discomforts: list[list[str]],
    output_path: str,
):
    # キャンバス作成
    canvas = create_canvas(875, DISCOMFORT_UP + EMOJI_IMAGE_SIZE + 20)

    # 降水量線分
    for i in [0, 2, 5, 10]:
        height = int(RAIN_ZERO - RAIN_UNIT * i)
        draw_line(canvas, (25, height, 850, height), color=LINE_COLOR, width=2)
        if i != 0:
            paste_png(
                canvas,
                os.path.join(EMOJIS_IMAGE_FOLDER, f"rain_{i}.png"),
                (850, height - EMOJI_IMAGE_SIZE // 2),
            )

    # 降水量を描画
    for i, r in enumerate(rains):
        if r != 0:
            draw_rounded_rectangle(
                canvas,
                (
                    50 + 50 * i - 20,
                    max(int(RAIN_ZERO - RAIN_UNIT * r), RAIN_MAX),
                    50 + 50 * i + 20,
                    RAIN_ZERO,
                ),
                radius=10,
                fill=RAIN_COLOR,
                outline=RAIN_COLOR,
                outline_width=0,
            )

    # PNG画像を貼る（透過PNGを想定）。座標は左上。
    for i, d in enumerate(discomforts):
        center = 50 + 50 * i
        width = EMOJI_IMAGE_SIZE * len(d)
        if len(d) != 3:
            for j, name in enumerate(d):
                paste_png(
                    canvas,
                    os.path.join(EMOJIS_IMAGE_FOLDER, f"{name}.png"),
                    (center - width // 2 + EMOJI_IMAGE_SIZE * j, DISCOMFORT_UP),
                )
        else:
            paste_png(
                canvas,
                os.path.join(EMOJIS_IMAGE_FOLDER, f"{d[0]}.png"),
                (center - EMOJI_IMAGE_SIZE // 2, DISCOMFORT_UP),
            )
            for j, name in enumerate(d[1:]):
                paste_png(
                    canvas,
                    os.path.join(EMOJIS_IMAGE_FOLDER, f"{name}.png"),
                    (
                        center + EMOJI_IMAGE_SIZE * (j - 1),
                        DISCOMFORT_UP + EMOJI_IMAGE_SIZE,
                    ),
                )

    for i, w in enumerate(weathers):
        center = 50 + 50 * i
        width = EMOJI_IMAGE_SIZE * len(w)
        for j, name in enumerate(w):
            paste_png(
                canvas,
                os.path.join(EMOJIS_IMAGE_FOLDER, f"{name}.png"),
                (center - width // 2 + EMOJI_IMAGE_SIZE * j, WEATHER_UP),
            )

    # ASCII テキストを描画
    for i in range(16):
        draw_text(
            canvas,
            (30 + i * 50, HOUR_UP),
            hour_text(i + 8),
            font_size=28,
            fill=TEXT_COLOR,
        )

    # 保存
    canvas.convert("RGB").save(output_path, "PNG")
