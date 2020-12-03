from typing import List


def text_cutter(text: str, text_size: int) -> List[str]:
    return [text[x:x + text_size] for x in range(0, len(text), text_size)]
