import sqlite3
import re
import shutil
from pathlib import Path

DB_PATH = Path("smartcart.db")
BACKUP_PATH = Path("smartcart_before_product_names.db")


# ---------------------------------------------------------
# SAFE BACKUP
# ---------------------------------------------------------

if not DB_PATH.exists():
    raise FileNotFoundError("smartcart.db nahi mila.")

if not BACKUP_PATH.exists():
    shutil.copy2(DB_PATH, BACKUP_PATH)
    print("Backup created:", BACKUP_PATH)
else:
    print("Backup already exists:", BACKUP_PATH)


# ---------------------------------------------------------
# PRODUCT NAME CATALOGUE
# ---------------------------------------------------------
# Ye names model-style/demo catalogue names hain.
# Existing good names ko hum unnecessarily replace nahi karenge.
# Prices, images, ratings, stock etc. untouched rahenge.

MOBILE_MODELS = {
    "Apple": [
        "Apple iPhone 15 128GB",
        "Apple iPhone 15 256GB",
        "Apple iPhone 15 Plus 128GB",
        "Apple iPhone 15 Pro 128GB",
        "Apple iPhone 15 Pro 256GB",
        "Apple iPhone 15 Pro Max 256GB",
        "Apple iPhone 16 128GB",
        "Apple iPhone 16 256GB",
        "Apple iPhone 16 Plus 128GB",
        "Apple iPhone 16 Pro 128GB",
        "Apple iPhone 16 Pro 256GB",
        "Apple iPhone 16 Pro Max 256GB",
    ],

    "Samsung": [
        "Samsung Galaxy S24 128GB",
        "Samsung Galaxy S24 256GB",
        "Samsung Galaxy S24+ 256GB",
        "Samsung Galaxy S24 Ultra 256GB",
        "Samsung Galaxy S24 Ultra 512GB",
        "Samsung Galaxy S25 128GB",
        "Samsung Galaxy S25 256GB",
        "Samsung Galaxy S25+ 256GB",
        "Samsung Galaxy S25 Ultra 256GB",
        "Samsung Galaxy S25 Ultra 512GB",
        "Samsung Galaxy A55 5G 128GB",
        "Samsung Galaxy A55 5G 256GB",
    ],

    "OnePlus": [
        "OnePlus 12 256GB",
        "OnePlus 12 512GB",
        "OnePlus 12R 128GB",
        "OnePlus 12R 256GB",
        "OnePlus 13 256GB",
        "OnePlus 13 512GB",
        "OnePlus Nord 4 128GB",
        "OnePlus Nord 4 256GB",
    ],

    "Xiaomi": [
        "Xiaomi 14 256GB",
        "Xiaomi 14 512GB",
        "Xiaomi 14 Civi 256GB",
        "Xiaomi 14 Civi 512GB",
        "Redmi Note 13 Pro 5G 128GB",
        "Redmi Note 13 Pro 5G 256GB",
        "Redmi Note 13 Pro+ 5G 256GB",
        "Redmi Note 14 Pro 5G 256GB",
    ],

    "Vivo": [
        "Vivo V30 128GB",
        "Vivo V30 256GB",
        "Vivo V40 128GB",
        "Vivo V40 256GB",
        "Vivo V40 Pro 256GB",
        "Vivo X100 256GB",
        "Vivo X100 Pro 512GB",
    ],

    "Oppo": [
        "OPPO Reno 11 128GB",
        "OPPO Reno 11 256GB",
        "OPPO Reno 12 256GB",
        "OPPO Reno 12 Pro 256GB",
        "OPPO Find X8 256GB",
        "OPPO Find X8 Pro 512GB",
    ],

    "Motorola": [
        "Motorola Edge 50 Fusion 128GB",
        "Motorola Edge 50 Fusion 256GB",
        "Motorola Edge 50 Pro 256GB",
        "Motorola Edge 50 Ultra 512GB",
        "Motorola Razr 50 256GB",
        "Motorola Razr 50 Ultra 512GB",
    ],

    "Realme": [
        "Realme 12 Pro 5G 128GB",
        "Realme 12 Pro+ 5G 256GB",
        "Realme GT 6 256GB",
        "Realme GT 6T 128GB",
        "Realme GT 6T 256GB",
        "Realme 13 Pro+ 5G 256GB",
    ],
}


LAPTOP_MODELS = {
    "Apple": [
        "Apple MacBook Air M2 13-inch 8GB 256GB",
        "Apple MacBook Air M2 15-inch 8GB 256GB",
        "Apple MacBook Air M3 13-inch 8GB 256GB",
        "Apple MacBook Air M3 15-inch 8GB 256GB",
        "Apple MacBook Air M3 16GB 512GB",
        "Apple MacBook Pro M3 14-inch 8GB 512GB",
        "Apple MacBook Pro M3 Pro 18GB 512GB",
        "Apple MacBook Pro M4 14-inch 16GB 512GB",
        "Apple MacBook Pro M4 Pro 24GB 512GB",
    ],

    "Lenovo": [
        "Lenovo IdeaPad Slim 3 15-inch",
        "Lenovo IdeaPad Slim 5 14-inch",
        "Lenovo IdeaPad Slim 5 16-inch",
        "Lenovo LOQ 15 Gaming Laptop",
        "Lenovo Legion 5 Gaming Laptop",
        "Lenovo ThinkPad E14",
        "Lenovo ThinkBook 14",
    ],

    "Dell": [
        "Dell Inspiron 15 3530",
        "Dell Inspiron 14 5430",
        "Dell Vostro 3520",
        "Dell Vostro 3530",
        "Dell XPS 13",
        "Dell XPS 15",
        "Dell G15 Gaming Laptop",
    ],

    "HP": [
        "HP Pavilion 15",
        "HP Pavilion Plus 14",
        "HP 15s 15-inch",
        "HP Victus 15 Gaming Laptop",
        "HP Victus 16 Gaming Laptop",
        "HP Envy x360 14",
        "HP Spectre x360 14",
    ],

    "Asus": [
        "ASUS Vivobook 15",
        "ASUS Vivobook 16",
        "ASUS Zenbook 14 OLED",
        "ASUS TUF Gaming F15",
        "ASUS TUF Gaming A15",
        "ASUS ROG Strix G16",
        "ASUS ROG Zephyrus G14",
    ],

    "Acer": [
        "Acer Aspire 5",
        "Acer Aspire Lite 15",
        "Acer Swift Go 14",
        "Acer Nitro V 15 Gaming Laptop",
        "Acer Predator Helios Neo 16",
    ],
}


CAMERA_MODELS = {
    "Canon": [
        "Canon EOS R50 Mirrorless Camera",
        "Canon EOS R10 Mirrorless Camera",
        "Canon EOS R7 Mirrorless Camera",
        "Canon EOS R8 Full Frame Mirrorless Camera",
        "Canon EOS R6 Mark II Mirrorless Camera",
        "Canon EOS 200D II DSLR Camera",
    ],

    "Sony": [
        "Sony Alpha A6400 Mirrorless Camera",
        "Sony Alpha A6700 Mirrorless Camera",
        "Sony Alpha A7 III Mirrorless Camera",
        "Sony Alpha A7 IV Mirrorless Camera",
        "Sony Alpha A7C II Mirrorless Camera",
    ],

    "Nikon": [
        "Nikon Z50 Mirrorless Camera",
        "Nikon Z5 Full Frame Mirrorless Camera",
        "Nikon Z6 II Mirrorless Camera",
        "Nikon Z7 II Mirrorless Camera",
        "Nikon Zf Full Frame Mirrorless Camera",
    ],

    "Fujifilm": [
        "Fujifilm X-S20 Mirrorless Camera",
        "Fujifilm X-T30 II Mirrorless Camera",
        "Fujifilm X-T5 Mirrorless Camera",
        "Fujifilm X100VI Compact Camera",
    ],

    "GoPro": [
        "GoPro HERO12 Black",
        "GoPro HERO13 Black",
        "GoPro HERO11 Black",
    ],

    "DJI": [
        "DJI Osmo Action 4",
        "DJI Osmo Action 5 Pro",
        "DJI Pocket 3",
        "DJI Mini 4 Pro",
    ],
}


TV_MODELS = {
    "Sony": [
        "Sony Bravia 55-inch 4K Google TV",
        "Sony Bravia 65-inch 4K Google TV",
        "Sony Bravia OLED 55-inch 4K TV",
        "Sony Bravia OLED 65-inch 4K TV",
    ],

    "LG": [
        "LG 43-inch 4K Smart TV",
        "LG 55-inch 4K UHD Smart TV",
        "LG 65-inch 4K UHD Smart TV",
        "LG OLED 55-inch 4K Smart TV",
        "LG OLED 65-inch 4K Smart TV",
    ],

    "Samsung": [
        "Samsung 43-inch Crystal 4K Smart TV",
        "Samsung 50-inch Crystal 4K Smart TV",
        "Samsung 55-inch Crystal 4K Smart TV",
        "Samsung 55-inch QLED 4K Smart TV",
        "Samsung 65-inch QLED 4K Smart TV",
    ],

    "Hisense": [
        "Hisense 43-inch 4K Smart TV",
        "Hisense 55-inch 4K Smart TV",
        "Hisense 65-inch 4K Smart TV",
    ],

    "TCL": [
        "TCL 43-inch 4K Smart TV",
        "TCL 55-inch 4K Smart TV",
        "TCL 65-inch QLED 4K Smart TV",
    ],

    "Xiaomi": [
        "Xiaomi 43-inch 4K Smart TV",
        "Xiaomi 50-inch 4K Smart TV",
        "Xiaomi 55-inch 4K Smart TV",
        "Xiaomi 65-inch 4K Smart TV",
    ],
}


AUDIO_MODELS = {
    "Sony": [
        "Sony WH-1000XM5 Wireless Headphones",
        "Sony WH-1000XM4 Wireless Headphones",
        "Sony WF-1000XM5 Wireless Earbuds",
        "Sony ULT Field 1 Portable Speaker",
    ],

    "JBL": [
        "JBL Tune 770NC Wireless Headphones",
        "JBL Live 660NC Wireless Headphones",
        "JBL Flip 6 Portable Speaker",
        "JBL Charge 5 Portable Speaker",
        "JBL PartyBox 110",
    ],

    "Sennheiser": [
        "Sennheiser Momentum 4 Wireless Headphones",
        "Sennheiser Accentum Wireless Headphones",
        "Sennheiser Momentum True Wireless 4",
    ],

    "boAt": [
        "boAt Rockerz 450 Wireless Headphones",
        "boAt Rockerz 550 Wireless Headphones",
        "boAt Airdopes 141",
        "boAt Airdopes 161",
        "boAt Nirvana Ion",
    ],

    "Noise": [
        "Noise Buds VS104",
        "Noise Buds X Prime",
        "Noise Air Buds Pro",
    ],

    "Anker": [
        "Anker Soundcore Life Q30",
        "Anker Soundcore Space One",
        "Anker Soundcore Motion+",
    ],
}


GAMING_MODELS = {
    "Microsoft": [
        "Microsoft Xbox Series X",
        "Microsoft Xbox Series S",
        "Microsoft Xbox Wireless Controller",
    ],

    "Logitech": [
        "Logitech G502 HERO Gaming Mouse",
        "Logitech G Pro Wireless Gaming Mouse",
        "Logitech G733 Wireless Gaming Headset",
        "Logitech G915 TKL Gaming Keyboard",
    ],

    "Razer": [
        "Razer DeathAdder V3 Gaming Mouse",
        "Razer Basilisk V3 Gaming Mouse",
        "Razer BlackShark V2 Gaming Headset",
        "Razer Huntsman V3 Pro Gaming Keyboard",
    ],

    "Corsair": [
        "Corsair K70 RGB Gaming Keyboard",
        "Corsair K65 RGB Gaming Keyboard",
        "Corsair HS80 RGB Wireless Headset",
    ],

    "Redragon": [
        "Redragon K552 Mechanical Gaming Keyboard",
        "Redragon M711 Gaming Mouse",
        "Redragon H510 Gaming Headset",
    ],
}


HOME_MODELS = {
    "Prestige": [
        "Prestige Electric Kettle 1.5L",
        "Prestige Mixer Grinder 750W",
        "Prestige Induction Cooktop",
        "Prestige Air Fryer 4.5L",
    ],

    "Bajaj": [
        "Bajaj Rex Mixer Grinder 500W",
        "Bajaj GX8 Mixer Grinder 750W",
        "Bajaj Majesty Electric Kettle 1.5L",
        "Bajaj Majesty Air Fryer",
    ],

    "Philips": [
        "Philips Air Fryer 4.1L",
        "Philips Mixer Grinder 750W",
        "Philips Electric Kettle 1.5L",
        "Philips Garment Steamer",
    ],

    "Bosch": [
        "Bosch Mixer Grinder 750W",
        "Bosch Electric Kettle 1.5L",
        "Bosch Food Processor",
        "Bosch Air Fryer",
    ],

    "Havells": [
        "Havells Aqua Plus Electric Kettle",
        "Havells Air Fryer 5L",
        "Havells Mixer Grinder 750W",
        "Havells Electric Oven",
    ],

    "Morphy Richards": [
        "Morphy Richards Air Fryer 5L",
        "Morphy Richards Electric Kettle 1.5L",
        "Morphy Richards OTG Oven",
        "Morphy Richards Mixer Grinder",
    ],
}


FASHION_MODELS = {
    "Nike": [
        "Nike Air Max Running Shoes",
        "Nike Revolution Running Shoes",
        "Nike Downshifter Running Shoes",
        "Nike Court Vision Low Sneakers",
    ],

    "Adidas": [
        "Adidas Ultraboost Running Shoes",
        "Adidas Duramo Running Shoes",
        "Adidas Grand Court Sneakers",
        "Adidas Runfalcon Running Shoes",
    ],

    "Puma": [
        "Puma Softride Running Shoes",
        "Puma Flyer Runner Shoes",
        "Puma Smash V2 Sneakers",
        "Puma RS-X Sneakers",
    ],

    "Fossil": [
        "Fossil Gen 6 Smartwatch",
        "Fossil Machine Chronograph Watch",
        "Fossil Grant Chronograph Watch",
    ],

    "Wildcraft": [
        "Wildcraft 35L Travel Backpack",
        "Wildcraft 45L Hiking Backpack",
        "Wildcraft Laptop Backpack 25L",
    ],
}


# ---------------------------------------------------------
# HELPERS
# ---------------------------------------------------------

def looks_synthetic(name):
    """
    Detects names such as:
    Apple Gaming Laptop SKU-00093 Demo SKU-00093
    OnePlus Smartphone SKU-09914 Demo SKU-09914
    """
    if not name:
        return True

    text = str(name).lower()

    patterns = [
        r"\bsku[-\s]?\d+\b",
        r"\bdemo\b",
        r"\bsample\b",
        r"\bgeneric\b",
        r"\btest\b",
        r"\bproduct[-\s]?\d+\b",
    ]

    return any(re.search(pattern, text) for pattern in patterns)


def choose_name(models, index):
    if not models:
        return None

    return models[index % len(models)]


def get_catalogue(category, brand):
    category = (category or "").strip()
    brand = (brand or "").strip()

    if category == "Mobiles":
        return MOBILE_MODELS.get(brand, [])

    if category == "Laptops":
        return LAPTOP_MODELS.get(brand, [])

    if category == "Cameras":
        return CAMERA_MODELS.get(brand, [])

    if category == "TV & Home":
        return TV_MODELS.get(brand, [])

    if category == "Audio":
        return AUDIO_MODELS.get(brand, [])

    if category == "Gaming":
        return GAMING_MODELS.get(brand, [])

    if category == "Home & Kitchen":
        return HOME_MODELS.get(brand, [])

    if category in ("Fashion", "Clothing"):
        return FASHION_MODELS.get(brand, [])

    return []


# ---------------------------------------------------------
# UPDATE
# ---------------------------------------------------------

db = sqlite3.connect(DB_PATH)
db.row_factory = sqlite3.Row

products = db.execute(
    """
    SELECT id, name, brand, category
    FROM products
    ORDER BY id
    """
).fetchall()

updated = 0
skipped = 0
not_supported = 0

brand_counters = {}

for product in products:
    product_id = product["id"]
    old_name = product["name"]
    brand = product["brand"]
    category = product["category"]

    # Existing proper names remain unchanged.
    if not looks_synthetic(old_name):
        skipped += 1
        continue

    models = get_catalogue(category, brand)

    if not models:
        not_supported += 1
        continue

    key = f"{category}|{brand}"

    index = brand_counters.get(key, 0)

    new_name = choose_name(models, index)

    brand_counters[key] = index + 1

    if not new_name:
        not_supported += 1
        continue

    db.execute(
        """
        UPDATE products
        SET name = ?
        WHERE id = ?
        """,
        (new_name, product_id)
    )

    updated += 1


db.commit()


# ---------------------------------------------------------
# RESULT
# ---------------------------------------------------------

print()
print("=" * 60)
print("SMARTCART PRODUCT NAME UPDATE")
print("=" * 60)
print("Total products:", len(products))
print("Updated:", updated)
print("Already proper / skipped:", skipped)
print("Unsupported category/brand:", not_supported)
print("=" * 60)

print()
print("Sample updated products:")

rows = db.execute(
    """
    SELECT id, name, brand, category
    FROM products
    WHERE id <= 120
    ORDER BY id
    """
).fetchall()

for row in rows:
    print(
        f"{row['id']:5} | "
        f"{row['brand']:<18} | "
        f"{row['category']:<18} | "
        f"{row['name']}"
    )

db.close()

print()
print("DONE.")
print("Database preserved:", DB_PATH)
print("Backup available:", BACKUP_PATH)