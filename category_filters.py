import os
import re
import sqlite3
from collections import OrderedDict

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, "smartcart.db")


# ============================================================
# DATABASE CONNECTION AND SCHEMA HELPERS
# ============================================================

def get_db():
    """Open a connection to the existing SmartCart database."""
    if not os.path.exists(DATABASE):
        raise FileNotFoundError(
            f"smartcart.db nahi mili: {DATABASE}"
        )

    conn = sqlite3.connect(DATABASE, timeout=30)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA busy_timeout=10000")
    return conn


def table_exists(conn, table_name):
    row = conn.execute(
        "SELECT 1 FROM sqlite_master WHERE type='table' AND name=?",
        (table_name,)
    ).fetchone()
    return row is not None


def table_columns(conn, table_name):
    if not table_exists(conn, table_name):
        return set()
    # table_name is an internal constant in this module, not user input.
    return {
        row["name"]
        for row in conn.execute(
            f'PRAGMA table_info("{table_name}")'
        ).fetchall()
    }


# ============================================================
# DISPLAY NAME HELPER
# ============================================================

def pretty_name(value):
    """Convert database field names into user-friendly filter labels."""
    if not value:
        return ""

    value = str(value).strip()
    replacements = {
        "ram": "RAM",
        "rom": "ROM",
        "cpu": "Processor",
        "gpu": "Graphics",
        "os": "Operating System",
        "5g": "5G",
        "4g": "4G",
        "ip68": "IP68",
        "ah": "Ah",
        "mah": "mAh",
        "mp": "MP",
        "w": "W",
        "hz": "Hz",
        "spf": "SPF",
        "aha": "AHA",
        "bha": "BHA",
    }

    if value.lower() in replacements:
        return replacements[value.lower()]

    value = value.replace("_", " ")
    value = re.sub(r"\s+", " ", value)
    return value.title()


# ============================================================
# CATEGORY AND SUBCATEGORY LOOKUPS
# ============================================================

def get_categories():
    conn = get_db()
    try:
        if not table_exists(conn, "product_categories"):
            return []

        rows = conn.execute("""
            SELECT DISTINCT main_category
            FROM product_categories
            WHERE main_category IS NOT NULL
              AND TRIM(main_category) != ''
            ORDER BY main_category
        """).fetchall()

        return [row["main_category"] for row in rows]
    finally:
        conn.close()


def get_subcategories(main_category=None):
    conn = get_db()
    try:
        if not table_exists(conn, "product_categories"):
            return []

        if main_category:
            rows = conn.execute("""
                SELECT DISTINCT subcategory
                FROM product_categories
                WHERE main_category = ?
                  AND subcategory IS NOT NULL
                  AND TRIM(subcategory) != ''
                ORDER BY subcategory
            """, (main_category,)).fetchall()
        else:
            rows = conn.execute("""
                SELECT DISTINCT subcategory
                FROM product_categories
                WHERE subcategory IS NOT NULL
                  AND TRIM(subcategory) != ''
                ORDER BY subcategory
            """).fetchall()

        return [row["subcategory"] for row in rows]
    finally:
        conn.close()


# ============================================================
# BRANDS
# ============================================================

def get_brands(main_category=None, subcategory=None):
    conn = get_db()
    try:
        if not table_exists(conn, "products"):
            return []
        if not table_exists(conn, "product_categories"):
            return []

        query = """
            SELECT DISTINCT p.brand
            FROM products p
            INNER JOIN product_categories pc
                ON pc.product_id = p.id
            WHERE p.brand IS NOT NULL
              AND TRIM(p.brand) != ''
        """
        params = []

        if main_category:
            query += " AND pc.main_category = ?"
            params.append(main_category)

        if subcategory:
            query += " AND pc.subcategory = ?"
            params.append(subcategory)

        query += " ORDER BY p.brand"

        rows = conn.execute(query, params).fetchall()
        return [row["brand"] for row in rows]
    finally:
        conn.close()


# ============================================================
# SPECIFICATION NAMES AND VALUES
# ============================================================

def get_spec_names(main_category=None, subcategory=None):
    conn = get_db()
    try:
        if not table_exists(conn, "product_specs"):
            return []
        if not table_exists(conn, "product_categories"):
            return []

        query = """
            SELECT DISTINCT ps.spec_name
            FROM product_specs ps
            INNER JOIN product_categories pc
                ON pc.product_id = ps.product_id
            WHERE ps.spec_name IS NOT NULL
              AND TRIM(ps.spec_name) != ''
        """
        params = []

        if main_category:
            query += " AND pc.main_category = ?"
            params.append(main_category)

        if subcategory:
            query += " AND pc.subcategory = ?"
            params.append(subcategory)

        query += " ORDER BY ps.spec_name"
        rows = conn.execute(query, params).fetchall()
        return [row["spec_name"] for row in rows]
    finally:
        conn.close()


def get_spec_values(spec_name, main_category=None, subcategory=None):
    conn = get_db()
    try:
        if not table_exists(conn, "product_specs"):
            return []
        if not table_exists(conn, "product_categories"):
            return []

        query = """
            SELECT DISTINCT ps.spec_value
            FROM product_specs ps
            INNER JOIN product_categories pc
                ON pc.product_id = ps.product_id
            WHERE ps.spec_name = ?
              AND ps.spec_value IS NOT NULL
              AND TRIM(ps.spec_value) != ''
        """
        params = [spec_name]

        if main_category:
            query += " AND pc.main_category = ?"
            params.append(main_category)

        if subcategory:
            query += " AND pc.subcategory = ?"
            params.append(subcategory)

        query += " ORDER BY ps.spec_value"
        rows = conn.execute(query, params).fetchall()
        return [row["spec_value"] for row in rows]
    finally:
        conn.close()


# ============================================================
# PRICE AND RATING RANGES
# ============================================================

def get_price_range(main_category=None, subcategory=None):
    conn = get_db()
    try:
        if not table_exists(conn, "products"):
            return {"min": 0, "max": 0}
        if not table_exists(conn, "product_categories"):
            return {"min": 0, "max": 0}

        query = """
            SELECT MIN(p.price) AS min_price,
                   MAX(p.price) AS max_price
            FROM products p
            INNER JOIN product_categories pc
                ON pc.product_id = p.id
            WHERE p.price IS NOT NULL
        """
        params = []

        if main_category:
            query += " AND pc.main_category = ?"
            params.append(main_category)

        if subcategory:
            query += " AND pc.subcategory = ?"
            params.append(subcategory)

        row = conn.execute(query, params).fetchone()
        if not row:
            return {"min": 0, "max": 0}

        return {
            "min": row["min_price"] or 0,
            "max": row["max_price"] or 0,
        }
    finally:
        conn.close()


def get_rating_range(main_category=None, subcategory=None):
    conn = get_db()
    try:
        if not table_exists(conn, "products"):
            return {"min": 0, "max": 5}
        if not table_exists(conn, "product_categories"):
            return {"min": 0, "max": 5}

        query = """
            SELECT MIN(p.rating) AS min_rating,
                   MAX(p.rating) AS max_rating
            FROM products p
            INNER JOIN product_categories pc
                ON pc.product_id = p.id
            WHERE p.rating IS NOT NULL
        """
        params = []

        if main_category:
            query += " AND pc.main_category = ?"
            params.append(main_category)

        if subcategory:
            query += " AND pc.subcategory = ?"
            params.append(subcategory)

        row = conn.execute(query, params).fetchone()
        if not row:
            return {"min": 0, "max": 5}

        return {
            "min": row["min_rating"] or 0,
            "max": row["max_rating"] or 5,
        }
    finally:
        conn.close()


# ============================================================
# DYNAMIC FILTER BUILDERS
# ============================================================

def create_spec_filter(spec_name, main_category=None, subcategory=None):
    values = get_spec_values(
        spec_name,
        main_category,
        subcategory
    )
    return {
        "key": spec_name,
        "label": pretty_name(spec_name),
        "type": "checkbox",
        "options": values,
    }


def get_filters(main_category=None, subcategory=None):
    filters = OrderedDict()

    brands = get_brands(main_category, subcategory)
    if brands:
        filters["brand"] = {
            "key": "brand",
            "label": "Brand",
            "type": "checkbox",
            "options": brands,
        }

    price = get_price_range(main_category, subcategory)
    filters["price"] = {
        "key": "price",
        "label": "Price",
        "type": "range",
        "min": price["min"],
        "max": price["max"],
    }

    rating = get_rating_range(main_category, subcategory)
    filters["rating"] = {
        "key": "rating",
        "label": "Rating",
        "type": "rating",
        "min": rating["min"],
        "max": rating["max"],
    }

    filters["stock"] = {
        "key": "stock",
        "label": "Availability",
        "type": "checkbox",
        "options": ["In Stock"],
    }

    for spec_name in get_spec_names(main_category, subcategory):
        spec_filter = create_spec_filter(
            spec_name,
            main_category,
            subcategory
        )
        if spec_filter["options"]:
            filters[spec_name] = spec_filter

    return list(filters.values())


# ============================================================
# COMPLETE CATEGORY INFORMATION
# ============================================================

def get_category_data(main_category=None, subcategory=None):
    return {
        "categories": get_categories(),
        "subcategories": get_subcategories(main_category),
        "brands": get_brands(main_category, subcategory),
        "filters": get_filters(main_category, subcategory),
        "price_range": get_price_range(main_category, subcategory),
        "rating_range": get_rating_range(main_category, subcategory),
    }


# ============================================================
# OPTIONAL COMMAND-LINE FILTER TEST
# ============================================================

def show_demo():
    print()
    print("=" * 70)
    print("SMARTCART AI - DYNAMIC FILTER TEST")
    print("=" * 70)
    print()
    print("Available Categories:")

    for category in get_categories():
        print(" -", category)

    print()
    print("Filters for Electronics / Smartphones:")

    filters = get_filters(
        main_category="Electronics",
        subcategory="Smartphones"
    )

    for filter_item in filters:
        print()
        print(f"[{filter_item['label']}]")

        if filter_item["type"] == "range":
            print(
                "  Range:",
                filter_item.get("min", 0),
                "-",
                filter_item.get("max", 0)
            )
        else:
            options = filter_item.get("options", [])
            for option in options[:15]:
                print("  -", option)
            if len(options) > 15:
                print(f"  ... and {len(options) - 15} more")

    print()
    print("=" * 70)


if __name__ == "__main__":
    if not os.path.exists(DATABASE):
        print("ERROR: smartcart.db nahi mili.")
    else:
        try:
            show_demo()
        except sqlite3.Error as exc:
            print("Database/schema error:", exc)
