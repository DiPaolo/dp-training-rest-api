import logging
import os
import pickle
from typing import Optional, Dict, List
from uuid import UUID

from web_server import domain

_PICKLE_CACHE_FILENAME = 'todo_item_list.dat'


def add_todo_item(item: domain.TodoItem) -> domain.TodoItem:
    data = get_repo()
    data.append(item.to_dict())
    update_repo(data)
    return item


def get_todo_items() -> List[domain.TodoItem]:
    return [domain.TodoItem.from_dict(i) for i in get_repo()]


def get_item_by_id(item_id: UUID) -> Optional[domain.TodoItem]:
    if not item_id:
        return None

    data = get_repo()
    try:
        found_item = next(filter(lambda i: i['id'] == item_id, data))
        return domain.TodoItem.from_dict(found_item)
    except:
        return None


def update_todo_item(item_id: UUID, item_in: domain.TodoItem) -> Optional[domain.TodoItem]:
    if not item_id:
        return None

    data = get_repo()
    try:
        for item in data:
            if item['id'] == item_id:
                for k, v in item_in.to_dict().items():
                    if k.lower() == 'id':
                        continue

                    if v is not None:
                        item[k] = v

                update_repo(data)
                return domain.TodoItem.from_dict(item)
    except:
        return None

    return None


def delete_item(item_id: UUID) -> Optional[domain.TodoItem]:
    if not item_id:
        return None

    data = get_repo()
    try:
        for item in data:
            if item['id'] == item_id:
                data.remove(item)
                update_repo(data)
                return domain.TodoItem.from_dict(item)
    except:
        return None

    return None


def get_repo(remove_from_cache: bool = False) -> Optional[List[Dict]]:
    data = _read_cache()
    if data is None:
        data = list()
    return data


def update_repo(data: List[Dict]):
    # cache = _read_cache()
    # if cache is None:
    #     cache = list()
    #
    _write_cache(data)


def _read_cache() -> Optional[List[Dict]]:
    if not os.path.exists(_PICKLE_CACHE_FILENAME):
        return None

    with open(_PICKLE_CACHE_FILENAME, 'rb') as f_read:
        try:
            return pickle.load(f_read)
        except Exception as e:
            logging.error(e)
            return None


def _write_cache(data: List[Dict]):
    with open(_PICKLE_CACHE_FILENAME, 'wb') as f_write:
        pickle.dump(data, f_write)
