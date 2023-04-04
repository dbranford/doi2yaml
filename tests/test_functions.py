from doi2yaml import lookup_dois, Result
from doi2yaml.processors import format_date, parse_orcid
from pathlib import Path
import pytest

p = Path("tests/files")


@pytest.mark.crossref_api
def test_lookup_doi():
    results = lookup_dois(
        [
            "10.1103/PhysRevD.65.022002",
            "10.1038/ncomms2067",
            "https://doi.org/10.1088/1367-2630/aa60ee",
            "https://doi.org/10.1103/PhysRevX.10.031023",
        ]
    )

    results_stored = Result.all_from_file(p / "test_all.json")
    results_stored = [r.result for r in results_stored]

    for r in results:
        del r["indexed"]

    for r in results_stored:
        del r["indexed"]

    assert results == results_stored


def test_format_date():
    assert format_date([2022]).startswith("2022")
    assert format_date([2022, 3]).startswith("2022-03")
    assert format_date([2022, 1, 1]) == "2022-01-01"
    assert format_date([2022, 11, 1]) == "2022-11-01"
    assert format_date([2022, 1, 23]) == "2022-01-23"
    assert format_date([2022, 11, 23]) == "2022-11-23"


def test_parse_orcid():
    orcid = r"0000-0001-2345-6789"
    assert parse_orcid(r"0000-0001-2345-6789") == orcid
    assert parse_orcid(r"orcid.org/0000-0001-2345-6789") == orcid
    assert parse_orcid(r"http://orcid.org/0000-0001-2345-6789") == orcid
    assert parse_orcid(r"https://orcid.org/0000-0001-2345-6789") == orcid
