import argparse
import sys
from PIL import Image
import cv2

ASCII_CHARS50 = "$@AB%8&WM#*oahkbdpqwmzcvunxrjft()1{}[]?-_+~li!';:,. "
ASCII_CHARS10 = "$@%#*+=-:. "

HTML_START = ['<html>', '<head>', '<meta charset="utf-8">', '<style>', 'div {line-height: 1.0;}', '</style>', '</head>',
              '  <body>', '  <div>', '	<p><pre>']
HTML_END = ['</p></pre>', '</div>', '</body>', '</html>']


def get_frame(video_capture, sec, count, colored):
    out_file = 'frames/image' + str(count)
    if colored:
        out_file += '.html'
    else:
        out_file += '.txt'
    video_capture.set(cv2.CAP_PROP_POS_MSEC, sec*1000)
    has_frames, image = video_capture.read()
    if has_frames:
        img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(img)
        result, resizedImage = convert_image_to_ascii(pil_image, (720, 240), True) if not colored else make_colored_image(pil_image, (720, 480), True)
        with open(out_file, 'w') as f:
            f.write('\n'.join(result))
    return has_frames


def video_to_ascii(video_path, frame_rate, colored=False):
    video_capture = cv2.VideoCapture(video_path)
    sec = 0
    count = 1
    success = get_frame(video_capture, sec, count, colored)
    while success:
        count = count + 1
        sec = sec + frame_rate
        sec = round(sec, 2)
        success = get_frame(video_capture, sec, count, colored)
    print('done')


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


def convert_image_to_ascii(image, scaling, moreChars):
    width, height = image.size
    if scaling:
        width, height = scaling
    else:
        height = int(height / 2) + 1
    resizedImage = image.resize((width, height), Image.ANTIALIAS)
    grayImage = to_greyscale(resizedImage)
    asciiString = pixel_to_ascii50(grayImage) if moreChars else pixel_to_ascii10(grayImage)
    length = len(asciiString)
    result = []
    for i in range(0, length, width):
        result.append(asciiString[i:i + width])
    return result, resizedImage


def make_colored_image(image, scaling, moreChars):
    asciiArray, _ = convert_image_to_ascii(image, scaling, moreChars)
    width, height = image.size
    if scaling:
        width, height = scaling
    else:
        height = int(height / 2) + 1
    resizedImage = image.resize((width, height), Image.ANTIALIAS)
    pixels = list(resizedImage.getdata())
    pixels = [pixels[i * width:(i + 1) * width] for i in range(height)]

    result = []
    for i in range(height):
        strokeColors = pixels[i]
        asciiStroke = list(asciiArray[i])
        temp = ''
        for j in range(len(asciiStroke)):
            if asciiStroke[j] == ' ':
                temp += asciiStroke[j]
            else:
                if len(strokeColors[j]) > 3:
                    r, g, b, br = strokeColors[j]
                else:
                    r, g, b = strokeColors[j]
                    br = 1
                temp += f'<span style="color: rgb({r}, {g}, {b}, {br})">' + asciiStroke[j] + '</span>'
        result.append(temp)
    result = HTML_START + result + HTML_END
    return result, resizedImage


def setup_and_parse(input):
    parser = argparse.ArgumentParser(description='Этот скрипт преобразует картинку в ASCII-art')
    parser.add_argument('--file', required=True, dest='filename',
                        help='Укажите полное или относительное имя файла, который хотите преобразовать')
    parser.add_argument('--colored', action='store_true', required=False, dest='isColored',
                        help='Используйте этот аргумент, если хотите получить цветной результат')
    parser.add_argument('--scale', nargs=2, type=int, required=False, metavar=('width', 'height'), default=None,
                        help='Передаётся 2 аргумента: желаемые ширина и высота результата в символах')
    parser.add_argument('--out', required=False, dest='outFile', default='out',
                        help='Укажите имя файла в формате .txt, в котором хотите увидеть результат')
    parser.add_argument('--morechars', action='store_true', required=False, dest='moreChars',
                        help='Используйте этот аргумент, если хотите, чтобы набор символов был разнообразнее')
    args = parser.parse_args(input)
    return args


def check_args(args):
    try:
        Image.open(args.filename)
    except FileNotFoundError:
        print("Файл не найден")
        exit(-11)
    if args.scale:
        if args.scale[0] <= 0 or args.scale[1] <= 0:
            print('Размеры картинок должны быть положительными')
            exit(-12)


def main():
    args = setup_and_parse(sys.argv[1:])
    #args = setup_and_parse(['ascii_main.py', '--file', 'waifu.png', '--scale', '100', '100', '--colored'])
    check_args(args)
    print('Подождите немного, скрипт генерирует арт')
    image = Image.open(args.filename)
    outFile = args.outFile
    if args.isColored:
        result, resizedImage = make_colored_image(image, args.scale, args.moreChars)
        outFile += '.html'
    else:
        result, resizedImage = convert_image_to_ascii(image, args.scale, args.moreChars)
        outFile += '.txt'
    with open(outFile, 'w') as f:
        f.write('\n'.join(result))
    print(f'Результат записан в {outFile}')


if __name__ == '__main__':
    #main()
    video_to_ascii('gravityfalls.mp4', 0.04, True)
