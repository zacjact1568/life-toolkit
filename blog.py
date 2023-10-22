import os
from enum import Enum
from typing import Optional

from utils import random_string, split_file_name


class Option(Enum):
    # 同一图片仅由一个文件组成
    NO_REDUPLICATE = 'A'
    # 仅处理 JPG/JPEG
    JPG_ONLY = 'B'
    # 同一图片由多个同名但不同后缀的文件组成
    MULTI_FILES = 'C'
    BACK = '*'


_avoid_reduplicate_set = set()

_rectification_dict = {}


def post_image_name_rectifier() -> bool:
    print('**** Blog post image name rectifier ****')

    path = input('Enter one filesystem directory path that contains image files: \n')
    while path != '*' and not os.access(path, os.F_OK):
        path = input('Directory does not exist, check and enter again: \n')
    if path == '*':
        return False

    option = menu()
    while option is None:
        option = menu()
    if option == Option.BACK:
        return False

    with os.scandir(path) as it:
        for file in it:
            rectify(path, file, option)
    return True


def menu() -> Optional[Option]:
    option = input(
        'Select one option to continue:\n'
        f'[{Option.NO_REDUPLICATE.value}] Single file per image, process any files\n'
        f'[{Option.JPG_ONLY.value}] Single file per image, process JPG/JPEG only\n'
        f'[{Option.MULTI_FILES.value}] Multiple files per image, process any files\n'
        f'[{Option.BACK.value}] Back\n'
    )
    if option == Option.NO_REDUPLICATE.value:
        return Option.NO_REDUPLICATE
    elif option == Option.JPG_ONLY.value:
        return Option.JPG_ONLY
    elif option == Option.MULTI_FILES.value:
        return Option.MULTI_FILES
    elif option == Option.BACK.value:
        return Option.BACK
    else:
        print(f'No option match: {option}')
        return None


def rectify(directory: str, file: os.DirEntry[str], option: Option):
    name = file.name
    if not file.is_file():
        print(f'Skip: {name} (Not a file)')
        return
    if name.startswith('.'):
        print(f'Skip: {name} (Hidden file)')
        return
    name_lower = name.lower()
    if option == Option.JPG_ONLY:
        if not name_lower.endswith('.jpg') and not name_lower.endswith('.jpeg'):
            print(f'Skip: {name} (Ignored image format)')
            return
        ext = 'jpg'
        main_new = random_string(avoid_reduplicate_set=_avoid_reduplicate_set)
    elif option == Option.MULTI_FILES:
        main, ext = split_file_name(name_lower)
        if main in _rectification_dict:
            main_new = _rectification_dict[main]
        else:
            main_new = random_string(avoid_reduplicate_set=_avoid_reduplicate_set)
            _rectification_dict[main] = main_new
    elif option == Option.NO_REDUPLICATE:
        _, ext = split_file_name(name_lower)
        main_new = random_string(avoid_reduplicate_set=_avoid_reduplicate_set)
    else:
        raise ValueError(f'Unexpected option: {option.name}')
    name_new = f'{main_new}.{ext}'
    print(f'Rename: {name} -> {name_new}')
    os.rename(file.path, os.path.join(directory, name_new))
