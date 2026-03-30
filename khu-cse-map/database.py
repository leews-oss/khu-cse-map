import sqlite3
import json
import os

DB_PATH = os.environ.get("DATABASE_PATH", "data/curriculum.db")


def get_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    conn = get_db()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS subjects (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            semester TEXT NOT NULL,
            category TEXT NOT NULL,
            credits INTEGER NOT NULL,
            concepts TEXT NOT NULL DEFAULT '[]',
            description TEXT DEFAULT ''
        );
        CREATE TABLE IF NOT EXISTS connections (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            from_id TEXT NOT NULL,
            to_id TEXT NOT NULL,
            type TEXT NOT NULL,
            reason TEXT DEFAULT '',
            shared TEXT DEFAULT '[]',
            FOREIGN KEY (from_id) REFERENCES subjects(id) ON DELETE CASCADE,
            FOREIGN KEY (to_id) REFERENCES subjects(id) ON DELETE CASCADE
        );
    """)
    conn.commit()
    conn.close()


# ── Subjects CRUD ──

def get_all_subjects():
    conn = get_db()
    rows = conn.execute("SELECT * FROM subjects ORDER BY semester, name").fetchall()
    conn.close()
    result = []
    for row in rows:
        d = dict(row)
        d["concepts"] = json.loads(d["concepts"])
        result.append(d)
    return result


def get_subject(subject_id: str):
    conn = get_db()
    row = conn.execute("SELECT * FROM subjects WHERE id = ?", (subject_id,)).fetchone()
    conn.close()
    if row:
        d = dict(row)
        d["concepts"] = json.loads(d["concepts"])
        return d
    return None


def create_subject(data: dict):
    conn = get_db()
    try:
        conn.execute(
            "INSERT INTO subjects (id, name, semester, category, credits, concepts, description) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (data["id"], data["name"], data["semester"], data["category"],
             data["credits"], json.dumps(data["concepts"], ensure_ascii=False), data.get("description", ""))
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()


def update_subject(subject_id: str, data: dict):
    conn = get_db()
    existing = conn.execute("SELECT * FROM subjects WHERE id = ?", (subject_id,)).fetchone()
    if not existing:
        conn.close()
        return False

    fields = []
    values = []
    for key in ["name", "semester", "category", "credits", "description"]:
        if key in data and data[key] is not None:
            fields.append(f"{key} = ?")
            values.append(data[key])
    if "concepts" in data and data["concepts"] is not None:
        fields.append("concepts = ?")
        values.append(json.dumps(data["concepts"], ensure_ascii=False))

    if fields:
        values.append(subject_id)
        conn.execute(f"UPDATE subjects SET {', '.join(fields)} WHERE id = ?", values)
        conn.commit()

    conn.close()
    return True


def delete_subject(subject_id: str):
    conn = get_db()
    existing = conn.execute("SELECT * FROM subjects WHERE id = ?", (subject_id,)).fetchone()
    if not existing:
        conn.close()
        return False
    conn.execute("DELETE FROM connections WHERE from_id = ? OR to_id = ?", (subject_id, subject_id))
    conn.execute("DELETE FROM subjects WHERE id = ?", (subject_id,))
    conn.commit()
    conn.close()
    return True


# ── Connections CRUD ──

def get_all_connections():
    conn = get_db()
    rows = conn.execute("SELECT * FROM connections ORDER BY id").fetchall()
    conn.close()
    result = []
    for row in rows:
        d = dict(row)
        d["shared"] = json.loads(d["shared"])
        # rename from_id/to_id for consistency
        result.append({
            "id": d["id"],
            "from": d["from_id"],
            "to": d["to_id"],
            "type": d["type"],
            "reason": d["reason"],
            "shared": d["shared"],
        })
    return result


def create_connection(data: dict):
    conn = get_db()
    # Verify both subjects exist
    from_exists = conn.execute("SELECT id FROM subjects WHERE id = ?", (data["from_id"],)).fetchone()
    to_exists = conn.execute("SELECT id FROM subjects WHERE id = ?", (data["to_id"],)).fetchone()
    if not from_exists or not to_exists:
        conn.close()
        return None

    cursor = conn.execute(
        "INSERT INTO connections (from_id, to_id, type, reason, shared) VALUES (?, ?, ?, ?, ?)",
        (data["from_id"], data["to_id"], data["type"],
         data.get("reason", ""), json.dumps(data.get("shared", []), ensure_ascii=False))
    )
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return new_id


def update_connection(conn_id: int, data: dict):
    conn = get_db()
    existing = conn.execute("SELECT * FROM connections WHERE id = ?", (conn_id,)).fetchone()
    if not existing:
        conn.close()
        return False

    fields = []
    values = []
    if "from_id" in data and data["from_id"] is not None:
        fields.append("from_id = ?")
        values.append(data["from_id"])
    if "to_id" in data and data["to_id"] is not None:
        fields.append("to_id = ?")
        values.append(data["to_id"])
    if "type" in data and data["type"] is not None:
        fields.append("type = ?")
        values.append(data["type"])
    if "reason" in data and data["reason"] is not None:
        fields.append("reason = ?")
        values.append(data["reason"])
    if "shared" in data and data["shared"] is not None:
        fields.append("shared = ?")
        values.append(json.dumps(data["shared"], ensure_ascii=False))

    if fields:
        values.append(conn_id)
        conn.execute(f"UPDATE connections SET {', '.join(fields)} WHERE id = ?", values)
        conn.commit()

    conn.close()
    return True


def delete_connection(conn_id: int):
    conn = get_db()
    existing = conn.execute("SELECT * FROM connections WHERE id = ?", (conn_id,)).fetchone()
    if not existing:
        conn.close()
        return False
    conn.execute("DELETE FROM connections WHERE id = ?", (conn_id,))
    conn.commit()
    conn.close()
    return True


def is_db_empty():
    conn = get_db()
    count = conn.execute("SELECT COUNT(*) FROM subjects").fetchone()[0]
    conn.close()
    return count == 0
