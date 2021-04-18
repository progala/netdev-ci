import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parents[1] / "ansible"))
from filter_plugins import build_dev_conns  # noqa: E402


fixt_path = Path(Path(__file__).parent / "fixtures")


@pytest.fixture
def conns_results():
    import json

    with Path(fixt_path / "results" / "vrxconns.json").open() as fin:
        vrxconns = json.load(fin)

    return vrxconns


def test_build_dev_conns(conns_results):
    assert (
        build_dev_conns.build_dev_conns(Path(fixt_path / "host_vars")) == conns_results
    )


# pytest_build_dev_conns()
