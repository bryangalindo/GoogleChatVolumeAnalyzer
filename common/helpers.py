from itertools import chain

from common import constants as c


def create_values_dict(values: list) -> dict:
    return {
        'values': values,
    }

def flatten_list(_list: list) -> list:
    if _list:
        if type(_list) == int:
            raise TypeError(1)
        elif len(_list) == 0:
            return 
        else:
            list_is_nested = is_nested_list(_list)
            if list_is_nested:
                return list(chain.from_iterable(_list))    
            
def get_room_thread_id_dict(_dict: dict) -> dict:
    room_parameters = _dict.get('thread', {}).get('name', '    ').split('/')
    return dict(room_id=room_parameters[c.ROOM_ID_INDEX], thread_id=room_parameters[c.THREAD_ID_INDEX])

def is_nested_list(_list: list) -> bool:
    if _list:
        return any(isinstance(i, list) for i in _list)

def string_is_unique(_string: str, _list: list) -> bool:
    if _string and _list:
        if _string in _list:
            return False
        else:
            return True
   
