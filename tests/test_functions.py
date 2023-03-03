from doi2yaml.doi2yaml import format_date, parse_orcid


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
