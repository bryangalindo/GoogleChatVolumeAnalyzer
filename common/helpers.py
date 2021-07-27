from itertools import chain


def string_is_unique(_string, _list):
    if _string in _list:
        return False
    else:
        return True

def create_values_dict(values: list) -> dict:
    return {
        'values': values,
    }

def flatten_list(_list: list) -> list:
    if _list is not None and _list != '':
        if type(_list) == int:
            raise TypeError(1)
        elif len(_list) == 0:
            return 
        else:
            return list(chain.from_iterable(_list))