from doi2yaml import ResultParser, Result
from pathlib import Path

p = ResultParser()

path = Path("tests/files")


def test_parse0():
    r = Result.from_file(path / "test_0.json")

    s = p.parse_to_yaml(r)

    with open(path / "test_answer_0.yaml") as f:
        a = f.read()

    assert a == s


def test_parse1():
    r = Result.from_file(path / "test_1.json")

    s = p.parse_to_yaml(r)

    with open(path / "test_answer_1.yaml") as f:
        a = f.read()

    assert a == s


def test_parse2():
    r = Result.from_file(path / "test_2.json")

    s = p.parse_to_yaml(r)

    with open(path / "test_answer_2.yaml") as f:
        a = f.read()

    assert a == s


def test_parse3():
    r = Result.from_file(path / "test_3.json")

    s = p.parse_to_yaml(r)

    with open(path / "test_answer_3.yaml") as f:
        a = f.read()

    assert a == s
