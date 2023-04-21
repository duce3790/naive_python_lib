from collections.abc import Mapping, MutableMapping, Sequence
from typing import Callable, Generator


def get_mapping_values_by_key_order(d: Mapping) -> Generator:
    r"""
    Return a generator giving the values by key order.
    """
    for k in sorted(d.keys()):
        yield d[k]


def change_mapping_keys(
    d: MutableMapping, f: Callable, recursive: bool = False
) -> MutableMapping:
    r"""
    Return a new mapping with keys changed
    """
    new_d = type(d)()
    for k, v in d.items():
        if recursive and isinstance(v, MutableMapping):
            v = change_mapping_keys(v, f, recursive)
        new_k = f(k)
        assert new_k not in new_d
        new_d[new_k] = v
    return new_d


def flatten_mapping(d: Mapping) -> list:
    r"""
    Return a list with values ordered by keys and flatten it
    """

    res = []
    for v in get_mapping_values_by_key_order(d):
        if isinstance(v, Mapping):
            res += flatten_mapping(v)
        else:
            res.append(v)
    return res


def reduce_values_by_key(f: Callable, maps: Sequence[dict]) -> dict:
    value_seq_dict: dict = {k: [] for k in maps[0]}
    for m in maps:
        for k, v in m.items():
            value_seq_dict[k].append(v)
    return {k: f(v) for k, v in value_seq_dict.items()}
