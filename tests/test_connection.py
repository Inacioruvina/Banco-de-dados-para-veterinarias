import os
import unittest
from unittest.mock import patch

import pyodbc

from src import connection as connection_module

get_connection = connection_module.get_connection


class ConnectionTests(unittest.TestCase):
    def setUp(self):
        self.settings = {
            "DB_DRIVER": "PostgreSQL Unicode(x64)",
            "DB_SERVER": "localhost",
            "DB_PORT": "5432",
            "DB_DATABASE": "VeterinariaDB",
            "DB_USER": "arthur",
            "DB_PASSWORD": "p;ss}word",
        }
        self.dotenv_patch = patch("src.connection.load_dotenv")
        self.dotenv_patch.start()
        self.addCleanup(self.dotenv_patch.stop)

    @patch("src.connection.pyodbc.connect")
    def test_connects_using_environment_and_escapes_password(self, connect):
        with patch.dict(os.environ, self.settings, clear=True):
            result = get_connection()

        self.assertIs(result, connect.return_value)
        connection_string = connect.call_args.args[0]
        self.assertIn("DRIVER={PostgreSQL Unicode(x64)}", connection_string)
        self.assertIn("SERVER=localhost", connection_string)
        self.assertIn("PORT=5432", connection_string)
        self.assertIn("DATABASE=VeterinariaDB", connection_string)
        self.assertIn("UID=arthur", connection_string)
        self.assertIn("PWD={p;ss}}word}", connection_string)
        self.assertEqual(connect.call_args.kwargs["timeout"], 5)

    @patch("src.connection.pyodbc.connect")
    def test_missing_configuration_fails_before_connection(self, connect):
        with patch.dict(os.environ, {**self.settings, "DB_SERVER": ""}, clear=True):
            with self.assertRaisesRegex(ValueError, "DB_SERVER"):
                get_connection()
        connect.assert_not_called()

    @patch("src.connection.pyodbc.connect")
    def test_invalid_port_fails_before_connection(self, connect):
        with patch.dict(os.environ, {**self.settings, "DB_PORT": "invalid"}, clear=True):
            with self.assertRaisesRegex(ValueError, "DB_PORT"):
                get_connection()
        connect.assert_not_called()

    @patch("src.connection.pyodbc.connect")
    def test_separator_in_server_fails_before_connection(self, connect):
        with patch.dict(os.environ, {**self.settings, "DB_SERVER": "localhost;UID=outro"}, clear=True):
            with self.assertRaisesRegex(ValueError, "DB_SERVER"):
                get_connection()
        connect.assert_not_called()

    def test_managed_connection_closes_after_use(self):
        managed_connection = getattr(connection_module, "managed_connection", None)
        self.assertIsNotNone(managed_connection)
        class FakeConnection:
            closed = False

            def close(self):
                self.closed = True

        fake = FakeConnection()
        with patch("src.connection.get_connection", return_value=fake):
            with managed_connection() as connection:
                self.assertIs(connection, fake)
                self.assertFalse(fake.closed)
        self.assertTrue(fake.closed)

    def test_managed_connection_closes_when_use_fails(self):
        managed_connection = getattr(connection_module, "managed_connection", None)
        self.assertIsNotNone(managed_connection)
        class FakeConnection:
            closed = False

            def close(self):
                self.closed = True

        fake = FakeConnection()
        with patch("src.connection.get_connection", return_value=fake):
            with self.assertRaisesRegex(RuntimeError, "falha no uso"):
                with managed_connection():
                    raise RuntimeError("falha no uso")
        self.assertTrue(fake.closed)

    def test_managed_connection_reports_odbc_failure(self):
        managed_connection = getattr(connection_module, "managed_connection", None)
        self.assertIsNotNone(managed_connection)
        with patch("src.connection.get_connection", side_effect=pyodbc.OperationalError("driver ausente")):
            with self.assertRaisesRegex(ConnectionError, "Falha na conexao com o PostgreSQL"):
                with managed_connection():
                    pass


if __name__ == "__main__":
    unittest.main()
