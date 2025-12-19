"""
Write function which updates dictionary with defined values but only if new value more then in dict
Restriction: do not use .update() method of dictionary
Examples:
    >>> set_to_dict({'a': 1, 'b': 2, 'c': 3}, a=0, b=4)  # only b updated because new value for a less then original value
    {'a': 1, 'b': 4, 'c': 3}
    >>> set_to_dict({}, a=0)
    {a: 0}
    >>> set_to_dict({'a': 5})
    {'a': 5}
"""
from typing import Dict


def set_to_dict(dict_to_update: Dict[str, int], **items_to_set) -> Dict:
    for i in items_to_set:
        if i not in dict_to_update or items_to_set[i] > dict_to_update[i]:
            dict_to_update[i] = items_to_set[i]
    return dict_to_update

if __name__ == '__main__':
    print(set_to_dict({'a': 1, 'b': 2, 'c': 3}, a=0, b=4))
    print(set_to_dict({}, a=0))
    print(set_to_dict({'a': 5}))