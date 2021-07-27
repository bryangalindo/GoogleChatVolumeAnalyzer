from itertools import chain


def is_nested_list(_list: list) -> bool:
    if _list:
        return any(isinstance(i, list) for i in _list)

def string_is_unique(_string: str, _list: list) -> bool:
    if _string and _list:
        if _string in _list:
            return False
        else:
            return True

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
            
def safeget(_dict, *keys):
    for key in keys:
        try:
            _dict = _dict[key]
        except KeyError:
            return None
    return _dict
        
