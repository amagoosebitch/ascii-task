import argparse
from PIL import Image

ASCII_CHARS50 = "$@B%8&WM#*oahkbdpqwmzcvunxrjft()1{}[]?-_+~<>li!;:,. "
ASCII_CHARS10 = "$@B%#*+=-:. "


def to_greyscale(image):
    return image.convert("L")


def pixel_to_ascii10(image):
    pixels = image.getdata()
    asciiString = ""
    for pixel in pixels:
        asciiString += ASCII_CHARS10[pixel//25]
    return asciiString


def pixel_to_ascii50(image):
    pixels = image.getdata()
    asciiString = ""
    for pixel in pixels:
        asciiString += ASCII_CHARS50[pixel//5]
    return asciiString


def convert_image_to_ASCII(filename, scale, moreChars):
    image = Image.open(filename)
    width, height = image.size
    if scale:
        width, height = scale
    height = height//2
    resizedImage = image.resize((width, height), Image.ANTIALIAS)
    grayImage = to_greyscale(resizedImage)
    asciiString = pixel_to_ascii50(grayImage) if moreChars else pixel_to_ascii10(grayImage)
    length = len(asciiString)
    result = []
    for i in range(0, length, width):
        result.append(asciiString[i:i + width])
    return result


def main():
    parser = argparse.ArgumentParser(description='Этот скрипт преобразует картинку в ASCII-art')
    parser.add_argument('--file', required=True, dest='filename',
                        help='Укажите полное или относительное имя файла, который хотите преобразовать')
    parser.add_argument('--scale', nargs=2, type=int, required=False, metavar=('width', 'height'), default=None,
                        help='Передаётся 2 аргумента: желаемые ширина и высота результата в символах')
    parser.add_argument('--out', required=False, dest='outFile', default='out.txt',
                        help='Укажите имя файла в формате .txt, в котором хотите увидеть результат')
    parser.add_argument('--morechars', action='store_true', required=False, dest='moreChars',
                        help='Используйте этот аргумент, если хотите, чтобы набор символов был разнообразнее')
    #add_argument('--colored', action='store_true', required=False, dest='isColored',
    #                   help='Используйте этот аргумент, если хотите получить цветной результат')
    args = parser.parse_args()
    filename = args.filename
    scaling = args.scale
    moreChars = args.moreChars
    print('Подождите немного, скрипт генерирует арт')
    result = convert_image_to_ASCII(filename, scaling, moreChars)
    outFile = args.outFile
    with open(outFile, 'w') as f:
        f.write('\n'.join(result))
    print(f'Результат записан в {outFile}')


if __name__ == '__main__':
    main()
