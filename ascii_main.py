import argparse
import sys
import os
from PIL import Image
import cv2
from time import sleep
import time
import platform
#random comment


ASCII_CHARS50 = "$@AB%8&WM#*oahkbdpqwmzcvunxrjft()1{}[]?-_+~li!';:,. "
ASCII_CHARS10 = "$@%#*+=-:. "

HTML_START = ['<html>', '<head>', '<meta charset="utf-8">', '<style>', 'div {line-height: 1.0;}', '</style>', '</head>',
              '  <body>', '  <div>', '	<p><pre>']
HTML_END = ['</p></pre>', '</div>', '</body>', '</html>']


def get_frame(video_capture, sec, count, directory_name, colored, size):
    out_file = '{}/{:05d}'.format(directory_name, count)
    if colored:
        out_file += '.html'
    else:
        out_file += '.txt'
    video_capture.set(cv2.CAP_PROP_POS_MSEC, sec*1000)
    has_frames, image = video_capture.read()
    if has_frames:
        img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(img)
        if size:
            width, height = size
        else:
            width = int(pil_image.width / 1.5) + 1
            height = int(pil_image.height / 3) + 1
        result, resized_image = convert_image_to_ascii(pil_image, (width, height), True) if not colored \
            else make_colored_image(pil_image, (width, height), True)
        with open(out_file, 'w') as f:
            f.write('\n'.join(result))
    return has_frames


def video_to_ascii(video_path, frame_rate, directory_name='frames', colored=False, size=False):
    os.makedirs(directory_name, exist_ok=True)
    video_capture = cv2.VideoCapture(video_path)
    if not frame_rate:
        frame_rate = round(video_capture.get(cv2.CAP_PROP_FPS))
    with open(os.path.join(directory_name, 'frame_rate.md'), 'w') as f:
        f.write(f"{frame_rate}")
    frame_rate = 1 / frame_rate
    sec = 0
    count = 1
    success = get_frame(video_capture, sec, count, directory_name, colored, size)
    while success:
        count = count + 1
        sec = sec + frame_rate
        sec = round(sec, 2)
        success = get_frame(video_capture, sec, count, directory_name, colored, size)


def to_greyscale(image):
    return image.convert("L")


def pixel_to_ascii10(image):
    pixels = image.getdata()
    ascii_string = ""
    for pixel in pixels:
        ascii_string += ASCII_CHARS10[pixel//25]
    return ascii_string


def pixel_to_ascii50(image):
    pixels = image.getdata()
    ascii_string = ""
    for pixel in pixels:
        ascii_string += ASCII_CHARS50[pixel//5]
    return ascii_string


def convert_image_to_ascii(image, scaling, more_chars):
    width, height = image.size
    if scaling:
        width, height = scaling
    else:
        height = int(height / 2) + 1
    resized_image = image.resize((width, height), Image.ANTIALIAS)
    gray_image = to_greyscale(resized_image)
    ascii_string = pixel_to_ascii50(gray_image) if more_chars else pixel_to_ascii10(gray_image)
    length = len(ascii_string)
    result = []
    for i in range(0, length, width):
        result.append(ascii_string[i:i + width])
    return result, resized_image


def make_colored_image(image, scaling, more_chars):
    ascii_array, _ = convert_image_to_ascii(image, scaling, more_chars)
    width, height = image.size
    if scaling:
        width, height = scaling
    else:
        height = int(height / 2) + 1
    resized_image = image.resize((width, height), Image.ANTIALIAS)
    pixels = list(resized_image.getdata())
    pixels = [pixels[i * width:(i + 1) * width] for i in range(height)]

    result = []
    for i in range(height):
        stroke_colors = pixels[i]
        ascii_stroke = list(ascii_array[i])
        temp = ''
        for j in range(len(ascii_stroke)):
            if ascii_stroke[j] == ' ':
                temp += ascii_stroke[j]
            else:
                if len(stroke_colors[j]) > 3:
                    r, g, b, br = stroke_colors[j]
                else:
                    r, g, b = stroke_colors[j]
                    br = 1
                temp += f"<span style=\"color: rgb({r}, {g}, {b}, {br})\">" + ascii_stroke[j] + '</span>'
        result.append(temp)
    result = HTML_START + result + HTML_END
    return result, resized_image


def play_ascii_video(directory):
    files = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.txt')]
    try:
        with open(os.path.join(directory, 'frame_rate.md')) as f:
            frame_rate = 1/(int(f.read()))
    except FileNotFoundError:
        print('Не обнаружен frame_rate.md файл с указанием количества кадров в секунду')
        sys.exit(-18)
    if len(files) == 0:
        print('Не обнаружено .txt файлов для анимации')
        sys.exit(-17)
    for file in files:
        start = time.perf_counter()
        if platform.system() == "Windows":
            os.system("cls")
        else:
            print("\033c", end="")
        with open(file) as f:
            text = f.read()
            print(text)
            remaining_time = frame_rate - (time.perf_counter() - start)
            if remaining_time > 0:
                sleep(remaining_time)


def setup_and_parse(input):
    parser = argparse.ArgumentParser(description='Этот скрипт преобразует картинку в ASCII-art')
    parser.add_argument('--file', required=False, dest='filename',
                        help='Укажите полное или относительное имя файла, который хотите преобразовать')
    parser.add_argument('--colored', action='store_true', required=False, dest='isColored',
                        help='Используйте этот аргумент, если хотите получить цветной результат')
    parser.add_argument('--out', required=False, dest='outFile',
                        help='Укажите имя файла(без расширения) или директорию(для видео), куда сохранить результат')
    parser.add_argument('--morechars', action='store_true', required=False, dest='moreChars',
                        help='Используйте этот аргумент, если хотите, чтобы набор символов был разнообразнее')
    parser.add_argument('--scale', nargs=2, type=int, required=False, metavar=('width', 'height'), default=None,
                        help='Передаётся 2 аргумента: желаемые ширина и высота результата в символах')
    parser.add_argument('--video', action='store_true', required=False, dest='convert_to_video',
                        help='Используйте это аргумент, если хотите преобразовать видео в ASCII-art')
    parser.add_argument('--framerate', type=int, required=False, dest='frame_rate', default=None,
                        help='Используйте этот аргумент, чтобы установить частоту взятия кадра из видео в секундах')
    parser.add_argument('--play', required=False, dest='play_filename',
                        help='Укажите путь до папки, в которой находится преобразованное ascii видео')
    args = parser.parse_args(input)
    return args


def check_args(args):
    if args.play_filename:
        if not os.path.isdir(args.play_filename):
            sys.exit(-11)
        for key, value in args.__dict__.items():
            if value and key != 'play_filename':
                print('play может быть только единственным аргументом')
                sys.exit(-16)
    else:
        try:
            if args.convert_to_video:
                video = cv2.VideoCapture(args.filename)
                if video is None or not video.isOpened():
                    raise FileNotFoundError
            else:
                Image.open(args.filename)
        except FileNotFoundError:
            print("Файл не найден")
            sys.exit(-11)
    if not args.convert_to_video and args.frame_rate:
        print('Частоту взятия кадров можно указывать только для видео')
        sys.exit(-15)
    if args.frame_rate and args.frame_rate <= 0:
        print('Частота взятия кадров должна быть положительной')
        sys.exit(-13)
    if args.scale:
        if args.scale[0] <= 0 or args.scale[1] <= 0:
            print('Размеры должны быть положительными')
            sys.exit(-12)


def main():
    args = setup_and_parse(sys.argv[1:])
    check_args(args)
    print('Подождите немного, скрипт генерирует арт')
    out_file = args.outFile if args.outFile else 'out'
    if args.convert_to_video:
        if not args.outFile: out_file += 'Frames'
        frame_rate = args.frame_rate
        video_to_ascii(args.filename, frame_rate, out_file, args.isColored, args.scale)
        out_file = f'папку {out_file}'
    elif args.play_filename:
        play_ascii_video(args.play_filename)
        input("Нажмите любую клавишу чтобы выйти...")
        sys.exit(0)
    else:
        image = Image.open(args.filename)
        if args.isColored:
            result, resized_image = make_colored_image(image, args.scale, args.moreChars)
            out_file += '.html'
        else:
            result, resized_image = convert_image_to_ascii(image, args.scale, args.moreChars)
            out_file += '.txt'
        with open(out_file, 'w') as f:
            f.write('\n'.join(result))
    print(f'Результат записан в {out_file}')


if __name__ == '__main__':
    main()
