from PIL import Image
from colorama import init, Fore

PALLETS = [
    "█▓▒░ ",
    "█▓▒@MBHENR#░KWXDFPQASUZbdehx*8Gm&04LOVYkpq5Tagns69owz$CIu23Jcfry%1v7l+it[]{}?j|()=~!-/<>\"^_';,:`. ",
    "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/|()1{}[]?-_+~<>i!lI;:,\"^`'. ",
    "⣿⣾⣼⣸⡇⡅⡆⡂⡄⡁⡀⠀"]

init(autoreset=True)


def get_char(brightness, colors_table):
    step = 255 / len(colors_table)
    for i in range(1, len(colors_table) + 1):
        if i * step >= brightness:
            return colors_table[i - 1]


def image_to_text(colors_table, image_name, reverse):
    img = Image.open(f"sources/{image_name}")
    pixels = img.load()
    x, y = img.size
    text_image = ""
    text_image += f"{y}, {x}\n"
    colors_table = PALLETS[colors_table]

    if reverse:
        colors_table = colors_table[::-1]

    for iy in range(y):
        for ix in range(x):
            # try, except костыль который мне лень исправлять :)
            try:
                r, g, b = pixels[ix, iy]
            except ValueError:
                r, g, b, a = pixels[ix, iy]
            brightness = (r + g + b) / 3
            if r == max(r, g, b) and r > (g + b) / 1.25:
                r, g, b = 1, 0, 0
            elif g == max(r, g, b) and g > (r + b) / 1.25:
                r, g, b = 0, 1, 0
            elif b == max(r, g, b) and b > (r + g) / 1.25:
                r, g, b = 0, 0, 1
            else:
                r, g, b = 0, 0, 0
            text_image += f"{r}, {g}, {b}, " + get_char(brightness, colors_table) + ";"
        text_image += "\n"

    file = open("output.txt", "w")
    file.write(text_image)
    file.close()


def make_out():
    file = open("output.txt", "r")

    image_info = file.readline()
    image_info = image_info.split(", ")
    y = int(image_info[0])
    x = int(image_info[1])

    image_data = file.readlines()

    for iy in range(y):
        line_data = image_data[iy].split(";")
        for ix in range(x):
            # try, except костыль который мне лень исправлять :)
            try:
                data = line_data[ix].split(", ")
                r = int(data[0])
                g = int(data[1])
                b = int(data[2])
                print((Fore.RED * r) + (Fore.GREEN * g) + (Fore.BLUE * b) + data[3], end="")
            except ValueError:
                continue
        print()


def main():
    while True:
        palette = input(
            "What kind of palette do we use?\n1: 5 levels of gray\n2: 99 levels of gray\n3: ascii\n4: braille\n")
        if palette not in {"1", "2", "3", "4"}:
            continue
        break
    palette = int(palette) - 1
    invert = False
    while True:
        inp = input("Invert black and white?[y/n]\n")
        if inp not in {"y", "n"}:
            continue
        if inp == "y":
            invert = True
        break
    image = input("Name and extension of image what we gonna use:\n")
    image_to_text(palette, image, invert)
    make_out()


if __name__ == '__main__':
    main()
