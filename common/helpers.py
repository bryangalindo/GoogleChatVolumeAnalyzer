from itertools import chain


def create_values_dict(values):
    return {
        'values': values,
    }

def flatten_list(_list):
    return list(chain.from_iterable(_list))