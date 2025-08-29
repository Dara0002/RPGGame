import pytest
import json
from unittest.mock import patch
from src.commands.commands import COMMAND_REGISTRY


class MockCursor:
    def execute(self, *args, **kwargs):
        return self

    def fetchone(self):
        return {
            "gold": 500,
            "inventory": json.dumps([]),
            "equipped": json.dumps({"armor": None, "weapon": None}),
        }

    def fetchall(self):
        return [self.fetchone()]


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

    modules_to_patch = [
        "src.commands.commands.get_database",
        "src.utils.get_equipped.get_database",
    ]

    patches = [patch(m, return_value=MockConn()) for m in modules_to_patch]
    for p in patches:
        p.start()
    yield

    for p in patches:
        p.stop()


@pytest.mark.parametrize("command_name", list(COMMAND_REGISTRY.keys()))
def test_command_runs(command_name):
    func = COMMAND_REGISTRY[command_name]

    if command_name == "shop buy":
        func(2)
    elif command_name == "equip":
        func("iron sword")
    elif command_name == "item":
        func("iron sword")
    elif command_name == "unequip":
        func("iron sword")
    elif command_name == "exit":
        pass
    else:
        func()
