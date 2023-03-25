import argparse
import doi2yaml

arg_parser = argparse.ArgumentParser()

arg_parser.add_argument("DOIs", nargs="*")
arg_parser.add_argument(
    "-i", "--input-file", help="Use JSON stored in file rather than the Crossref API"
)
arg_parser.add_argument("-o", "--output-file")
arg_parser.add_argument(
    "--fetch",
    action="store_true",
    help="Lookup the DOI without parsing the resulting JSON",
)


def run(args=None):
    if args is None:
        args = arg_parser.parse_args()
    dois = args["DOIs"]

    if args["input_file"] is None:
        results = doi2yaml.lookup_dois(dois)
    else:
        results = doi2yaml.Result.all_from_file(args["input_file"])

    results = [doi2yaml.Result(r) for r in results]

    if args["fetch"] is True:
        output = [r.result for r in results]
    else:
        parser = doi2yaml.ResultParser()

        yaml = [parser.parse_to_yaml(r) for r in results]
        yaml = "\n".join(yaml)

        output = yaml

    if args["output_file"] is None:
        print(output)
    else:
        if args["fetch"] is True:
            doi2yaml.Result.all_to_file(args["output_file"], output)
        elif args["fetch"] is False:
            with open(args["output_file"], "w") as f:
                f.write(output)
