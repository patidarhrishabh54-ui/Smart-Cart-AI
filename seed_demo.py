"""
SmartCart AI - 10,000+ Demo Product Seeder

Save this file as seed_demo.py in the same folder as app.py.
Run:
    .\.venv\Scripts\python.exe seed_demo.py

Creates 10,000 demo products without deleting existing products.
Prices, images, store prices, and history are generated sample data.
"""

import os
import sqlite3
import random
from datetime import datetime, timedelta

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "smartcart.db")

TARGET_DEMO_PRODUCTS = 10000
BATCH_SIZE = 250

random.seed(2026)

CATALOG = {
    "Mobiles": {
        "items": ["Smartphone", "5G Phone", "Android Phone", "Camera Phone"],
        "brands": ["Samsung", "Xiaomi", "OnePlus", "Realme", "Motorola", "Vivo", "Oppo"],
        "low": 6999, "high": 119999, "image_key": "smartphone",
    },
    "Laptops": {
        "items": ["Laptop", "Gaming Laptop", "Ultrabook", "Student Laptop"],
        "brands": ["HP", "Dell", "Lenovo", "Asus", "Acer", "Apple"],
        "low": 24999, "high": 249999, "image_key": "laptop",
    },
    "Audio": {
        "items": ["Wireless Earbuds", "Bluetooth Headphones", "Speaker", "Neckband"],
        "brands": ["Sony", "JBL", "boAt", "Noise", "Sennheiser", "Anker"],
        "low": 599, "high": 39999, "image_key": "headphones",
    },
    "TV & Home": {
        "items": ["Smart TV", "LED TV", "Soundbar", "Streaming Device"],
        "brands": ["Samsung", "LG", "Sony", "TCL", "Xiaomi", "Hisense"],
        "low": 2999, "high": 199999, "image_key": "television",
    },
    "Fashion": {
        "items": ["Sneakers", "Running Shoes", "Backpack", "Jacket", "Watch"],
        "brands": ["Nike", "Adidas", "Puma", "Fossil", "Wildcraft"],
        "low": 499, "high": 29999, "image_key": "sneakers",
    },
    "Home & Kitchen": {
        "items": ["Mixer Grinder", "Air Fryer", "Coffee Maker", "Vacuum Cleaner", "Cookware Set"],
        "brands": ["Philips", "Prestige", "Bajaj", "Havells", "Bosch", "Morphy Richards"],
        "low": 799, "high": 49999, "image_key": "kitchen appliance",
    },
    "Gaming": {
        "items": ["Gaming Controller", "Gaming Mouse", "Gaming Keyboard", "Gaming Headset", "Console Accessory"],
        "brands": ["Logitech", "Razer", "Sony", "Microsoft", "Redragon", "Corsair"],
        "low": 999, "high": 69999, "image_key": "gaming controller",
    },
    "Cameras": {
        "items": ["Digital Camera", "Action Camera", "Camera Lens", "Tripod", "Webcam"],
        "brands": ["Canon", "Nikon", "Sony", "GoPro", "Fujifilm", "DJI"],
        "low": 1499, "high": 299999, "image_key": "camera",
    },
}


def connect_db():
    if not os.path.exists(DB_PATH):
        raise FileNotFoundError(
            f"Database not found: {DB_PATH}\n"
            "Please run app.py once first to create smartcart.db."
        )

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def table_columns(conn, table_name):
    rows = conn.execute(
        f"PRAGMA table_info({table_name})"
    ).fetchall()

    return {row["name"]: row for row in rows}


def ensure_optional_tables(conn):
    conn.execute("""
        CREATE TABLE IF NOT EXISTS product_images (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL,
            image_url TEXT NOT NULL,
            image_order INTEGER NOT NULL DEFAULT 1,
            UNIQUE(product_id, image_order),
            FOREIGN KEY(product_id) REFERENCES products(id)
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS stores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS store_prices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL,
            store_id INTEGER NOT NULL,
            price REAL NOT NULL,
            checked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(product_id) REFERENCES products(id),
            FOREIGN KEY(store_id) REFERENCES stores(id)
        )
    """)

    conn.execute("""
        CREATE INDEX IF NOT EXISTS idx_products_category
        ON products(category)
    """)

    conn.execute("""
        CREATE INDEX IF NOT EXISTS idx_products_price
        ON products(price)
    """)

    conn.execute("""
        CREATE INDEX IF NOT EXISTS idx_product_images_product
        ON product_images(product_id)
    """)

    conn.execute("""
        CREATE INDEX IF NOT EXISTS idx_store_prices_product
        ON store_prices(product_id)
    """)

    for name in ["Demo Store A", "Demo Store B", "Demo Store C"]:
        conn.execute(
            "INSERT OR IGNORE INTO stores(name) VALUES (?)",
            (name,)
        )

    conn.commit()


def value_for_column(col_name, product):
    name = col_name.lower()

    mapping = {
        "name": product["name"],
        "title": product["name"],
        "category": product["category"],
        "brand": product["brand"],
        "price": product["price"],
        "rating": product["rating"],
        "image": product["images"][0],
        "image_url": product["images"][0],
        "description": product["description"],
        "stock": product["stock"],
        "platform": product["platform"],
        "source": product["platform"],
        "url": "",
        "product_url": "",
        "sku": product["sku"],
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

    return mapping.get(name)


def insert_product(conn, columns, product):
    insert_cols = []
    values = []

    for col_name, info in columns.items():
        if col_name == "id" or info["pk"]:
            continue

        value = value_for_column(col_name, product)

        # Handle extra required columns in an existing database.
        if value is None and info["notnull"] and info["dflt_value"] is None:
            low_name = col_name.lower()
            declared_type = (info["type"] or "").upper()

            if any(t in declared_type for t in ["INT", "REAL", "NUM"]):
                value = 0
            elif "price" in low_name:
                value = product["price"]
            elif "image" in low_name or "photo" in low_name:
                value = product["images"][0]
            elif "name" in low_name or "title" in low_name:
                value = product["name"]
            elif "category" in low_name:
                value = product["category"]
            elif "brand" in low_name:
                value = product["brand"]
            elif any(x in low_name for x in ["platform", "store", "source"]):
                value = product["platform"]
            elif "description" in low_name:
                value = product["description"]
            elif "stock" in low_name or "quantity" in low_name:
                value = product["stock"]
            else:
                value = ""

        if value is not None:
            insert_cols.append(col_name)
            values.append(value)

    if not insert_cols:
        raise RuntimeError("Could not determine columns for products table.")

    quoted_cols = ", ".join(
        '"' + c.replace('"', '""') + '"'
        for c in insert_cols
    )

    placeholders = ", ".join(["?"] * len(values))

    sql = f"""
        INSERT INTO products ({quoted_cols})
        VALUES ({placeholders})
    """

    cursor = conn.execute(sql, values)
    return cursor.lastrowid


def main():
    conn = connect_db()

    try:
        columns = table_columns(conn, "products")

        if not columns:
            raise RuntimeError(
                "Table 'products' does not exist. "
                "Run app.py once to initialize the database."
            )

        ensure_optional_tables(conn)

        existing_demo = conn.execute("""
            SELECT COUNT(*)
            FROM products
            WHERE name LIKE '%Demo SKU-%'
        """).fetchone()[0]

        remaining = max(0, TARGET_DEMO_PRODUCTS - existing_demo)

        print(f"Database: {DB_PATH}")
        print(f"Existing demo products: {existing_demo:,}")
        print(f"Products to add: {remaining:,}")

        store_rows = conn.execute("""
            SELECT id, name
            FROM stores
            WHERE name LIKE 'Demo Store %'
            ORDER BY id
        """).fetchall()

        store_ids = [row["id"] for row in store_rows]

        inserted = 0

        for index in range(existing_demo + 1, TARGET_DEMO_PRODUCTS + 1):
            category = random.choice(list(CATALOG.keys()))
            info = CATALOG[category]

            item_type = random.choice(info["items"])
            brand = random.choice(info["brands"])
            sku = f"SKU-{index:05d}"

            # Generated sample price, not a verified market price.
            price = round(
                random.uniform(info["low"], info["high"]), 2
            )

            rating = round(random.uniform(3.2, 5.0), 1)
            stock = random.randint(0, 150)

            keyword = info["image_key"].replace(" ", "%20")

            images = [
                f"https://loremflickr.com/640/480/{keyword}?lock={index * 3 + 1}",
                f"https://loremflickr.com/640/480/{keyword}?lock={index * 3 + 2}",
                f"https://loremflickr.com/640/480/{keyword}?lock={index * 3 + 3}",
            ]

            product = {
                "name": f"{brand} {item_type} {sku} Demo SKU-{index:05d}",
                "category": category,
                "brand": brand,
                "price": price,
                "rating": rating,
                "images": images,
                "description": (
                    f"Demo catalog entry for {brand} {item_type}. "
                    "Generated sample data for testing SmartCart AI."
                ),
                "stock": stock,
                "platform": "SmartCart Demo",
                "sku": sku,
            }

            product_id = insert_product(conn, columns, product)

            # Save all 3 image URLs.
            for image_order, image_url in enumerate(images, start=1):
                conn.execute("""
                    INSERT OR IGNORE INTO product_images
                    (product_id, image_url, image_order)
                    VALUES (?, ?, ?)
                """, (product_id, image_url, image_order))

            # Synthetic price history points.
            conn.execute("""
                INSERT INTO price_history
                (product_id, price, recorded_at)
                VALUES (?, ?, ?)
            """, (
                product_id,
                price,
                (datetime.now() - timedelta(days=30)).strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
            ))

            conn.execute("""
                INSERT INTO price_history
                (product_id, price, recorded_at)
                VALUES (?, ?, ?)
            """, (
                product_id,
                price,
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            ))

            # Sample comparison prices for demo stores.
            for store_id in store_ids:
                store_price = round(
                    price * random.uniform(0.90, 1.12), 2
                )

                conn.execute("""
                    INSERT INTO store_prices
                    (product_id, store_id, price)
                    VALUES (?, ?, ?)
                """, (product_id, store_id, store_price))

            inserted += 1

            if inserted % BATCH_SIZE == 0:
                conn.commit()
                print(f"Added {inserted:,} / {remaining:,}")

        conn.commit()

        total = conn.execute(
            "SELECT COUNT(*) FROM products"
        ).fetchone()[0]

        demo_total = conn.execute("""
            SELECT COUNT(*)
            FROM products
            WHERE name LIKE '%Demo SKU-%'
        """).fetchone()[0]

        print("\nSUCCESS")
        print(f"Demo products now in database: {demo_total:,}")
        print(f"All products including existing products: {total:,}")
        print("Each newly added demo product has 3 image URLs.")
        print(
            "Reminder: generated names, prices, images, store prices, "
            "and history are demo data."
        )

    except Exception as exc:
        conn.rollback()
        print("\nDATABASE ERROR:")
        print(str(exc))
        print("\nPlease send me the full error shown above.")
        raise

    finally:
        conn.close()


if __name__ == "__main__":
    main()