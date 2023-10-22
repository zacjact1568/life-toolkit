from random import sample
from string import ascii_lowercase, digits
from typing import MutableSet


def random_string(length=4, avoid_reduplicate_set: MutableSet = None) -> str:
    """
    随机生成 length 个字符的字符串，只包括小写字母和数字
    """
    def generate():
        return ''.join(sample(ascii_lowercase + digits, length))
    ret = generate()
    if avoid_reduplicate_set is None:
        return ret
    while ret in avoid_reduplicate_set:
        ret = generate()
    avoid_reduplicate_set.add(ret)
    return ret


def split_file_name(name: str) -> tuple[str, str]:
    index = name.rfind('.')
    if index < 0:
        return name, ''
    return name[:index], name[index + 1:]
