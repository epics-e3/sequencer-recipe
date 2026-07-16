import logging
import os
import subprocess
from contextlib import contextmanager
from pathlib import Path

import pytest
from p4p.client.thread import Context
from run_iocsh import IOC, wait_for

LOG = logging.getLogger(__name__)

TEST_DIR = Path(__file__).parent

pytestmark = pytest.mark.skipif(
    not os.environ.get("CONDA_BUILD"),
    reason="Runtime test requires conda-build environment",
)

PV_CONTROL = "TEST:Control"
PV_STATE = "TEST:State"


@pytest.fixture(scope="session")
def sequencer_module():
    r = subprocess.run(
        [
            "make",
            f"CC={os.environ['CC']}",
            f"CCC={os.environ['CXX']}",
            "MODULE=seqtest",
            "LIBVERSION=test",
            "build",
            "install",
        ],
        cwd=TEST_DIR / "sequencer-module",
        capture_output=True,
        text=True,
    )
    LOG.error("make stdout:\n%s", r.stdout)
    LOG.error("make stderr:\n%s", r.stderr)
    r.check_returncode()
    lib = Path(os.environ["PREFIX"]) / "lib" / "libseqtest.so"
    if not lib.exists():
        raise RuntimeError("seqtest module was not installed")


@pytest.fixture
def running_ioc(sequencer_module):
    @contextmanager
    def _run():
        proc = None
        try:
            with IOC((TEST_DIR / "st.cmd").as_posix()) as proc:
                proc.wait_for_output()
                yield proc
        finally:
            if proc is not None:
                LOG.error("IOC stdout:\n%s", proc.stdout)
                LOG.error("IOC stderr:\n%s", proc.stderr)

    return _run


def test_state_machine(running_ioc):
    with running_ioc(), Context("pva") as ctx:
        wait_for(lambda: ctx.get(PV_STATE) == 0)
        ctx.put(PV_CONTROL, 1)
        wait_for(lambda: ctx.get(PV_STATE) == 1)
        ctx.put(PV_CONTROL, 0)
        wait_for(lambda: ctx.get(PV_STATE) == 0)
