from doi2yaml import Result
from doi2yaml.doi2yaml import format_date, parse_authors
from pathlib import Path

p = Path("tests/files")


def test_result_to_yaml_key():
    r = Result.from_file(p / "test_0.json")

    y = r.to_yaml_key("publisher")
    assert y == "  publisher: American Physical Society (APS)"

    y = r.to_yaml_key("not-publisher", "publisher")
    assert y == "  not-publisher: American Physical Society (APS)"

    y = r.to_yaml_key("not-publisher", ["publisher"])
    assert y == "  not-publisher: American Physical Society (APS)"

    y = r.to_yaml_key("date", ["created", "date-parts"])
    assert y == "  date: [[2002, 7, 27]]"


def test_result_to_yaml_key_missing():
    r = Result.from_file(p / "test_0.json")

    y = r.to_yaml_key("publisher", "not-publisher")
    assert y == ""

    y = r.to_yaml_key("publisher", "not-publisher", default="foo")
    assert y == "  publisher: foo"


def test_result_to_yaml_key_processor():
    r = Result.from_file(p / "test_0.json")

    y = r.to_yaml_key("date", ["published", "date-parts", 0], processor=format_date)
    assert y == "  date: 2001-12-26"

    y = r.to_yaml_key("authors", "author", processor=parse_authors)
    assert (
        y
        == """  authors:
    - name: H. J. Kimble
      orcid: null
    - name: Yuri Levin
      orcid: null
    - name: Andrey B. Matsko
      orcid: null
    - name: Kip S. Thorne
      orcid: null
    - name: Sergey P. Vyatchanin
      orcid: null"""
    )


def test_result_to_yaml_key_fallback():
    r = Result.from_file(p / "test_0.json")

    y = r.to_yaml_key("not-publisher", fallback={"key_yaml": "publisher"})
    assert y == "  publisher: American Physical Society (APS)"

    y = r.to_yaml_key(
        "date",
        ["created", "not-date-parts"],
        fallback={"key_yaml": "date", "key_json": ["created", "date-parts"]},
    )
    assert y == "  date: [[2002, 7, 27]]"
