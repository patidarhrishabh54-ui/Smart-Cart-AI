
import os
import sqlite3
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "smartcart.db")
BACKUP_DIR = os.path.join(BASE_DIR, "backups")

def main():
    if not os.path.isfile(DB_PATH):
        print(f"ERROR: Database nahi mili: {DB_PATH}")
        return

    os.makedirs(BACKUP_DIR, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    sql_path = os.path.join(
        BACKUP_DIR, f"smartcart_backup_{timestamp}.sql"
    )
    db_path = os.path.join(
        BACKUP_DIR, f"smartcart_backup_{timestamp}.db"
    )

    source = sqlite3.connect(DB_PATH, timeout=30)

    try:
        # Verify database integrity before exporting.
        integrity = source.execute("PRAGMA integrity_check").fetchone()[0]
        if integrity != "ok":
            print("ERROR: Database integrity check failed:", integrity)
            print("Original database ko change nahi kiya gaya.")
            return

        # Count products without modifying the source.
        tables = {
            row[0] for row in source.execute(
                "SELECT name FROM sqlite_master WHERE type='table'"
            )
        }

        product_count = None
        if "products" in tables:
            product_count = source.execute(
                "SELECT COUNT(*) FROM products"
            ).fetchone()[0]

        # Consistent SQLite backup, including database tables and data.
        destination = sqlite3.connect(db_path)
        try:
            source.backup(destination)
        finally:
            destination.close()

        # Export schema, data, indexes, triggers and views as SQL.
        with open(sql_path, "w", encoding="utf-8", newline="\n") as file:
            file.write("-- SmartCart AI SQLite database export\n")
            file.write(f"-- Created: {datetime.now().isoformat()}\n")
            file.write("-- Source database is not modified by this export.\n\n")
            for statement in source.iterdump():
                file.write(statement + "\n")

        print("\nBACKUP SUCCESSFUL")
        print("-----------------")
        print("Database integrity:", integrity)
        print("Tables:", len(tables))
        print("Products:", product_count if product_count is not None else "products table not found")
        print("SQL export:", sql_path)
        print("SQLite backup:", db_path)
        print("\nOriginal smartcart.db ko delete ya overwrite nahi kiya gaya.")

    except (sqlite3.Error, OSError) as exc:
        print("Backup error:", exc)

    finally:
        source.close()

if __name__ == "__main__":
    main()
