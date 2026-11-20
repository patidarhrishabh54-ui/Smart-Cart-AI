import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, "smartcart.db")


def main():
    print("=" * 60)
    print("SMARTCART AI - CATALOGUE SETUP")
    print("=" * 60)

    if not os.path.exists(DATABASE):
        print("ERROR: smartcart.db nahi mili.")
        return

    db = sqlite3.connect(DATABASE)
    db.execute("PRAGMA foreign_keys = ON")

    # =========================================================
    # PRODUCT SPECIFICATIONS
    # =========================================================

    db.execute("""
        CREATE TABLE IF NOT EXISTS product_specs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL,
            spec_name TEXT NOT NULL,
            spec_value TEXT NOT NULL,

            UNIQUE(product_id, spec_name),

            FOREIGN KEY(product_id)
                REFERENCES products(id)
                ON DELETE CASCADE
        )
    """)

    # =========================================================
    # PRODUCT CATEGORY STRUCTURE
    # =========================================================

    db.execute("""
        CREATE TABLE IF NOT EXISTS product_categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            product_id INTEGER NOT NULL,

            main_category TEXT NOT NULL,
            subcategory TEXT,
            segment TEXT,

            UNIQUE(
                product_id,
                main_category,
                subcategory,
                segment
            ),

            FOREIGN KEY(product_id)
                REFERENCES products(id)
                ON DELETE CASCADE
        )
    """)

    # =========================================================
    # PRODUCT ATTRIBUTES
    # Useful for filters such as gender, skin type, etc.
    # =========================================================

    db.execute("""
        CREATE TABLE IF NOT EXISTS product_attributes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            product_id INTEGER NOT NULL,

            attribute_name TEXT NOT NULL,
            attribute_value TEXT NOT NULL,

            UNIQUE(
                product_id,
                attribute_name,
                attribute_value
            ),

            FOREIGN KEY(product_id)
                REFERENCES products(id)
                ON DELETE CASCADE
        )
    """)

    # =========================================================
    # INDEXES
    # =========================================================

    db.execute("""
        CREATE INDEX IF NOT EXISTS
        idx_product_specs_product
        ON product_specs(product_id)
    """)

    db.execute("""
        CREATE INDEX IF NOT EXISTS
        idx_product_specs_name
        ON product_specs(spec_name)
    """)

    db.execute("""
        CREATE INDEX IF NOT EXISTS
        idx_product_categories_product
        ON product_categories(product_id)
    """)

    db.execute("""
        CREATE INDEX IF NOT EXISTS
        idx_product_categories_main
        ON product_categories(main_category)
    """)

    db.execute("""
        CREATE INDEX IF NOT EXISTS
        idx_product_attributes_product
        ON product_attributes(product_id)
    """)

    db.execute("""
        CREATE INDEX IF NOT EXISTS
        idx_product_attributes_name
        ON product_attributes(attribute_name)
    """)

    db.commit()

    # =========================================================
    # SHOW RESULTS
    # =========================================================

    tables = db.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
        ORDER BY name
    """).fetchall()

    print()
    print("Database tables:")
    for table in tables:
        print(" -", table[0])

    product_count = db.execute(
        "SELECT COUNT(*) FROM products"
    ).fetchone()[0]

    spec_count = db.execute(
        "SELECT COUNT(*) FROM product_specs"
    ).fetchone()[0]

    category_count = db.execute(
        "SELECT COUNT(*) FROM product_categories"
    ).fetchone()[0]

    attribute_count = db.execute(
        "SELECT COUNT(*) FROM product_attributes"
    ).fetchone()[0]

    print()
    print("Products           :", product_count)
    print("Specifications     :", spec_count)
    print("Product categories :", category_count)
    print("Product attributes :", attribute_count)

    db.close()

    print()
    print("=" * 60)
    print("CATALOGUE SETUP COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()