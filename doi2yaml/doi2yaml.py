import crossref_commons.retrieval
import json
import logging
from collections.abc import Callable
from typing import Self
import re


def lookup_dois(dois: list[str]) -> list[dict]:
    results = []
    for doi in dois:
        lookup = crossref_commons.retrieval.get_publication_as_json(doi)
        results.append(lookup)
    return results


class Result:
    def __init__(self, result: dict):
        self.result = result
        try:
            self.doi = result["DOI"]
        except KeyError:
            logging.error(f"No DOI found for entry {result}")
            raise ValueError("Result parsed appears invalid, no DOI found")

    def to_yaml_key(
        self,
        key_yaml: str,
        key_json: str | list[str] | None = None,
        # default is not run through processor
        # default takes priority over fallback
        default: str | None = None,
        processor: Callable[..., str] | None = None,
        fallback: dict | None = None,
    ) -> str:
        if key_json is None:
            key_json = key_yaml
        if isinstance(key_json, str) is True:
            key_json = [key_json]

        try:
            val = self.result
            for key in key_json:
                val = val[key]
            if processor is not None:
                val = processor(val)
            if val[0] != "\n":
                val = f" {val}"
            return f"  {key_yaml}:{val}"
        except KeyError:
            logging.warning(f"Key {key_json} missing from entry {self.doi}")
        if default is not None:
            val = default
            return f"  {key_yaml}: {val}"
        if fallback is None:
            return ""
        return self.to_yaml_key(**fallback)

    @classmethod
    def from_file(cls, file: str) -> Self:
        with open(file) as f:
            result = json.load(f)
        return cls(result)

    @classmethod
    def all_from_file(cls, file: str) -> list[Self]:
        with open(file) as f:
            results = json.load(f)
        return [cls(r) for r in results]

    def to_file(self, file: str):
        with open(file, "w") as f:
            json.dump(self.result, f)

    @staticmethod
    def all_to_file(file: str, results: list[Self]):
        with open(file, "w") as f:
            json.dump(results, f)

    @classmethod
    def from_dict(cls, d: dict) -> list[Self]:
        return [cls(r) for r in d]


class ResultParser:
    def __init__(self):
        self.yaml_keys = {
            "title": {"key_json": ["title", 0]},
            "journal": {"key_json": ["container-title", 0]},
            "authors": {"key_json": "author", "processor": parse_authors},
            "date": {
                "key_json": ["published", "date-parts", 0],
                "processor": format_date,
            },
            "volume": {},
            "page": {"key_json": ["article-number"], "fallback": {"key_yaml": "page"}},
        }

    def parse_to_yaml(self, result: Result) -> str:
        doi = result.doi
        yaml_args = []
        for k, args in self.yaml_keys.items():
            yaml_args.append(result.to_yaml_key(k, **args))
        yaml_args.append(f"  doi: {doi}")
        yaml = "\n".join(yaml_args)
        yaml = "-" + yaml[1:]
        return yaml


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
