import argparse
import doi2yaml

arg_parser = argparse.ArgumentParser()

arg_parser.add_argument("DOIs", nargs="*")


def run(args=None):
    if args is None:
        args = arg_parser.parse_args()
    dois = args["DOIs"]

    results = doi2yaml.lookup_dois(dois)

    results = [doi2yaml.Result(r) for r in results]

    parser = doi2yaml.ResultParser()

    yaml = [parser.parse_to_yaml(r) for r in results]
    yaml = "\n".join(yaml)

    print(yaml)
