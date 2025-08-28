import json
from typing import Optional
from src.utils.database import get_database


def get_equipped(item_type: Optional[str] = None) -> dict[str, str | None] | str:
    conn = get_database()
    c = conn.cursor()
    c.execute("SELECT equipped FROM progress")
    row = c.fetchone()
    equipped = json.loads(row["equipped"])

    if item_type is None:
        return equipped

    return equipped.get(item_type)
