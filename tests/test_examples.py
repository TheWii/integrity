import os

import pytest
from beet import run_beet
from pytest_insta import SnapshotFixture

EXAMPLES = [
    f
    for f in os.listdir("examples")
    if not f.startswith("nosnap_") and not f.startswith(".DS_Store")
]


@pytest.mark.parametrize("directory", EXAMPLES)
def test_build(snapshot: SnapshotFixture, directory: str):
    with run_beet(directory=f"examples/{directory}") as ctx:
        assert snapshot("data_pack") == ctx.data
