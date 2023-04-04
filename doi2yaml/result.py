import json
import logging
from collections.abc import Callable
from typing import Self


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
