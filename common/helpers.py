from itertools import chain


def create_values_dict(values: list) -> dict:
    return {
        'values': values,
    }

def flatten_list(_list: list) -> list:
    if _list is not None and _list != '':
        if type(_list) == int:
            raise TypeError(1)
        else:
            return list(chain.from_iterable(_list))