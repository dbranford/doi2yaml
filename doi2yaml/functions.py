import crossref_commons.retrieval


def lookup_dois(dois: list[str]) -> list[dict]:
    results = []
    for doi in dois:
        lookup = crossref_commons.retrieval.get_publication_as_json(doi)
        results.append(lookup)
    return results
