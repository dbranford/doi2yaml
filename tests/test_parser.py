from doi2yaml import ResultParser, Result
from pathlib import Path
import pytest

path = Path("tests/files")


@pytest.fixture
def res_yaml_from_index(request):
    index = request.param
    r = Result.from_file(path / f"test_{index}.json")
    with open(path / f"test_answer_{index}.yaml") as f:
        y = f.read()
    return r, y


@pytest.mark.parametrize("res_yaml_from_index", [0, 1, 2, 3], indirect=True)
def test_parse(res_yaml_from_index):
    r, a = res_yaml_from_index

    p = ResultParser()

    s = p.parse_to_yaml(r)

    assert a == s


def test_parse_change_keys():
    r = Result.from_file(path / "test_0.json")

    p = ResultParser()
    p.yaml_keys = {
        "volume": {},
    }
    y = p.parse_to_yaml(r)

    assert y == "- volume: 65\n  doi: 10.1103/physrevd.65.022002"
