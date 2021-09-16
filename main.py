import argparse
from PIL import Image

ASCII_CHARS = ["@", "#", "$", "%", "?", "*", "+", ";", ":", ",", ".", ' ']


def main(first = True,image = None):
    if first:
        path = input("Введите полный путь до картинки\n")
    else:
        path = input('\n')
    try:
        image = Image.open(path)
    except FileNotFoundError:
        print("Путь указан не верно")
        main(False)

    image = resize(image, 50)
    gray_image = to_greyscale(image)
    ascii_str = pixel_to_ascii(gray_image)
    res = []
    img_width = gray_image.width
    ascii_str_len = len(ascii_str)
    for i in range(0, ascii_str_len, img_width):
        res.append(ascii_str[i:i + img_width])
    print('\n'.join(res))

def resize(image, new_width = 100):
    width, height = image.size
    new_height = new_width * int(height / width)
    return image.resize((new_width, new_height))


def to_greyscale(image):
    return image.convert("L")


def pixel_to_ascii(image):
    pixels = image.getdata()
    ascii_str = "";
    for pixel in pixels:
        ascii_str += ASCII_CHARS[pixel//25];
    return ascii_str


if __name__ == '__main__':
    main()