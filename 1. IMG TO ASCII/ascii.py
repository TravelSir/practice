# -*- coding: utf-8 -*-
from PIL import Image

IMG = 'ascii.png'
WIDTH = 80
HEIGHT = 80
OUTPUT = "output.txt"

ascii_char = list("$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. ")


# 将256灰度映射到70个字符上
def get_char(r, g, b, alpha=256):
    if alpha == 0:
        return ' '
    length = len(ascii_char)
    gray = int(0.2126 * r + 0.7152 * g + 0.0722 * b)

    unit = (256.0 + 1)/length
    return ascii_char[int(gray/unit)]


if __name__ == '__main__':

    im = Image.open(IMG)
    im = im.resize((WIDTH, HEIGHT))
    im = im.convert("RGBA")  # 需转成RGBA格式
    txt = ""
    for i in range(HEIGHT):
        for j in range(WIDTH):
            args = im.getpixel((j, i))
            txt += get_char(*args)
        txt += '\n'

    print(txt)

# 字符画输出到文件
    with open(OUTPUT, 'w') as f:
        f.write(txt)
