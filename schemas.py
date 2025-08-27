PROGRESS_SCHEMA = """
CREATE TABLE IF NOT EXISTS progress (
    id TEXT PRIMARY KEY,
    stage INTEGER NOT NULL DEFAULT 1,
    xp INTEGER NOT NULL DEFAULT 0,
    gold INTEGER NOT NULL DEFAULT 0,
    character TEXT NOT NULL DEFAULT 'Novice Squire',
    inventory TEXT DEFAULT '{}',
    first_time INTEGER DEFAULT 1
)
"""


def create_tables(conn):
    c = conn.cursor()
    c.execute(PROGRESS_SCHEMA)
    conn.commit()
