import pytest
import ascii_main


def test_wrong_filename():
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        ascii_main.convert_image_to_ASCII('notExistingFile.abc', [10,10], False)
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == -11


def test_wrong_scaling():
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        ascii_main.convert_image_to_ASCII('lovejpg.jpg', [0, -11], False)
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == -12

