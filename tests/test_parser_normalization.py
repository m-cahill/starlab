"""M08 parser normalization unit tests (pure, no s2protocol)."""

from __future__ import annotations

import json
from enum import Enum
from typing import Any, cast

import pytest
from starlab.replays.parser_normalization import NormalizationError, normalize_value
from starlab.runs.json_util import canonical_json_dumps, sha256_hex_of_canonical_json


class _Sample(Enum):
    X = 1


def test_normalize_bytes_hex_lowercase() -> None:
    assert normalize_value(b"\xab\xcd") == "abcd"
    assert normalize_value(bytearray(b"\x00\xff")) == "00ff"


def test_normalize_tuple_to_list() -> None:
    assert normalize_value((1, (2, 3))) == [1, [2, 3]]


def test_normalize_dict_sorted_keys() -> None:
    d = {"z": 1, "a": {"m": 2, "b": 3}}
    n = normalize_value(d)
    assert list(n.keys()) == ["a", "z"]
    assert list(n["a"].keys()) == ["b", "m"]


def test_normalize_enum_uses_name() -> None:
    assert normalize_value(_Sample.X) == "X"


def test_reject_non_finite_float() -> None:
    with pytest.raises(NormalizationError, match="non-finite"):
        normalize_value(float("nan"))
    with pytest.raises(NormalizationError, match="non-finite"):
        normalize_value(float("inf"))


def test_reject_unsupported_type() -> None:
    with pytest.raises(NormalizationError, match="unsupported type"):
        normalize_value(cast(Any, object()))


def test_deterministic_json_hash_twice() -> None:
    tree = {"a": [1, 2], "b": b"\x01\x02"}
    n = normalize_value(tree)
    h1 = sha256_hex_of_canonical_json(n)
    h2 = sha256_hex_of_canonical_json(normalize_value(tree))
    assert h1 == h2


def test_json_dumps_roundtrip_no_nan() -> None:
    n = normalize_value({"x": 1.5})
    text = canonical_json_dumps(n)
    json.loads(text[:-1])  # strip newline for loads
