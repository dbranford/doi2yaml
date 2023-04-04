from doi2yaml.result import Result
from doi2yaml.processors import format_date, parse_authors


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
            "page": {
                "key_json": ["article-number"],
                "fallback": {"key_yaml": "page"},
            },
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
