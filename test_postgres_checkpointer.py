import importlib.util
import os
from pathlib import Path
import sys
import types
import unittest
from unittest.mock import patch


MODULE_PATH = Path(__file__).parent / "utils" / "postgres_checkpointer.py"


class FakeConnectionPool:
    instances = []

    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.closed = False
        self.__class__.instances.append(self)

    @staticmethod
    def check_connection(_connection):
        return None

    def close(self):
        self.closed = True


class FakePostgresSaver:
    def __init__(self, pool):
        self.conn = pool
        self.setup_calls = 0

    def setup(self):
        self.setup_calls += 1


def load_subject():
    langgraph_module = types.ModuleType("langgraph")
    checkpoint_module = types.ModuleType("langgraph.checkpoint")
    postgres_module = types.ModuleType("langgraph.checkpoint.postgres")
    postgres_module.PostgresSaver = FakePostgresSaver
    pool_module = types.ModuleType("psycopg_pool")
    pool_module.ConnectionPool = FakeConnectionPool

    fake_modules = {
        "langgraph": langgraph_module,
        "langgraph.checkpoint": checkpoint_module,
        "langgraph.checkpoint.postgres": postgres_module,
        "psycopg_pool": pool_module,
    }
    spec = importlib.util.spec_from_file_location("postgres_checkpointer_subject", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    with patch.dict(sys.modules, fake_modules):
        spec.loader.exec_module(module)
    return module


class SharedPostgresCheckpointerTests(unittest.TestCase):
    def setUp(self):
        FakeConnectionPool.instances.clear()

    def test_reuses_one_validated_pool_with_max_size_40(self):
        module = load_subject()
        env = {
            "POSTGRES_DATABASE_URL": "postgresql://example.invalid/database",
            "SKIP_POSTGRES_SETUP": "true",
        }

        with patch.dict(os.environ, env, clear=False):
            first = module.get_shared_checkpointer()
            second = module.get_shared_checkpointer()

        self.assertIs(first, second)
        self.assertEqual(len(FakeConnectionPool.instances), 1)
        pool = FakeConnectionPool.instances[0]
        self.assertEqual(pool.kwargs["max_size"], 40)
        self.assertIs(pool.kwargs["check"], FakeConnectionPool.check_connection)

    def test_close_releases_pool_and_allows_recreation(self):
        module = load_subject()
        with patch.dict(
            os.environ,
            {"POSTGRES_DATABASE_URL": "postgresql://example.invalid/database"},
            clear=False,
        ):
            first = module.get_shared_checkpointer()
            module.close_shared_postgres_pool()
            second = module.get_shared_checkpointer()

        self.assertTrue(first.conn.closed)
        self.assertIsNot(first, second)
        self.assertEqual(len(FakeConnectionPool.instances), 2)

    def test_setup_runs_only_once_for_the_shared_checkpointer(self):
        module = load_subject()
        env = {
            "POSTGRES_DATABASE_URL": "postgresql://example.invalid/database",
            "SKIP_POSTGRES_SETUP": "false",
        }

        with patch.dict(os.environ, env, clear=False):
            first = module.get_shared_checkpointer()
            second = module.get_shared_checkpointer()

        self.assertIs(first, second)
        self.assertEqual(first.setup_calls, 1)


if __name__ == "__main__":
    unittest.main()
