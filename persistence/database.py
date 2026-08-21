import sqlite3
import os

DEFAULT_DB_PATH = "saves/tower_of_lucas.db"


def _ensure_dir(db_path: str) -> None:
    dirname = os.path.dirname(db_path)
    if dirname:
        os.makedirs(dirname, exist_ok=True)


def get_connection(db_path: str = DEFAULT_DB_PATH) -> sqlite3.Connection:
    _ensure_dir(db_path)
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.row_factory = sqlite3.Row
    return conn


def init_db(db_path: str = DEFAULT_DB_PATH) -> None:
    conn = get_connection(db_path)
    with conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS characters (
                name TEXT PRIMARY KEY,
                class_name TEXT NOT NULL,
                race_name TEXT NOT NULL,
                hp INTEGER NOT NULL,
                max_hp INTEGER NOT NULL,
                atk INTEGER NOT NULL,
                defense INTEGER NOT NULL,
                speed INTEGER NOT NULL,
                mana INTEGER NOT NULL,
                max_mana INTEGER NOT NULL,
                gold INTEGER NOT NULL DEFAULT 0,
                exp INTEGER NOT NULL DEFAULT 0,
                level INTEGER NOT NULL DEFAULT 1,
                current_floor INTEGER NOT NULL DEFAULT 1,
                skill_cooldowns TEXT NOT NULL DEFAULT '{}',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS inventory_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                character_name TEXT NOT NULL,
                name TEXT NOT NULL,
                slot TEXT NOT NULL,
                rarity TEXT NOT NULL,
                hp_bonus INTEGER NOT NULL DEFAULT 0,
                atk_bonus INTEGER NOT NULL DEFAULT 0,
                defense_bonus INTEGER NOT NULL DEFAULT 0,
                speed_bonus INTEGER NOT NULL DEFAULT 0,
                mana_bonus INTEGER NOT NULL DEFAULT 0,
                upgrade_level INTEGER NOT NULL DEFAULT 0,
                description TEXT NOT NULL DEFAULT '',
                sprite TEXT NOT NULL DEFAULT '',
                FOREIGN KEY (character_name) REFERENCES characters(name) ON DELETE CASCADE
            );
        """)
    conn.close()
