import pytest
import ascii_main
from PIL import Image


def pattern_for_exit_tests(args, exitCode):
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        args = ascii_main.setup_and_parse(args)
        ascii_main.check_args(args)
        assert pytest_wrapped_e.type == SystemExit
        assert pytest_wrapped_e.value.code == exitCode


def test_wrong_filename_for_image():
    pattern_for_exit_tests(['--file', 'someweird.argument'], -11)


def test_wrong_filename_for_video():
    pattern_for_exit_tests(['--file', 'someweird.argument', '--video'], -11)


def test_negative_framerate_for_video():
    pattern_for_exit_tests(['--file', 'gravityfalls.mp4', '--video', '--framerate', '-1'], -13)


def test_framerate_for_image():
    pattern_for_exit_tests(['--file', 'lovejpg.jpg', '--framerate', '-1'], -15)


def test_wrong_scaling():
    pattern_for_exit_tests(['--file', 'cat.jpg', '--scale', '-10', '0'], -12)


def test_correct_arguments1():
    args = ascii_main.setup_and_parse(['--file', 'cat.jpg', '--scale', '40', '40', '--morechars', '--out', 'some'])
    try:
        ascii_main.check_args(args)
        exitFlag = False
    except SystemExit:
        exitFlag = True
    assert exitFlag == False


def test_correct_arguments2():
    args = ascii_main.setup_and_parse(
        ['--file', 'gravityfalls.mp4', '--scale', '40', '40', '--morechars', '--video'])
    try:
        ascii_main.check_args(args)
        exitFlag = False
    except SystemExit:
        exitFlag = True
    assert exitFlag == False


def test_scales_correct():
    args = ascii_main.setup_and_parse(['--file', 'cat.jpg', '--scale', '40', '40', '--morechars', '--out', 'some'])
    image = Image.open(args.filename)
    result, resizedImage = ascii_main.convert_image_to_ascii(image, args.scale, args.moreChars)
    assert len(result) == args.scale[1]
    for stroke in result:
        assert len(stroke) == args.scale[0]


def test_to_grayscale_correct():
    image = Image.open('cat.jpg')
    grey_image = ascii_main.to_greyscale(image)
    pixels = grey_image.getdata()
    for pixel in pixels:
        assert 0 <= pixel <= 255


def test_morechars_correct():
    args = ascii_main.setup_and_parse(['--file', 'cat.jpg', '--scale', '40', '40', '--morechars', '--out', 'some'])
    image = Image.open(args.filename)
    result, resizedImage = ascii_main.convert_image_to_ascii(image, args.scale, args.moreChars)
    for stroke in result:
        for char in stroke:
            assert char in ascii_main.ASCII_CHARS50