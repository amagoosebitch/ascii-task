import pytest
import ascii_main
from PIL import Image


def test_wrong_filename():
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        args = ascii_main.setup_and_parse(['--file', 'someweird.argument'])
        ascii_main.check_args(args)
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == -11


def test_wrong_scaling():
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        args = ascii_main.setup_and_parse(['--file', 'cat.jpg', '--scale', '-10', '0'])
        ascii_main.check_args(args)
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == -12


def test_correct_arguments():
    args = ascii_main.setup_and_parse(['--file', 'cat.jpg', '--scale', '40', '40', '--morechars', '--out', 'some.txt'])
    try:
        ascii_main.check_args(args)
        exitFlag = False
    except SystemExit:
        exitFlag = True
    assert exitFlag == False


def test_scales_correct():
    args = ascii_main.setup_and_parse(['--file', 'cat.jpg', '--scale', '40', '40', '--morechars', '--out', 'some.txt'])
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
    args = ascii_main.setup_and_parse(['--file', 'cat.jpg', '--scale', '40', '40', '--morechars', '--out', 'some.txt'])
    image = Image.open(args.filename)
    result, resizedImage = ascii_main.convert_image_to_ascii(image, args.scale, args.moreChars)
    for stroke in result:
        for char in stroke:
            assert char in ascii_main.ASCII_CHARS50