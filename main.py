from PIL import Image


PALLETES = [
"█▓▒░ ",
"█▓▒@MBHENR#░KWXDFPQASUZbdehx*8Gm&04LOVYkpq5Tagns69owz$CIu23Jcfry%1v7l+it[] {}?j|()=~!-/<>\"^_';,:`. ",
"$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. ",
"⣿⣾⣼⣸⡇⡅⡆⡂⡄⡁⡀⠀"]


def get_char(brightness, colorstable):
    step = 255 / len(colorstable)
    for i in range(1, len(colorstable) + 1):
        if i * step >= brightness:
            return colorstable[i - 1]


def image_to_text(colorstable, imageName):
    image = Image.open(f"sources/{imageName}")
    pixels = image.load()
    x, y = image.size
    textImage = ""


    for iy in range(y):
        for ix in range(x):
            try:
                r, g, b = pixels[ix, iy]
            except:
                r, g, b, a = pixels[ix, iy]
            brightness = (r + g + b) / 3
            textImage += get_char(brightness, colorstable)
        textImage += "\n"

    file = open("output.txt", "w")
    file.write(textImage)
    file.close()

def text_to_image(colorstable):
    file = open("output.txt", "r")
    lines = file.readlines()

    imageWitdh = len(lines[0]) - 1
    imageHeight = len(lines)

    pixels = []
    for line in range(len(lines)):
        pixels.append([])
        lines[line].replace("\n", "")
        for pixel in lines[line]:
            try:
                pixels[line].append((int(colorstable.index(pixel) * (255 / len(colorstable))),
                                     int(colorstable.index(pixel) * (255 / len(colorstable))),
                                     int(colorstable.index(pixel) * (255 / len(colorstable)))))
            except:
                pass

    print(imageWitdh, imageHeight)
    image = Image.new("RGB", (imageWitdh, imageHeight), (0, 0, 0))
    imagePixels = image.load()
    for y in range(imageHeight):
        for x in range(imageWitdh):
            imagePixels[x, y] = pixels[y][x]
    image.save("text_to_image.png")


while True:
    pallete = input("What kind of palette do we use?\n1: 5 levels of gray\n2: 99 levels of gray\n3: ascii\n4: braille\n")
    if pallete not in {"1", "2", "3", "4"}:
        continue
    break
pallete = PALLETES[int(pallete)-1]
while True:
    inp = input("Invert black and white?[y/n]\n")
    if inp not in {"y", "n"}:
        continue
    if inp == "y":
        pallete = pallete[::-1]
    break
image = input("Name and extension of image what we gonna use:\n")
image_to_text(pallete, image)
text_to_image(pallete)
