import sqlite3
import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, "smartcart.db")


# ============================================================
# SMARTPHONE CATALOGUE
# ============================================================

PRODUCTS = [

    # --------------------------------------------------------
    # APPLE
    # --------------------------------------------------------

    {
        "name": "Apple iPhone 15 128GB",
        "brand": "Apple",
        "category": "Electronics",
        "subcategory": "Smartphones",
        "segment": "Premium Smartphone",
        "price": 69999,
        "mrp": 79900,
        "rating": 4.5,
        "reviews": 12500,
        "description": "Apple iPhone 15 with 128GB storage and A16 Bionic chip.",
        "specs": {
            "Model": "iPhone 15",
            "Variant": "128GB",
            "RAM": "6GB",
            "Storage": "128GB",
            "Processor": "Apple A16 Bionic",
            "Display": "6.1 inch Super Retina XDR OLED",
            "Refresh Rate": "60Hz",
            "Rear Camera": "48MP + 12MP",
            "Front Camera": "12MP",
            "Battery": "3349mAh",
            "5G": "Yes",
            "OS": "iOS",
            "Charging": "USB-C",
            "Water Resistance": "IP68",
        },
    },

    {
        "name": "Apple iPhone 15 256GB",
        "brand": "Apple",
        "category": "Electronics",
        "subcategory": "Smartphones",
        "segment": "Premium Smartphone",
        "price": 79999,
        "mrp": 89900,
        "rating": 4.5,
        "reviews": 9800,
        "description": "Apple iPhone 15 with 256GB storage.",
        "specs": {
            "Model": "iPhone 15",
            "Variant": "256GB",
            "RAM": "6GB",
            "Storage": "256GB",
            "Processor": "Apple A16 Bionic",
            "Display": "6.1 inch Super Retina XDR OLED",
            "Refresh Rate": "60Hz",
            "Rear Camera": "48MP + 12MP",
            "Front Camera": "12MP",
            "Battery": "3349mAh",
            "5G": "Yes",
            "OS": "iOS",
            "Charging": "USB-C",
            "Water Resistance": "IP68",
        },
    },

    {
        "name": "Apple iPhone 15 Pro 128GB",
        "brand": "Apple",
        "category": "Electronics",
        "subcategory": "Smartphones",
        "segment": "Premium Smartphone",
        "price": 99999,
        "mrp": 109900,
        "rating": 4.6,
        "reviews": 8500,
        "description": "Apple iPhone 15 Pro with A17 Pro processor.",
        "specs": {
            "Model": "iPhone 15 Pro",
            "Variant": "128GB",
            "RAM": "8GB",
            "Storage": "128GB",
            "Processor": "Apple A17 Pro",
            "Display": "6.1 inch Super Retina XDR OLED",
            "Refresh Rate": "120Hz",
            "Rear Camera": "48MP + 12MP + 12MP",
            "Front Camera": "12MP",
            "Battery": "3274mAh",
            "5G": "Yes",
            "OS": "iOS",
            "Charging": "USB-C",
            "Water Resistance": "IP68",
        },
    },

    {
        "name": "Apple iPhone 15 Pro Max 256GB",
        "brand": "Apple",
        "category": "Electronics",
        "subcategory": "Smartphones",
        "segment": "Premium Smartphone",
        "price": 119999,
        "mrp": 134900,
        "rating": 4.7,
        "reviews": 9200,
        "description": "Apple iPhone 15 Pro Max with 256GB storage.",
        "specs": {
            "Model": "iPhone 15 Pro Max",
            "Variant": "256GB",
            "RAM": "8GB",
            "Storage": "256GB",
            "Processor": "Apple A17 Pro",
            "Display": "6.7 inch Super Retina XDR OLED",
            "Refresh Rate": "120Hz",
            "Rear Camera": "48MP + 12MP + 12MP",
            "Front Camera": "12MP",
            "Battery": "4441mAh",
            "5G": "Yes",
            "OS": "iOS",
            "Charging": "USB-C",
            "Water Resistance": "IP68",
        },
    },

    {
        "name": "Apple iPhone 16 128GB",
        "brand": "Apple",
        "category": "Electronics",
        "subcategory": "Smartphones",
        "segment": "Premium Smartphone",
        "price": 79999,
        "mrp": 79900,
        "rating": 4.6,
        "reviews": 7200,
        "description": "Apple iPhone 16 with A18 chip and 128GB storage.",
        "specs": {
            "Model": "iPhone 16",
            "Variant": "128GB",
            "RAM": "8GB",
            "Storage": "128GB",
            "Processor": "Apple A18",
            "Display": "6.1 inch Super Retina XDR OLED",
            "Refresh Rate": "60Hz",
            "Rear Camera": "48MP + 12MP",
            "Front Camera": "12MP",
            "Battery": "3561mAh",
            "5G": "Yes",
            "OS": "iOS",
            "Charging": "USB-C",
            "Water Resistance": "IP68",
        },
    },

    {
        "name": "Apple iPhone 16 Pro 128GB",
        "brand": "Apple",
        "category": "Electronics",
        "subcategory": "Smartphones",
        "segment": "Premium Smartphone",
        "price": 119999,
        "mrp": 119900,
        "rating": 4.7,
        "reviews": 6100,
        "description": "Apple iPhone 16 Pro with A18 Pro processor.",
        "specs": {
            "Model": "iPhone 16 Pro",
            "Variant": "128GB",
            "RAM": "8GB",
            "Storage": "128GB",
            "Processor": "Apple A18 Pro",
            "Display": "6.3 inch Super Retina XDR OLED",
            "Refresh Rate": "120Hz",
            "Rear Camera": "48MP + 48MP + 12MP",
            "Front Camera": "12MP",
            "Battery": "3582mAh",
            "5G": "Yes",
            "OS": "iOS",
            "Charging": "USB-C",
            "Water Resistance": "IP68",
        },
    },

    {
        "name": "Apple iPhone 16 Pro Max 256GB",
        "brand": "Apple",
        "category": "Electronics",
        "subcategory": "Smartphones",
        "segment": "Premium Smartphone",
        "price": 144999,
        "mrp": 144900,
        "rating": 4.7,
        "reviews": 6800,
        "description": "Apple iPhone 16 Pro Max with 256GB storage.",
        "specs": {
            "Model": "iPhone 16 Pro Max",
            "Variant": "256GB",
            "RAM": "8GB",
            "Storage": "256GB",
            "Processor": "Apple A18 Pro",
            "Display": "6.9 inch Super Retina XDR OLED",
            "Refresh Rate": "120Hz",
            "Rear Camera": "48MP + 48MP + 12MP",
            "Front Camera": "12MP",
            "Battery": "4685mAh",
            "5G": "Yes",
            "OS": "iOS",
            "Charging": "USB-C",
            "Water Resistance": "IP68",
        },
    },

    # --------------------------------------------------------
    # SAMSUNG
    # --------------------------------------------------------

    {
        "name": "Samsung Galaxy S24 256GB",
        "brand": "Samsung",
        "category": "Electronics",
        "subcategory": "Smartphones",
        "segment": "Premium Smartphone",
        "price": 74999,
        "mrp": 79999,
        "rating": 4.5,
        "reviews": 11000,
        "description": "Samsung Galaxy S24 with 256GB storage.",
        "specs": {
            "Model": "Galaxy S24",
            "Variant": "256GB",
            "RAM": "8GB",
            "Storage": "256GB",
            "Processor": "Snapdragon 8 Gen 3",
            "Display": "6.2 inch Dynamic AMOLED 2X",
            "Refresh Rate": "120Hz",
            "Rear Camera": "50MP + 10MP + 12MP",
            "Front Camera": "12MP",
            "Battery": "4000mAh",
            "5G": "Yes",
            "OS": "Android",
            "Charging": "25W",
            "Water Resistance": "IP68",
        },
    },

    {
        "name": "Samsung Galaxy S24 Ultra 256GB",
        "brand": "Samsung",
        "category": "Electronics",
        "subcategory": "Smartphones",
        "segment": "Ultra Premium Smartphone",
        "price": 129999,
        "mrp": 134999,
        "rating": 4.7,
        "reviews": 15000,
        "description": "Samsung Galaxy S24 Ultra with S Pen and 256GB storage.",
        "specs": {
            "Model": "Galaxy S24 Ultra",
            "Variant": "256GB",
            "RAM": "12GB",
            "Storage": "256GB",
            "Processor": "Snapdragon 8 Gen 3",
            "Display": "6.8 inch Dynamic AMOLED 2X",
            "Refresh Rate": "120Hz",
            "Rear Camera": "200MP + 50MP + 12MP + 10MP",
            "Front Camera": "12MP",
            "Battery": "5000mAh",
            "5G": "Yes",
            "OS": "Android",
            "Charging": "45W",
            "S Pen": "Yes",
            "Water Resistance": "IP68",
        },
    },

    {
        "name": "Samsung Galaxy S24 Ultra 512GB",
        "brand": "Samsung",
        "category": "Electronics",
        "subcategory": "Smartphones",
        "segment": "Ultra Premium Smartphone",
        "price": 139999,
        "mrp": 144999,
        "rating": 4.7,
        "reviews": 9800,
        "description": "Samsung Galaxy S24 Ultra with 512GB storage.",
        "specs": {
            "Model": "Galaxy S24 Ultra",
            "Variant": "512GB",
            "RAM": "12GB",
            "Storage": "512GB",
            "Processor": "Snapdragon 8 Gen 3",
            "Display": "6.8 inch Dynamic AMOLED 2X",
            "Refresh Rate": "120Hz",
            "Rear Camera": "200MP + 50MP + 12MP + 10MP",
            "Front Camera": "12MP",
            "Battery": "5000mAh",
            "5G": "Yes",
            "OS": "Android",
            "Charging": "45W",
            "S Pen": "Yes",
            "Water Resistance": "IP68",
        },
    },

    {
        "name": "Samsung Galaxy S24 FE 128GB",
        "brand": "Samsung",
        "category": "Electronics",
        "subcategory": "Smartphones",
        "segment": "Premium Smartphone",
        "price": 59999,
        "mrp": 64999,
        "rating": 4.4,
        "reviews": 5600,
        "description": "Samsung Galaxy S24 FE with 128GB storage.",
        "specs": {
            "Model": "Galaxy S24 FE",
            "Variant": "128GB",
            "RAM": "8GB",
            "Storage": "128GB",
            "Processor": "Exynos 2400e",
            "Display": "6.7 inch Dynamic AMOLED 2X",
            "Refresh Rate": "120Hz",
            "Rear Camera": "50MP + 8MP + 12MP",
            "Front Camera": "10MP",
            "Battery": "4700mAh",
            "5G": "Yes",
            "OS": "Android",
            "Charging": "25W",
            "Water Resistance": "IP68",
        },
    },

    # --------------------------------------------------------
    # ONEPLUS
    # --------------------------------------------------------

    {
        "name": "OnePlus 12 256GB",
        "brand": "OnePlus",
        "category": "Electronics",
        "subcategory": "Smartphones",
        "segment": "Premium Smartphone",
        "price": 64999,
        "mrp": 69999,
        "rating": 4.6,
        "reviews": 9200,
        "description": "OnePlus 12 with Snapdragon processor and 256GB storage.",
        "specs": {
            "Model": "OnePlus 12",
            "Variant": "256GB",
            "RAM": "12GB",
            "Storage": "256GB",
            "Processor": "Snapdragon 8 Gen 3",
            "Display": "6.82 inch AMOLED",
            "Refresh Rate": "120Hz",
            "Rear Camera": "50MP + 64MP + 48MP",
            "Front Camera": "32MP",
            "Battery": "5400mAh",
            "5G": "Yes",
            "OS": "Android",
            "Charging": "100W",
            "Wireless Charging": "50W",
        },
    },

    {
        "name": "OnePlus 12 512GB",
        "brand": "OnePlus",
        "category": "Electronics",
        "subcategory": "Smartphones",
        "segment": "Premium Smartphone",
        "price": 69999,
        "mrp": 74999,
        "rating": 4.6,
        "reviews": 6700,
        "description": "OnePlus 12 with 512GB storage.",
        "specs": {
            "Model": "OnePlus 12",
            "Variant": "512GB",
            "RAM": "16GB",
            "Storage": "512GB",
            "Processor": "Snapdragon 8 Gen 3",
            "Display": "6.82 inch AMOLED",
            "Refresh Rate": "120Hz",
            "Rear Camera": "50MP + 64MP + 48MP",
            "Front Camera": "32MP",
            "Battery": "5400mAh",
            "5G": "Yes",
            "OS": "Android",
            "Charging": "100W",
            "Wireless Charging": "50W",
        },
    },

    {
        "name": "OnePlus 13 256GB",
        "brand": "OnePlus",
        "category": "Electronics",
        "subcategory": "Smartphones",
        "segment": "Premium Smartphone",
        "price": 69999,
        "mrp": 74999,
        "rating": 4.7,
        "reviews": 5100,
        "description": "OnePlus 13 with flagship processor and 256GB storage.",
        "specs": {
            "Model": "OnePlus 13",
            "Variant": "256GB",
            "RAM": "12GB",
            "Storage": "256GB",
            "Processor": "Snapdragon 8 Elite",
            "Display": "6.82 inch AMOLED",
            "Refresh Rate": "120Hz",
            "Rear Camera": "50MP + 50MP + 50MP",
            "Front Camera": "32MP",
            "Battery": "6000mAh",
            "5G": "Yes",
            "OS": "Android",
            "Charging": "100W",
            "Wireless Charging": "50W",
        },
    },

    # --------------------------------------------------------
    # GOOGLE PIXEL
    # --------------------------------------------------------

    {
        "name": "Google Pixel 9 128GB",
        "brand": "Google",
        "category": "Electronics",
        "subcategory": "Smartphones",
        "segment": "Premium Smartphone",
        "price": 79999,
        "mrp": 79999,
        "rating": 4.5,
        "reviews": 4300,
        "description": "Google Pixel 9 with Tensor processor and 128GB storage.",
        "specs": {
            "Model": "Pixel 9",
            "Variant": "128GB",
            "RAM": "12GB",
            "Storage": "128GB",
            "Processor": "Google Tensor G4",
            "Display": "6.3 inch OLED",
            "Refresh Rate": "120Hz",
            "Rear Camera": "50MP + 48MP",
            "Front Camera": "10.5MP",
            "Battery": "4700mAh",
            "5G": "Yes",
            "OS": "Android",
            "Charging": "27W",
            "Wireless Charging": "Yes",
        },
    },

    {
        "name": "Google Pixel 9 Pro 256GB",
        "brand": "Google",
        "category": "Electronics",
        "subcategory": "Smartphones",
        "segment": "Premium Smartphone",
        "price": 109999,
        "mrp": 109999,
        "rating": 4.6,
        "reviews": 3600,
        "description": "Google Pixel 9 Pro with 256GB storage.",
        "specs": {
            "Model": "Pixel 9 Pro",
            "Variant": "256GB",
            "RAM": "16GB",
            "Storage": "256GB",
            "Processor": "Google Tensor G4",
            "Display": "6.3 inch LTPO OLED",
            "Refresh Rate": "120Hz",
            "Rear Camera": "50MP + 48MP + 48MP",
            "Front Camera": "42MP",
            "Battery": "4700mAh",
            "5G": "Yes",
            "OS": "Android",
            "Charging": "27W",
            "Wireless Charging": "Yes",
        },
    },

    # --------------------------------------------------------
    # XIAOMI
    # --------------------------------------------------------

    {
        "name": "Xiaomi 14 256GB",
        "brand": "Xiaomi",
        "category": "Electronics",
        "subcategory": "Smartphones",
        "segment": "Premium Smartphone",
        "price": 69999,
        "mrp": 79999,
        "rating": 4.5,
        "reviews": 5400,
        "description": "Xiaomi 14 flagship smartphone with 256GB storage.",
        "specs": {
            "Model": "Xiaomi 14",
            "Variant": "256GB",
            "RAM": "12GB",
            "Storage": "256GB",
            "Processor": "Snapdragon 8 Gen 3",
            "Display": "6.36 inch AMOLED",
            "Refresh Rate": "120Hz",
            "Rear Camera": "50MP + 50MP + 50MP",
            "Front Camera": "32MP",
            "Battery": "4610mAh",
            "5G": "Yes",
            "OS": "Android",
            "Charging": "90W",
            "Wireless Charging": "50W",
        },
    },

    {
        "name": "Redmi Note 13 Pro 5G 256GB",
        "brand": "Redmi",
        "category": "Electronics",
        "subcategory": "Smartphones",
        "segment": "Mid Range Smartphone",
        "price": 29999,
        "mrp": 32999,
        "rating": 4.4,
        "reviews": 14500,
        "description": "Redmi Note 13 Pro 5G with 256GB storage.",
        "specs": {
            "Model": "Redmi Note 13 Pro 5G",
            "Variant": "256GB",
            "RAM": "8GB",
            "Storage": "256GB",
            "Processor": "Snapdragon 7s Gen 2",
            "Display": "6.67 inch AMOLED",
            "Refresh Rate": "120Hz",
            "Rear Camera": "200MP + 8MP + 2MP",
            "Front Camera": "16MP",
            "Battery": "5100mAh",
            "5G": "Yes",
            "OS": "Android",
            "Charging": "67W",
        },
    },

    # --------------------------------------------------------
    # MOTOROLA
    # --------------------------------------------------------

    {
        "name": "Motorola Edge 50 Pro 256GB",
        "brand": "Motorola",
        "category": "Electronics",
        "subcategory": "Smartphones",
        "segment": "Premium Smartphone",
        "price": 35999,
        "mrp": 39999,
        "rating": 4.4,
        "reviews": 4900,
        "description": "Motorola Edge 50 Pro with 256GB storage.",
        "specs": {
            "Model": "Edge 50 Pro",
            "Variant": "256GB",
            "RAM": "12GB",
            "Storage": "256GB",
            "Processor": "Snapdragon 7 Gen 3",
            "Display": "6.7 inch pOLED",
            "Refresh Rate": "144Hz",
            "Rear Camera": "50MP + 10MP + 13MP",
            "Front Camera": "50MP",
            "Battery": "4500mAh",
            "5G": "Yes",
            "OS": "Android",
            "Charging": "125W",
            "Wireless Charging": "50W",
        },
    },

    # --------------------------------------------------------
    # NOTHING
    # --------------------------------------------------------

    {
        "name": "Nothing Phone 2 256GB",
        "brand": "Nothing",
        "category": "Electronics",
        "subcategory": "Smartphones",
        "segment": "Premium Smartphone",
        "price": 39999,
        "mrp": 44999,
        "rating": 4.4,
        "reviews": 6200,
        "description": "Nothing Phone 2 with Glyph interface and 256GB storage.",
        "specs": {
            "Model": "Phone 2",
            "Variant": "256GB",
            "RAM": "12GB",
            "Storage": "256GB",
            "Processor": "Snapdragon 8+ Gen 1",
            "Display": "6.7 inch OLED",
            "Refresh Rate": "120Hz",
            "Rear Camera": "50MP + 50MP",
            "Front Camera": "32MP",
            "Battery": "4700mAh",
            "5G": "Yes",
            "OS": "Android",
            "Charging": "45W",
            "Wireless Charging": "15W",
        },
    },

    {
        "name": "Nothing Phone 2a 256GB",
        "brand": "Nothing",
        "category": "Electronics",
        "subcategory": "Smartphones",
        "segment": "Mid Range Smartphone",
        "price": 27999,
        "mrp": 29999,
        "rating": 4.3,
        "reviews": 7800,
        "description": "Nothing Phone 2a with 256GB storage.",
        "specs": {
            "Model": "Phone 2a",
            "Variant": "256GB",
            "RAM": "8GB",
            "Storage": "256GB",
            "Processor": "MediaTek Dimensity 7200 Pro",
            "Display": "6.7 inch AMOLED",
            "Refresh Rate": "120Hz",
            "Rear Camera": "50MP + 50MP",
            "Front Camera": "32MP",
            "Battery": "5000mAh",
            "5G": "Yes",
            "OS": "Android",
            "Charging": "45W",
        },
    },

    # --------------------------------------------------------
    # REALME
    # --------------------------------------------------------

    {
        "name": "Realme GT 6 256GB",
        "brand": "Realme",
        "category": "Electronics",
        "subcategory": "Smartphones",
        "segment": "Premium Smartphone",
        "price": 40999,
        "mrp": 44999,
        "rating": 4.5,
        "reviews": 5100,
        "description": "Realme GT 6 with 256GB storage.",
        "specs": {
            "Model": "GT 6",
            "Variant": "256GB",
            "RAM": "8GB",
            "Storage": "256GB",
            "Processor": "Snapdragon 8s Gen 3",
            "Display": "6.78 inch LTPO AMOLED",
            "Refresh Rate": "120Hz",
            "Rear Camera": "50MP + 8MP",
            "Front Camera": "32MP",
            "Battery": "5500mAh",
            "5G": "Yes",
            "OS": "Android",
            "Charging": "120W",
        },
    },

    # --------------------------------------------------------
    # VIVO
    # --------------------------------------------------------

    {
        "name": "Vivo V40 256GB",
        "brand": "Vivo",
        "category": "Electronics",
        "subcategory": "Smartphones",
        "segment": "Mid Range Smartphone",
        "price": 39999,
        "mrp": 44999,
        "rating": 4.4,
        "reviews": 3900,
        "description": "Vivo V40 with ZEISS camera system and 256GB storage.",
        "specs": {
            "Model": "V40",
            "Variant": "256GB",
            "RAM": "8GB",
            "Storage": "256GB",
            "Processor": "Snapdragon 7 Gen 3",
            "Display": "6.78 inch AMOLED",
            "Refresh Rate": "120Hz",
            "Rear Camera": "50MP + 50MP",
            "Front Camera": "50MP",
            "Battery": "5500mAh",
            "5G": "Yes",
            "OS": "Android",
            "Charging": "80W",
        },
    },

    # --------------------------------------------------------
    # OPPO
    # --------------------------------------------------------

    {
        "name": "OPPO Reno 12 Pro 256GB",
        "brand": "OPPO",
        "category": "Electronics",
        "subcategory": "Smartphones",
        "segment": "Mid Range Smartphone",
        "price": 39999,
        "mrp": 44999,
        "rating": 4.4,
        "reviews": 4300,
        "description": "OPPO Reno 12 Pro with 256GB storage.",
        "specs": {
            "Model": "Reno 12 Pro",
            "Variant": "256GB",
            "RAM": "12GB",
            "Storage": "256GB",
            "Processor": "MediaTek Dimensity 7300 Energy",
            "Display": "6.7 inch AMOLED",
            "Refresh Rate": "120Hz",
            "Rear Camera": "50MP + 50MP + 8MP",
            "Front Camera": "50MP",
            "Battery": "5000mAh",
            "5G": "Yes",
            "OS": "Android",
            "Charging": "80W",
        },
    },

    # --------------------------------------------------------
    # IQOO
    # --------------------------------------------------------

    {
        "name": "iQOO 12 256GB",
        "brand": "iQOO",
        "category": "Electronics",
        "subcategory": "Smartphones",
        "segment": "Performance Smartphone",
        "price": 52999,
        "mrp": 54999,
        "rating": 4.6,
        "reviews": 4700,
        "description": "iQOO 12 flagship performance smartphone.",
        "specs": {
            "Model": "iQOO 12",
            "Variant": "256GB",
            "RAM": "12GB",
            "Storage": "256GB",
            "Processor": "Snapdragon 8 Gen 3",
            "Display": "6.78 inch AMOLED",
            "Refresh Rate": "144Hz",
            "Rear Camera": "50MP + 64MP + 50MP",
            "Front Camera": "16MP",
            "Battery": "5000mAh",
            "5G": "Yes",
            "OS": "Android",
            "Charging": "120W",
        },
    },

    # --------------------------------------------------------
    # POCO
    # --------------------------------------------------------

    {
        "name": "POCO X6 Pro 256GB",
        "brand": "POCO",
        "category": "Electronics",
        "subcategory": "Smartphones",
        "segment": "Performance Smartphone",
        "price": 26999,
        "mrp": 29999,
        "rating": 4.4,
        "reviews": 12500,
        "description": "POCO X6 Pro performance smartphone with 256GB storage.",
        "specs": {
            "Model": "POCO X6 Pro",
            "Variant": "256GB",
            "RAM": "8GB",
            "Storage": "256GB",
            "Processor": "MediaTek Dimensity 8300 Ultra",
            "Display": "6.67 inch AMOLED",
            "Refresh Rate": "120Hz",
            "Rear Camera": "64MP + 8MP + 2MP",
            "Front Camera": "16MP",
            "Battery": "5000mAh",
            "5G": "Yes",
            "OS": "Android",
            "Charging": "67W",
        },
    },
]


# ============================================================
# DATABASE HELPERS
# ============================================================

def product_exists(db, name, brand):
    row = db.execute(
        """
        SELECT id
        FROM products
        WHERE LOWER(name) = LOWER(?)
          AND LOWER(COALESCE(brand, '')) = LOWER(?)
        LIMIT 1
        """,
        (name, brand)
    ).fetchone()

    return row[0] if row else None


def insert_product(db, product):

    existing_id = product_exists(
        db,
        product["name"],
        product["brand"]
    )

    if existing_id:
        return existing_id, False

    cursor = db.execute(
        """
        INSERT INTO products (
            name,
            category,
            brand,
            platform,
            price,
            mrp,
            rating,
            reviews,
            lifespan_years,
            energy_kwh,
            review_text,
            product_url,
            image,
            description,
            stock
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            product["name"],
            product["category"],
            product["brand"],
            "SmartCart Demo Catalogue",
            product["price"],
            product["mrp"],
            product["rating"],
            product["reviews"],
            3,
            0,
            "",
            "#",
            None,
            product["description"],
            1
        )
    )

    return cursor.lastrowid, True


def add_category(db, product_id, product):

    db.execute(
        """
        INSERT OR IGNORE INTO product_categories (
            product_id,
            main_category,
            subcategory,
            segment
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            product_id,
            product["category"],
            product["subcategory"],
            product["segment"]
        )
    )


def add_specs(db, product_id, specs):

    for spec_name, spec_value in specs.items():

        db.execute(
            """
            INSERT OR IGNORE INTO product_specs (
                product_id,
                spec_name,
                spec_value
            )
            VALUES (?, ?, ?)
            """,
            (
                product_id,
                spec_name,
                str(spec_value)
            )
        )


def add_attributes(db, product_id, product):

    attributes = {
        "Brand": product["brand"],
        "Product Type": "Smartphone",
        "Category": "Smartphones",
        "5G": product["specs"].get("5G", "No"),
        "OS": product["specs"].get("OS", ""),
        "RAM": product["specs"].get("RAM", ""),
        "Storage": product["specs"].get("Storage", ""),
        "Processor": product["specs"].get("Processor", ""),
        "Display": product["specs"].get("Display", ""),
        "Refresh Rate": product["specs"].get("Refresh Rate", ""),
    }

    for name, value in attributes.items():

        if not value:
            continue

        db.execute(
            """
            INSERT OR IGNORE INTO product_attributes (
                product_id,
                attribute_name,
                attribute_value
            )
            VALUES (?, ?, ?)
            """,
            (
                product_id,
                name,
                str(value)
            )
        )


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 65)
    print("SMARTCART AI - SMARTPHONE CATALOGUE SEED")
    print("=" * 65)

    if not os.path.exists(DATABASE):
        print()
        print("ERROR: smartcart.db nahi mili.")
        print("Project folder check karein.")
        return

    db = sqlite3.connect(DATABASE)
    db.execute("PRAGMA foreign_keys = ON")

    added = 0
    skipped = 0

    for product in PRODUCTS:

        product_id, was_added = insert_product(
            db,
            product
        )

        if was_added:
            added += 1
            print(
                f"[ADDED] {product['brand']} - "
                f"{product['name']}"
            )
        else:
            skipped += 1
            print(
                f"[SKIP]  {product['brand']} - "
                f"{product['name']} already exists"
            )

        add_category(
            db,
            product_id,
            product
        )

        add_specs(
            db,
            product_id,
            product["specs"]
        )

        add_attributes(
            db,
            product_id,
            product
        )

    db.commit()

    # --------------------------------------------------------
    # FINAL COUNTS
    # --------------------------------------------------------

    total_products = db.execute(
        "SELECT COUNT(*) FROM products"
    ).fetchone()[0]

    total_specs = db.execute(
        "SELECT COUNT(*) FROM product_specs"
    ).fetchone()[0]

    total_categories = db.execute(
        "SELECT COUNT(*) FROM product_categories"
    ).fetchone()[0]

    total_attributes = db.execute(
        "SELECT COUNT(*) FROM product_attributes"
    ).fetchone()[0]

    smartphone_count = db.execute(
        """
        SELECT COUNT(*)
        FROM product_categories
        WHERE subcategory = 'Smartphones'
        """
    ).fetchone()[0]

    db.close()

    print()
    print("=" * 65)
    print("CATALOGUE SEED COMPLETE")
    print("=" * 65)

    print()
    print("New products added     :", added)
    print("Existing products skip :", skipped)

    print()
    print("Total products         :", total_products)
    print("Total specifications   :", total_specs)
    print("Total categories       :", total_categories)
    print("Total attributes       :", total_attributes)
    print("Smartphone catalogue   :", smartphone_count)

    print()
    print("Existing database data was NOT deleted.")
    print("Catalogue data is project/demo data unless externally verified.")
    print()
    print("=" * 65)


if __name__ == "__main__":
    main()