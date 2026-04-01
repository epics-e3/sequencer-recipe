import logging
import os
import subprocess
from contextlib import contextmanager
from pathlib import Path

import pytest
from p4p.client.thread import Context
from run_iocsh import IOC

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
    if not (Path(os.environ["PREFIX"]) / "lib" / "libseqtest.so").exists():
        raise RuntimeError("seqtest module was not installed")


@pytest.fixture
def running_ioc(sequencer_module, wait_until):
    @contextmanager
    def _run():
        proc = None
        try:
            with IOC((TEST_DIR / "st.cmd").as_posix()) as proc:
                wait_until(proc.is_running)
                yield proc
        finally:
            if proc is not None:
                LOG.error("IOC stdout:\n%s", proc.outs)
                LOG.error("IOC stderr:\n%s", proc.errs)

    return _run


def test_state_machine(running_ioc, wait_until):
    with running_ioc(), Context("pva") as ctx:
        wait_until(lambda: ctx.get(PV_STATE) == 0)
        ctx.put(PV_CONTROL, 1)
        wait_until(lambda: ctx.get(PV_STATE) == 1)
        ctx.put(PV_CONTROL, 0)
        wait_until(lambda: ctx.get(PV_STATE) == 0)
