import pytest


def pytest_addoption(parser):
    parser.addoption(
        "--test-crossref-api",
        action="store_true",
        default=False,
        help="Run tests which call the Crossref API",
    )


def pytest_collection_modifyitems(config, items):
    if config.getoption("--test-crossref-api") is False:
        no_crossref = pytest.mark.skip(
            reason="Tests which use the Crossref API are skipped unless the --test-crossref-api option is used"
        )
        for item in items:
            if "crossref_api" in item.keywords:
                item.add_marker(no_crossref)
