import time
from settings import vk_group_id
from typing import Tuple


def create_join_link_and_key(join_prefix: str, room_id: int) -> Tuple[str, str]:
    key = f"{join_prefix}{int(time.time())}{room_id}{len(str(room_id))}"
    vk_link = f'vk.me/-{vk_group_id}?ref={key}'
    return key, vk_link


def parse_key(command: str, join_prefix) -> int:
    ref_code = command.replace(join_prefix, '').strip()
    if not ref_code:
        return 0
    num_len = int(ref_code[-1]) if ref_code[-1].isdigit() else 0
    if not num_len:
        return num_len
    return int(ref_code[-num_len-1:-1]) if ref_code[-num_len-1:-1].isdigit() else 0
