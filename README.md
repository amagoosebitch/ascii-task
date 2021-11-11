# ASCII-art
Версия 1.0

Авторы: [Лифанов Фёдор](https://github.com/amagoosebitch), [Полуяненко Алёна](https://github.com/NiripsaKakVsegda)

Ревью выполнил: [Александр Анкудинов](https://github.com/xelez)
# Описание
Данный скрипт позволяет преобразовать картинку или видео в ASCII-арт и сохранить результат в ч\б (.txt) или цветном (.html) формате, а так же проиграть видео.
# Требования
* Python 3.8 и выше

* Pillow 8.0 и выше

* opencv-python 4.4 и выше
# Состав
* Скрипт: `ascii_main.py`

* Тесты: `tests.py`

* Необходимые библиотеки: `requirements.txt`

* Картинки/видео для теста: `/files`
# Работа скрипта
```
python ascii-main.py --file [название файла] [аргументы]
```
```
python ascii-main.py -h или python ascii-main/py 
```
```
--help для получения справки об аргументах и возможностях скрипта
```
```
python ascii-main.py --play [директория с ascii-кадрами] для проигрывания ascii-видео
```
