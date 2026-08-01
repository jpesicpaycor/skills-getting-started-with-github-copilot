import copy

import pytest
from fastapi.testclient import TestClient

from src.app import activities, app


_INITIAL_ACTIVITIES = copy.deepcopy(activities)


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities_state():
    """Reset global in-memory activity data before and after each test."""
    activities.clear()
    activities.update(copy.deepcopy(_INITIAL_ACTIVITIES))

    yield

    activities.clear()
    activities.update(copy.deepcopy(_INITIAL_ACTIVITIES))
