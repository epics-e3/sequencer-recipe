from collections.abc import Callable
from time import monotonic, sleep

import pytest

DEFAULT_POLL_INTERVAL_SECONDS = 0.05
DEFAULT_TIMEOUT_SECONDS = 10.0
Predicate = Callable[[], bool]
WaitUntil = Callable[[Predicate, float, float], None]


@pytest.fixture(scope="session")
def wait_until() -> WaitUntil:
    def _wait_until(
        predicate: Predicate,
        timeout: float = DEFAULT_TIMEOUT_SECONDS,
        poll_interval: float = DEFAULT_POLL_INTERVAL_SECONDS,
    ) -> bool:
        deadline = monotonic() + timeout
        while monotonic() < deadline:
            if predicate():
                return True
            sleep(poll_interval)
        raise TimeoutError(
            f"Predicate {predicate} did not become true within {timeout} seconds"
        )

    return _wait_until
