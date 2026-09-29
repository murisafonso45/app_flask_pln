import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = BASE_DIR / "comentarios.db"


def get_connection():
    """
    Cria uma conexão com o banco SQLite.
    """
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row

    return connection


def init_database():
    """
    Cria a tabela de comentários caso ela ainda não exista.
    """
    connection = get_connection()

    try:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS comentarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                texto TEXT NOT NULL,
                sentimento TEXT NOT NULL,
                score REAL NOT NULL,
                criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        connection.commit()

    finally:
        connection.close()


def salvar_comentario(texto, sentimento, score):
    """
    Salva uma análise no banco de dados.
    """
    connection = get_connection()

    try:
        cursor = connection.execute(
            """
            INSERT INTO comentarios
            (texto, sentimento, score)
            VALUES (?, ?, ?)
            """,
            (texto, sentimento, score)
        )

        connection.commit()

        return cursor.lastrowid

    finally:
        connection.close()


def listar_comentarios(limit=50):
    """
    Retorna os comentários mais recentes.
    """
    connection = get_connection()

    try:
        cursor = connection.execute(
            """
            SELECT
                id,
                texto,
                sentimento,
                score,
                criado_em
            FROM comentarios
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,)
        )

        return cursor.fetchall()

    finally:
        connection.close()
