import re
import logging


def format_date(date: list[int]) -> str:
    date = list(map(str, date))
    while len(date) < 3:
        date.append("00")
    for i in (1, 2):
        if len(date[i]) == 1:
            date[i] = "0" + date[i]
    return "-".join(date)


def parse_authors(authors: list[dict]) -> str:
    authors_list = []
    for i, author in enumerate(authors):
        try:
            name = author["given"] + " " + author["family"]
            try:
                orcid = author["ORCID"]
            except KeyError:
                orcid = "null"
            author_yaml = f"    - name: {name}\n      orcid: {parse_orcid(orcid)}"
            authors_list.append(author_yaml)
        except KeyError:
            logging.warning(f"Author {i+1} missing name part from current entry")
    return "\n" + "\n".join(authors_list)


def parse_orcid(orcid: str) -> str:
    if orcid == "null":
        return orcid
    match = re.fullmatch(r"((https?://)?orcid.org/)?(?P<orcid>[^/]*)/?", orcid)
    if match is None:
        raise ValueError("parse_orcid could not parse a valid ORCID iD")
    else:
        return match.group("orcid")
