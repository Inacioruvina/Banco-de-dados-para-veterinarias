"""Conexão com PostgreSQL via ODBC."""

import os
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

import pyodbc
from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def _plain_value(name: str, value: str) -> str:
    """Rejeita separadores de parâmetros ODBC."""
    if any(character in value for character in (";", "\r", "\n", "\0")):
        raise ValueError(f"Valor invalido em {name}")
    return value


def get_connection() -> pyodbc.Connection:
    """Retorna uma conexão aberta; o chamador deve fechá-la."""
    load_dotenv(PROJECT_ROOT / ".env")
    required = ("DB_DRIVER", "DB_SERVER", "DB_DATABASE", "DB_USER", "DB_PASSWORD")
    missing = [name for name in required if not os.getenv(name)]
    if missing:
        raise ValueError("Configuracao ausente em .env: " + ", ".join(missing))

    driver = _plain_value("DB_DRIVER", os.environ["DB_DRIVER"])
    if "{" in driver or "}" in driver:
        raise ValueError("Valor invalido em DB_DRIVER")
    server = _plain_value("DB_SERVER", os.environ["DB_SERVER"])
    database = _plain_value("DB_DATABASE", os.environ["DB_DATABASE"])
    user = _plain_value("DB_USER", os.environ["DB_USER"])
    port = os.getenv("DB_PORT", "5432")
    if not port.isascii() or not port.isdecimal() or not 1 <= int(port) <= 65535:
        raise ValueError("DB_PORT deve ser um numero entre 1 e 65535")
    password = os.environ["DB_PASSWORD"]
    if "\0" in password:
        raise ValueError("Valor invalido em DB_PASSWORD")
    escaped_password = password.replace("}", "}}")

    connection_string = (
        f"DRIVER={{{driver}}};SERVER={server};PORT={port};"
        f"DATABASE={database};UID={user};PWD={{{escaped_password}}}"
    )
    return pyodbc.connect(connection_string, timeout=5)


@contextmanager
def managed_connection() -> Iterator[pyodbc.Connection]:
    """Fecha a conexão ao sair do bloco with, inclusive em caso de erro."""
    connection = None
    try:
        connection = get_connection()
        yield connection
    except pyodbc.Error as exc:
        raise ConnectionError("Falha na conexao com o PostgreSQL") from exc
    finally:
        if connection is not None:
            connection.close()
