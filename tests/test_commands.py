import pytest
from unittest.mock import patch
from src.commands.commands import COMMAND_REGISTRY


# Mock database connection for commands that use it
class MockCursor:
    def execute(self, *args, **kwargs):
        return self

    def fetchone(self):
        return {"id": "1", "gold": 500}


class MockConn:
    def cursor(self):
        return MockCursor()

    def close(self):
        pass

    def commit(self):
        pass

    row_factory = None


@pytest.fixture(autouse=True)
def mock_init_db():
    with patch("src.commands.commands.init_db", return_value=MockConn()):
        yield


@pytest.mark.parametrize("command_name", list(COMMAND_REGISTRY.keys()))
def test_command_runs(command_name):
    func = COMMAND_REGISTRY[command_name]

    if command_name == "shop buy":
        func(2)
    elif command_name == "exit":
        pass
    else:
        func()
