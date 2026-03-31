"""
Database setup script for the Impact project.
- Creates impact.db with needs and volunteers tables.
- Inserts initial data for testing.
- Provides helper functions for the Flask application.
"""

import sqlite3
import csv

DB_PATH = "impact.db"

# ─────────────────────────────────────────────────────────────────────────────
# 1.  CONNECTION HELPER
# ─────────────────────────────────────────────────────────────────────────────

def get_db():
    """Return a connection to impact.db with row access by name."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# ─────────────────────────────────────────────────────────────────────────────
# 2.  CREATE TABLES
# ─────────────────────────────────────────────────────────────────────────────

def create_tables():
    conn = get_db()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS needs (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            area     TEXT    NOT NULL,
            category TEXT    NOT NULL,
            urgency  INTEGER NOT NULL    -- 1 = low, 5 = critical
        );

        CREATE TABLE IF NOT EXISTS volunteers (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            name         TEXT    NOT NULL,
            skill        TEXT    NOT NULL,
            location     TEXT    NOT NULL,
            availability INTEGER NOT NULL   -- hours available per week
        );
    """)
    conn.commit()
    conn.close()
    print("Tables initialized.")

# ─────────────────────────────────────────────────────────────────────────────
# 3.  INSERT DATA
# ─────────────────────────────────────────────────────────────────────────────

def insert_sample_data():
    needs_rows = [
        ("Chennai North",  "Food Supply",      5),
        ("Chennai South",  "Medical Aid",      4),
        ("Chennai West",   "Shelter",          5),
        ("Tambaram",       "Education",        2),
        ("Velachery",      "Clean Water",      3),
    ]

    volunteers_rows = [
        ("Srividhya",  "Database",      "Chennai North",   10),
        ("Suresh K",    "Backend",       "Chennai South",   12),
        ("Ravi Kumar",  "First Aid",     "Chennai West",     8),
        ("Meena S",     "Teaching",      "Tambaram",         6),
        ("Arjun R",     "Logistics",     "Velachery",       15),
    ]

    conn = get_db()
    cur  = conn.cursor()

    if cur.execute("SELECT COUNT(*) FROM needs").fetchone()[0] == 0:
        cur.executemany(
            "INSERT INTO needs (area, category, urgency) VALUES (?,?,?)",
            needs_rows
        )
        print("Initial needs data loaded.")

    if cur.execute("SELECT COUNT(*) FROM volunteers").fetchone()[0] == 0:
        cur.executemany(
            "INSERT INTO volunteers (name, skill, location, availability) VALUES (?,?,?,?)",
            volunteers_rows
        )
        print("Initial volunteer data loaded.")

    conn.commit()
    conn.close()

# ─────────────────────────────────────────────────────────────────────────────
# 4.  DATA RETRIEVAL FUNCTIONS
# ─────────────────────────────────────────────────────────────────────────────

def get_needs_sorted_by_urgency():
    conn = get_db()
    rows = conn.execute(
        "SELECT * FROM needs ORDER BY urgency DESC"
    ).fetchall()
    conn.close()
    return rows

def get_all_volunteers():
    conn = get_db()
    rows = conn.execute("SELECT * FROM volunteers").fetchall()
    conn.close()
    return rows

def match_volunteers_to_need(need_id):
    """Finds volunteers in the same area as the specified need."""
    conn = get_db()
    need = conn.execute(
        "SELECT * FROM needs WHERE id = ?", (need_id,)
    ).fetchone()

    if not need:
        conn.close()
        return []

    matched = conn.execute(
        "SELECT * FROM volunteers WHERE location = ?", (need["area"],)
    ).fetchall()
    conn.close()
    return matched

# ─────────────────────────────────────────────────────────────────────────────
# 5.  EXPORT UTILITY
# ─────────────────────────────────────────────────────────────────────────────

def export_needs_csv(filename="urgent_needs.csv"):
    rows = get_needs_sorted_by_urgency()
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "area", "category", "urgency"])
        for row in rows:
            writer.writerow([row["id"], row["area"], row["category"], row["urgency"]])
    print(f"Exported data to {filename}")

# ─────────────────────────────────────────────────────────────────────────────
# 6.  EXECUTION
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    create_tables()
    insert_sample_data()

    print("\n--- Current Needs ---")
    for row in get_needs_sorted_by_urgency():
        print(f"[{row['urgency']} / 5] {row['area']} - {row['category']}")

    print("\n--- Matching for Need #1 ---")
    for v in match_volunteers_to_need(1):
        print(f"Volunteer: {v['name']} ({v['skill']})")

    export_needs_csv()