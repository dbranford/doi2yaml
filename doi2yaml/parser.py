from collections.abc import Callable
from doi2yaml.result import Result
from doi2yaml.processors import format_date, parse_authors


class ResultParser:
    def __init__(
        self,
        yaml_keys: dict[str, dict] | None = None,
        processors: dict[str, Callable] | None = None,
    ):
        if yaml_keys is None:
            yaml_keys = {
                "title": {"key_json": ["title", 0]},
                "journal": {"key_json": ["container-title", 0]},
                "authors": {"key_json": "author", "processor": "parse_authors"},
                "date": {
                    "key_json": ["published", "date-parts", 0],
                    "processor": "format_date",
                },
                "volume": {},
                "page": {
                    "key_json": ["article-number"],
                    "fallback": {"key_yaml": "page"},
                },
            }
        if processors is None:
            processors = {
                "parse_authors": parse_authors,
                "format_date": format_date,
            }
        self.yaml_keys = yaml_keys
        self.processor_dict = processors
        self.callable_yaml_keys = None

        self.make_callable_yaml_keys()

    def parse_to_yaml(self, result: Result) -> str:
        doi = result.doi
        yaml_args = []
        for k, args in self.callable_yaml_keys.items():
            yaml_args.append(result.to_yaml_key(k, **args))
        yaml_args.append(f"  doi: {doi}")
        yaml = "\n".join(yaml_args)
        yaml = "-" + yaml[1:]
        return yaml

    def make_callable_yaml_keys(
        self, use_processors: dict[str, Callable] | None = None
    ):
        if use_processors is None:
            use_processors = self.processor_dict

        p = use_processors

        keys = self.yaml_keys.copy()

        for d in keys.values():
            if "processor" in d:
                if isinstance(d["processor"], str):
                    try:
                        d["processor"] = p[d["processor"]]
                    except KeyError:
                        raise ValueError(
                            f"Processor {d['processor']} not found in processor dictionary"
                        )
            while "fallback" in d:
                d = d["fallback"]
                if "processor" in d:
                    if isinstance(d["processor"], str):
                        d["processor"] = p[d["processor"]]

        self.callable_yaml_keys = keys
