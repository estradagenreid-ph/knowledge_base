import sqlite3
from pathlib import Path

DB_PATH = Path("data/knowledge.db")


def get_connection():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row

    return connection


def initialize_database():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS entities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            entity_type TEXT NOT NULL,
            description TEXT,
            UNIQUE(name, entity_type)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source_id INTEGER NOT NULL,
            relationship TEXT NOT NULL,
            target_id INTEGER NOT NULL,
            source_document TEXT,
            FOREIGN KEY(source_id) REFERENCES entities(id),
            FOREIGN KEY(target_id) REFERENCES entities(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT UNIQUE NOT NULL,
            content TEXT
        )
    """)

    connection.commit()
    connection.close()


def add_entity(name, entity_type, description=""):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT OR IGNORE INTO entities
        (name, entity_type, description)
        VALUES (?, ?, ?)
    """, (name, entity_type, description))

    connection.commit()

    cursor.execute("""
        SELECT id FROM entities
        WHERE name = ? AND entity_type = ?
    """, (name, entity_type))

    entity_id = cursor.fetchone()["id"]

    connection.close()

    return entity_id


def add_relationship(
    source_id,
    relationship,
    target_id,
    source_document=""
):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO relationships
        (source_id, relationship, target_id, source_document)
        VALUES (?, ?, ?, ?)
    """, (
        source_id,
        relationship,
        target_id,
        source_document
    ))

    connection.commit()
    connection.close()


def add_document(filename, content):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT OR REPLACE INTO documents
        (filename, content)
        VALUES (?, ?)
    """, (filename, content))

    connection.commit()
    connection.close()


def get_all_entities():
    connection = get_connection()

    rows = connection.execute("""
        SELECT *
        FROM entities
        ORDER BY name
    """).fetchall()

    connection.close()

    return rows


def get_all_relationships():
    connection = get_connection()

    rows = connection.execute("""
        SELECT
            e1.name AS source,
            r.relationship,
            e2.name AS target,
            r.source_document
        FROM relationships r
        JOIN entities e1
            ON r.source_id = e1.id
        JOIN entities e2
            ON r.target_id = e2.id
        ORDER BY e1.name
    """).fetchall()

    connection.close()

    return rows


def search_entities(search_term):
    connection = get_connection()

    rows = connection.execute("""
        SELECT *
        FROM entities
        WHERE name LIKE ?
           OR entity_type LIKE ?
           OR description LIKE ?
        ORDER BY name
    """, (
        f"%{search_term}%",
        f"%{search_term}%",
        f"%{search_term}%"
    )).fetchall()

    connection.close()

    return rows


def get_entity_relationships(entity_name):
    connection = get_connection()

    rows = connection.execute("""
        SELECT
            e1.name AS source,
            r.relationship,
            e2.name AS target,
            r.source_document
        FROM relationships r
        JOIN entities e1
            ON r.source_id = e1.id
        JOIN entities e2
            ON r.target_id = e2.id
        WHERE e1.name LIKE ?
           OR e2.name LIKE ?
    """, (
        f"%{entity_name}%",
        f"%{entity_name}%"
    )).fetchall()

    connection.close()

    return rows