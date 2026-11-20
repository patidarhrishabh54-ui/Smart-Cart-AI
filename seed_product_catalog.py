import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, "smartcart.db")


SMARTPHONES = [

    # =========================================================
    # APPLE
    # =========================================================

    {
        "name": "Apple iPhone 15 128GB",
        "brand": "Apple",
        "price": 59999,
        "mrp": 69900,
        "rating": 4.6,
        "reviews": 12500,
        "storage": "128 GB",
        "ram": "6 GB",
        "camera": "48 MP",
        "front_camera": "12 MP",
        "battery": "3349 mAh",
        "display": "6.1 inch",
        "display_type": "Super Retina XDR OLED",
        "refresh_rate": "60 Hz",
        "processor": "Apple A16 Bionic",
        "network": "5G",
        "os": "iOS",
        "description": "Apple iPhone 15 with 6.1-inch display, A16 Bionic chip and 48MP main camera."
    },

    {
        "name": "Apple iPhone 15 256GB",
        "brand": "Apple",
        "price": 69999,
        "mrp": 79900,
        "rating": 4.6,
        "reviews": 9800,
        "storage": "256 GB",
        "ram": "6 GB",
        "camera": "48 MP",
        "front_camera": "12 MP",
        "battery": "3349 mAh",
        "display": "6.1 inch",
        "display_type": "Super Retina XDR OLED",
        "refresh_rate": "60 Hz",
        "processor": "Apple A16 Bionic",
        "network": "5G",
        "os": "iOS",
        "description": "Apple iPhone 15 256GB with A16 Bionic processor and 48MP camera."
    },

    {
        "name": "Apple iPhone 15 Plus 128GB",
        "brand": "Apple",
        "price": 69999,
        "mrp": 79900,
        "rating": 4.6,
        "reviews": 7100,
        "storage": "128 GB",
        "ram": "6 GB",
        "camera": "48 MP",
        "front_camera": "12 MP",
        "battery": "4383 mAh",
        "display": "6.7 inch",
        "display_type": "Super Retina XDR OLED",
        "refresh_rate": "60 Hz",
        "processor": "Apple A16 Bionic",
        "network": "5G",
        "os": "iOS",
        "description": "Apple iPhone 15 Plus with large 6.7-inch OLED display."
    },

    {
        "name": "Apple iPhone 15 Pro 128GB",
        "brand": "Apple",
        "price": 109999,
        "mrp": 119900,
        "rating": 4.7,
        "reviews": 8600,
        "storage": "128 GB",
        "ram": "8 GB",
        "camera": "48 MP",
        "front_camera": "12 MP",
        "battery": "3274 mAh",
        "display": "6.1 inch",
        "display_type": "Super Retina XDR OLED",
        "refresh_rate": "120 Hz",
        "processor": "Apple A17 Pro",
        "network": "5G",
        "os": "iOS",
        "description": "Apple iPhone 15 Pro with titanium design and A17 Pro chip."
    },

    {
        "name": "Apple iPhone 15 Pro Max 256GB",
        "brand": "Apple",
        "price": 129999,
        "mrp": 139900,
        "rating": 4.8,
        "reviews": 11200,
        "storage": "256 GB",
        "ram": "8 GB",
        "camera": "48 MP",
        "front_camera": "12 MP",
        "battery": "4441 mAh",
        "display": "6.7 inch",
        "display_type": "Super Retina XDR OLED",
        "refresh_rate": "120 Hz",
        "processor": "Apple A17 Pro",
        "network": "5G",
        "os": "iOS",
        "description": "Apple iPhone 15 Pro Max with A17 Pro chip and advanced camera system."
    },

    {
        "name": "Apple iPhone 16 128GB",
        "brand": "Apple",
        "price": 69999,
        "mrp": 79900,
        "rating": 4.7,
        "reviews": 13400,
        "storage": "128 GB",
        "ram": "8 GB",
        "camera": "48 MP",
        "front_camera": "12 MP",
        "battery": "3561 mAh",
        "display": "6.1 inch",
        "display_type": "Super Retina XDR OLED",
        "refresh_rate": "60 Hz",
        "processor": "Apple A18",
        "network": "5G",
        "os": "iOS",
        "description": "Apple iPhone 16 with A18 chip and advanced camera system."
    },

    {
        "name": "Apple iPhone 16 256GB",
        "brand": "Apple",
        "price": 79999,
        "mrp": 89900,
        "rating": 4.7,
        "reviews": 8700,
        "storage": "256 GB",
        "ram": "8 GB",
        "camera": "48 MP",
        "front_camera": "12 MP",
        "battery": "3561 mAh",
        "display": "6.1 inch",
        "display_type": "Super Retina XDR OLED",
        "refresh_rate": "60 Hz",
        "processor": "Apple A18",
        "network": "5G",
        "os": "iOS",
        "description": "Apple iPhone 16 256GB with A18 processor."
    },

    {
        "name": "Apple iPhone 16 Pro 128GB",
        "brand": "Apple",
        "price": 109999,
        "mrp": 119900,
        "rating": 4.8,
        "reviews": 9300,
        "storage": "128 GB",
        "ram": "8 GB",
        "camera": "48 MP",
        "front_camera": "12 MP",
        "battery": "3582 mAh",
        "display": "6.3 inch",
        "display_type": "Super Retina XDR OLED",
        "refresh_rate": "120 Hz",
        "processor": "Apple A18 Pro",
        "network": "5G",
        "os": "iOS",
        "description": "Apple iPhone 16 Pro with A18 Pro chip and Pro camera system."
    },

    {
        "name": "Apple iPhone 16 Pro Max 256GB",
        "brand": "Apple",
        "price": 119999,
        "mrp": 129900,
        "rating": 4.8,
        "reviews": 11800,
        "storage": "256 GB",
        "ram": "8 GB",
        "camera": "48 MP",
        "front_camera": "12 MP",
        "battery": "4685 mAh",
        "display": "6.9 inch",
        "display_type": "Super Retina XDR OLED",
        "refresh_rate": "120 Hz",
        "processor": "Apple A18 Pro",
        "network": "5G",
        "os": "iOS",
        "description": "Apple iPhone 16 Pro Max with 6.9-inch display and A18 Pro chip."
    },

    # =========================================================
    # SAMSUNG
    # =========================================================

    {
        "name": "Samsung Galaxy S24 128GB",
        "brand": "Samsung",
        "price": 69999,
        "mrp": 79999,
        "rating": 4.6,
        "reviews": 15400,
        "storage": "128 GB",
        "ram": "8 GB",
        "camera": "50 MP",
        "front_camera": "12 MP",
        "battery": "4000 mAh",
        "display": "6.2 inch",
        "display_type": "Dynamic AMOLED 2X",
        "refresh_rate": "120 Hz",
        "processor": "Snapdragon / Exynos",
        "network": "5G",
        "os": "Android",
        "description": "Samsung Galaxy S24 flagship smartphone."
    },

    {
        "name": "Samsung Galaxy S24 256GB",
        "brand": "Samsung",
        "price": 75999,
        "mrp": 84999,
        "rating": 4.6,
        "reviews": 10800,
        "storage": "256 GB",
        "ram": "8 GB",
        "camera": "50 MP",
        "front_camera": "12 MP",
        "battery": "4000 mAh",
        "display": "6.2 inch",
        "display_type": "Dynamic AMOLED 2X",
        "refresh_rate": "120 Hz",
        "processor": "Snapdragon / Exynos",
        "network": "5G",
        "os": "Android",
        "description": "Samsung Galaxy S24 256GB flagship smartphone."
    },

    {
        "name": "Samsung Galaxy S24 Ultra 256GB",
        "brand": "Samsung",
        "price": 109999,
        "mrp": 129999,
        "rating": 4.8,
        "reviews": 21400,
        "storage": "256 GB",
        "ram": "12 GB",
        "camera": "200 MP",
        "front_camera": "12 MP",
        "battery": "5000 mAh",
        "display": "6.8 inch",
        "display_type": "Dynamic AMOLED 2X",
        "refresh_rate": "120 Hz",
        "processor": "Snapdragon 8 Gen 3",
        "network": "5G",
        "os": "Android",
        "description": "Samsung Galaxy S24 Ultra with 200MP camera and S Pen."
    },

    {
        "name": "Samsung Galaxy S24 Ultra 512GB",
        "brand": "Samsung",
        "price": 129999,
        "mrp": 139999,
        "rating": 4.8,
        "reviews": 17200,
        "storage": "512 GB",
        "ram": "12 GB",
        "camera": "200 MP",
        "front_camera": "12 MP",
        "battery": "5000 mAh",
        "display": "6.8 inch",
        "display_type": "Dynamic AMOLED 2X",
        "refresh_rate": "120 Hz",
        "processor": "Snapdragon 8 Gen 3",
        "network": "5G",
        "os": "Android",
        "description": "Samsung Galaxy S24 Ultra 512GB flagship smartphone."
    },

    {
        "name": "Samsung Galaxy S25 256GB",
        "brand": "Samsung",
        "price": 80999,
        "mrp": 85999,
        "rating": 4.7,
        "reviews": 8600,
        "storage": "256 GB",
        "ram": "12 GB",
        "camera": "50 MP",
        "front_camera": "12 MP",
        "battery": "4000 mAh",
        "display": "6.2 inch",
        "display_type": "Dynamic AMOLED 2X",
        "refresh_rate": "120 Hz",
        "processor": "Snapdragon 8 Elite",
        "network": "5G",
        "os": "Android",
        "description": "Samsung Galaxy S25 flagship smartphone."
    },

    {
        "name": "Samsung Galaxy S25 Ultra 256GB",
        "brand": "Samsung",
        "price": 119999,
        "mrp": 129999,
        "rating": 4.8,
        "reviews": 9700,
        "storage": "256 GB",
        "ram": "12 GB",
        "camera": "200 MP",
        "front_camera": "12 MP",
        "battery": "5000 mAh",
        "display": "6.9 inch",
        "display_type": "Dynamic AMOLED 2X",
        "refresh_rate": "120 Hz",
        "processor": "Snapdragon 8 Elite",
        "network": "5G",
        "os": "Android",
        "description": "Samsung Galaxy S25 Ultra flagship smartphone."
    },

    # =========================================================
    # ONEPLUS
    # =========================================================

    {
        "name": "OnePlus 12 256GB",
        "brand": "OnePlus",
        "price": 64999,
        "mrp": 69999,
        "rating": 4.6,
        "reviews": 12600,
        "storage": "256 GB",
        "ram": "12 GB",
        "camera": "50 MP",
        "front_camera": "32 MP",
        "battery": "5400 mAh",
        "display": "6.82 inch",
        "display_type": "AMOLED",
        "refresh_rate": "120 Hz",
        "processor": "Snapdragon 8 Gen 3",
        "network": "5G",
        "os": "Android",
        "description": "OnePlus 12 flagship smartphone with high performance hardware."
    },

    {
        "name": "OnePlus 12 512GB",
        "brand": "OnePlus",
        "price": 69999,
        "mrp": 75999,
        "rating": 4.6,
        "reviews": 7900,
        "storage": "512 GB",
        "ram": "16 GB",
        "camera": "50 MP",
        "front_camera": "32 MP",
        "battery": "5400 mAh",
        "display": "6.82 inch",
        "display_type": "AMOLED",
        "refresh_rate": "120 Hz",
        "processor": "Snapdragon 8 Gen 3",
        "network": "5G",
        "os": "Android",
        "description": "OnePlus 12 512GB high-performance flagship smartphone."
    },

    {
        "name": "OnePlus 13 256GB",
        "brand": "OnePlus",
        "price": 69999,
        "mrp": 74999,
        "rating": 4.7,
        "reviews": 6100,
        "storage": "256 GB",
        "ram": "12 GB",
        "camera": "50 MP",
        "front_camera": "32 MP",
        "battery": "6000 mAh",
        "display": "6.82 inch",
        "display_type": "LTPO AMOLED",
        "refresh_rate": "120 Hz",
        "processor": "Snapdragon 8 Elite",
        "network": "5G",
        "os": "Android",
        "description": "OnePlus 13 flagship smartphone."
    },

    {
        "name": "OnePlus 13 512GB",
        "brand": "OnePlus",
        "price": 79999,
        "mrp": 84999,
        "rating": 4.7,
        "reviews": 4900,
        "storage": "512 GB",
        "ram": "16 GB",
        "camera": "50 MP",
        "front_camera": "32 MP",
        "battery": "6000 mAh",
        "display": "6.82 inch",
        "display_type": "LTPO AMOLED",
        "refresh_rate": "120 Hz",
        "processor": "Snapdragon 8 Elite",
        "network": "5G",
        "os": "Android",
        "description": "OnePlus 13 512GB flagship smartphone."
    },

    # =========================================================
    # GOOGLE PIXEL
    # =========================================================

    {
        "name": "Google Pixel 8 128GB",
        "brand": "Google",
        "price": 54999,
        "mrp": 75999,
        "rating": 4.5,
        "reviews": 7200,
        "storage": "128 GB",
        "ram": "8 GB",
        "camera": "50 MP",
        "front_camera": "10.5 MP",
        "battery": "4575 mAh",
        "display": "6.2 inch",
        "display_type": "OLED",
        "refresh_rate": "120 Hz",
        "processor": "Google Tensor G3",
        "network": "5G",
        "os": "Android",
        "description": "Google Pixel 8 with Tensor processor and advanced computational photography."
    },

    {
        "name": "Google Pixel 8 Pro 128GB",
        "brand": "Google",
        "price": 79999,
        "mrp": 106999,
        "rating": 4.6,
        "reviews": 5400,
        "storage": "128 GB",
        "ram": "12 GB",
        "camera": "50 MP",
        "front_camera": "10.5 MP",
        "battery": "5050 mAh",
        "display": "6.7 inch",
        "display_type": "LTPO OLED",
        "refresh_rate": "120 Hz",
        "processor": "Google Tensor G3",
        "network": "5G",
        "os": "Android",
        "description": "Google Pixel 8 Pro flagship smartphone."
    },

    {
        "name": "Google Pixel 9 128GB",
        "brand": "Google",
        "price": 74999,
        "mrp": 79999,
        "rating": 4.6,
        "reviews": 4300,
        "storage": "128 GB",
        "ram": "12 GB",
        "camera": "50 MP",
        "front_camera": "10.5 MP",
        "battery": "4700 mAh",
        "display": "6.3 inch",
        "display_type": "OLED",
        "refresh_rate": "120 Hz",
        "processor": "Google Tensor G4",
        "network": "5G",
        "os": "Android",
        "description": "Google Pixel 9 smartphone with Tensor G4 processor."
    },

    {
        "name": "Google Pixel 9 Pro 256GB",
        "brand": "Google",
        "price": 109999,
        "mrp": 119999,
        "rating": 4.7,
        "reviews": 3500,
        "storage": "256 GB",
        "ram": "16 GB",
        "camera": "50 MP",
        "front_camera": "42 MP",
        "battery": "4700 mAh",
        "display": "6.3 inch",
        "display_type": "LTPO OLED",
        "refresh_rate": "120 Hz",
        "processor": "Google Tensor G4",
        "network": "5G",
        "os": "Android",
        "description": "Google Pixel 9 Pro with advanced camera system and Tensor G4."
    },

    # =========================================================
    # XIAOMI / REDMI
    # =========================================================

    {
        "name": "Xiaomi 14 256GB",
        "brand": "Xiaomi",
        "price": 59999,
        "mrp": 69999,
        "rating": 4.5,
        "reviews": 6200,
        "storage": "256 GB",
        "ram": "12 GB",
        "camera": "50 MP",
        "front_camera": "32 MP",
        "battery": "4610 mAh",
        "display": "6.36 inch",
        "display_type": "AMOLED",
        "refresh_rate": "120 Hz",
        "processor": "Snapdragon 8 Gen 3",
        "network": "5G",
        "os": "Android",
        "description": "Xiaomi 14 flagship smartphone."
    },

    {
        "name": "Xiaomi 14 Ultra 512GB",
        "brand": "Xiaomi",
        "price": 99999,
        "mrp": 109999,
        "rating": 4.6,
        "reviews": 3900,
        "storage": "512 GB",
        "ram": "16 GB",
        "camera": "50 MP Quad Camera",
        "front_camera": "32 MP",
        "battery": "5000 mAh",
        "display": "6.73 inch",
        "display_type": "LTPO AMOLED",
        "refresh_rate": "120 Hz",
        "processor": "Snapdragon 8 Gen 3",
        "network": "5G",
        "os": "Android",
        "description": "Xiaomi 14 Ultra premium camera-focused smartphone."
    },

    {
        "name": "Redmi Note 13 Pro 5G 128GB",
        "brand": "Redmi",
        "price": 24999,
        "mrp": 31999,
        "rating": 4.4,
        "reviews": 18200,
        "storage": "128 GB",
        "ram": "8 GB",
        "camera": "200 MP",
        "front_camera": "16 MP",
        "battery": "5100 mAh",
        "display": "6.67 inch",
        "display_type": "AMOLED",
        "refresh_rate": "120 Hz",
        "processor": "Snapdragon 7s Gen 2",
        "network": "5G",
        "os": "Android",
        "description": "Redmi Note 13 Pro 5G with 200MP camera."
    },

    {
        "name": "Redmi Note 13 Pro+ 5G 256GB",
        "brand": "Redmi",
        "price": 29999,
        "mrp": 35999,
        "rating": 4.5,
        "reviews": 14700,
        "storage": "256 GB",
        "ram": "12 GB",
        "camera": "200 MP",
        "front_camera": "16 MP",
        "battery": "5000 mAh",
        "display": "6.67 inch",
        "display_type": "AMOLED",
        "refresh_rate": "120 Hz",
        "processor": "MediaTek Dimensity 7200 Ultra",
        "network": "5G",
        "os": "Android",
        "description": "Redmi Note 13 Pro+ 5G smartphone."
    },

    # =========================================================
    # MOTOROLA
    # =========================================================

    {
        "name": "Motorola Edge 50 Fusion 128GB",
        "brand": "Motorola",
        "price": 22999,
        "mrp": 27999,
        "rating": 4.4,
        "reviews": 8200,
        "storage": "128 GB",
        "ram": "8 GB",
        "camera": "50 MP",
        "front_camera": "32 MP",
        "battery": "5000 mAh",
        "display": "6.7 inch",
        "display_type": "pOLED",
        "refresh_rate": "144 Hz",
        "processor": "Snapdragon 7s Gen 2",
        "network": "5G",
        "os": "Android",
        "description": "Motorola Edge 50 Fusion with pOLED display."
    },

    {
        "name": "Motorola Edge 50 Pro 256GB",
        "brand": "Motorola",
        "price": 31999,
        "mrp": 39999,
        "rating": 4.5,
        "reviews": 6300,
        "storage": "256 GB",
        "ram": "12 GB",
        "camera": "50 MP",
        "front_camera": "50 MP",
        "battery": "4500 mAh",
        "display": "6.7 inch",
        "display_type": "pOLED",
        "refresh_rate": "144 Hz",
        "processor": "Snapdragon 7 Gen 3",
        "network": "5G",
        "os": "Android",
        "description": "Motorola Edge 50 Pro premium smartphone."
    },

    # =========================================================
    # NOTHING
    # =========================================================

    {
        "name": "Nothing Phone 2 256GB",
        "brand": "Nothing",
        "price": 39999,
        "mrp": 49999,
        "rating": 4.4,
        "reviews": 7100,
        "storage": "256 GB",
        "ram": "12 GB",
        "camera": "50 MP",
        "front_camera": "32 MP",
        "battery": "4700 mAh",
        "display": "6.7 inch",
        "display_type": "OLED",
        "refresh_rate": "120 Hz",
        "processor": "Snapdragon 8+ Gen 1",
        "network": "5G",
        "os": "Android",
        "description": "Nothing Phone 2 with transparent design and Glyph interface."
    },

    {
        "name": "Nothing Phone 2a 128GB",
        "brand": "Nothing",
        "price": 23999,
        "mrp": 27999,
        "rating": 4.3,
        "reviews": 9200,
        "storage": "128 GB",
        "ram": "8 GB",
        "camera": "50 MP",
        "front_camera": "32 MP",
        "battery": "5000 mAh",
        "display": "6.7 inch",
        "display_type": "AMOLED",
        "refresh_rate": "120 Hz",
        "processor": "MediaTek Dimensity 7200 Pro",
        "network": "5G",
        "os": "Android",
        "description": "Nothing Phone 2a with AMOLED display and Glyph design."
    },

    # =========================================================
    # REALME
    # =========================================================

    {
        "name": "Realme GT 6 256GB",
        "brand": "Realme",
        "price": 40999,
        "mrp": 44999,
        "rating": 4.5,
        "reviews": 6800,
        "storage": "256 GB",
        "ram": "8 GB",
        "camera": "50 MP",
        "front_camera": "32 MP",
        "battery": "5500 mAh",
        "display": "6.78 inch",
        "display_type": "LTPO AMOLED",
        "refresh_rate": "120 Hz",
        "processor": "Snapdragon 8s Gen 3",
        "network": "5G",
        "os": "Android",
        "description": "Realme GT 6 performance smartphone."
    },

    {
        "name": "Realme 13 Pro 5G 128GB",
        "brand": "Realme",
        "price": 25999,
        "mrp": 29999,
        "rating": 4.3,
        "reviews": 4100,
        "storage": "128 GB",
        "ram": "8 GB",
        "camera": "50 MP",
        "front_camera": "32 MP",
        "battery": "5200 mAh",
        "display": "6.7 inch",
        "display_type": "OLED",
        "refresh_rate": "120 Hz",
        "processor": "Snapdragon 7s Gen 2",
        "network": "5G",
        "os": "Android",
        "description": "Realme 13 Pro 5G smartphone."
    },

    # =========================================================
    # VIVO
    # =========================================================

    {
        "name": "Vivo V40 128GB",
        "brand": "Vivo",
        "price": 34999,
        "mrp": 39999,
        "rating": 4.4,
        "reviews": 5300,
        "storage": "128 GB",
        "ram": "8 GB",
        "camera": "50 MP",
        "front_camera": "50 MP",
        "battery": "5500 mAh",
        "display": "6.78 inch",
        "display_type": "AMOLED",
        "refresh_rate": "120 Hz",
        "processor": "Snapdragon 7 Gen 3",
        "network": "5G",
        "os": "Android",
        "description": "Vivo V40 smartphone with ZEISS camera system."
    },

    {
        "name": "Vivo X100 256GB",
        "brand": "Vivo",
        "price": 59999,
        "mrp": 69999,
        "rating": 4.6,
        "reviews": 4600,
        "storage": "256 GB",
        "ram": "12 GB",
        "camera": "50 MP Triple Camera",
        "front_camera": "32 MP",
        "battery": "5000 mAh",
        "display": "6.78 inch",
        "display_type": "AMOLED",
        "refresh_rate": "120 Hz",
        "processor": "MediaTek Dimensity 9300",
        "network": "5G",
        "os": "Android",
        "description": "Vivo X100 premium camera smartphone."
    },

    # =========================================================
    # OPPO
    # =========================================================

    {
        "name": "OPPO Reno 12 256GB",
        "brand": "OPPO",
        "price": 32999,
        "mrp": 37999,
        "rating": 4.3,
        "reviews": 3800,
        "storage": "256 GB",
        "ram": "8 GB",
        "camera": "50 MP",
        "front_camera": "32 MP",
        "battery": "5000 mAh",
        "display": "6.7 inch",
        "display_type": "AMOLED",
        "refresh_rate": "120 Hz",
        "processor": "MediaTek Dimensity 7300-Energy",
        "network": "5G",
        "os": "Android",
        "description": "OPPO Reno 12 smartphone."
    },

    {
        "name": "OPPO Find X8 256GB",
        "brand": "OPPO",
        "price": 69999,
        "mrp": 79999,
        "rating": 4.6,
        "reviews": 2800,
        "storage": "256 GB",
        "ram": "12 GB",
        "camera": "50 MP Triple Camera",
        "front_camera": "32 MP",
        "battery": "5630 mAh",
        "display": "6.59 inch",
        "display_type": "AMOLED",
        "refresh_rate": "120 Hz",
        "processor": "MediaTek Dimensity 9400",
        "network": "5G",
        "os": "Android",
        "description": "OPPO Find X8 flagship smartphone."
    },

    # =========================================================
    # IQOO
    # =========================================================

    {
        "name": "iQOO 12 256GB",
        "brand": "iQOO",
        "price": 52999,
        "mrp": 59999,
        "rating": 4.6,
        "reviews": 6700,
        "storage": "256 GB",
        "ram": "12 GB",
        "camera": "50 MP",
        "front_camera": "16 MP",
        "battery": "5000 mAh",
        "display": "6.78 inch",
        "display_type": "AMOLED",
        "refresh_rate": "144 Hz",
        "processor": "Snapdragon 8 Gen 3",
        "network": "5G",
        "os": "Android",
        "description": "iQOO 12 flagship performance smartphone."
    },

    {
        "name": "iQOO Neo 9 Pro 128GB",
        "brand": "iQOO",
        "price": 32999,
        "mrp": 36999,
        "rating": 4.5,
        "reviews": 5400,
        "storage": "128 GB",
        "ram": "8 GB",
        "camera": "50 MP",
        "front_camera": "16 MP",
        "battery": "5160 mAh",
        "display": "6.78 inch",
        "display_type": "AMOLED",
        "refresh_rate": "144 Hz",
        "processor": "Snapdragon 8 Gen 2",
        "network": "5G",
        "os": "Android",
        "description": "iQOO Neo 9 Pro performance smartphone."
    },

    # =========================================================
    # POCO
    # =========================================================

    {
        "name": "POCO X6 Pro 256GB",
        "brand": "POCO",
        "price": 24999,
        "mrp": 29999,
        "rating": 4.4,
        "reviews": 12500,
        "storage": "256 GB",
        "ram": "8 GB",
        "camera": "64 MP",
        "front_camera": "16 MP",
        "battery": "5000 mAh",
        "display": "6.67 inch",
        "display_type": "AMOLED",
        "refresh_rate": "120 Hz",
        "processor": "MediaTek Dimensity 8300 Ultra",
        "network": "5G",
        "os": "Android",
        "description": "POCO X6 Pro performance smartphone."
    },

    {
        "name": "POCO F6 256GB",
        "brand": "POCO",
        "price": 29999,
        "mrp": 33999,
        "rating": 4.5,
        "reviews": 7400,
        "storage": "256 GB",
        "ram": "8 GB",
        "camera": "50 MP",
        "front_camera": "20 MP",
        "battery": "5000 mAh",
        "display": "6.67 inch",
        "display_type": "AMOLED",
        "refresh_rate": "120 Hz",
        "processor": "Snapdragon 8s Gen 3",
        "network": "5G",
        "os": "Android",
        "description": "POCO F6 performance smartphone."
    }
]


def table_columns(conn, table_name):
    rows = conn.execute(
        f'PRAGMA table_info("{table_name}")'
    ).fetchall()

    return {row[1] for row in rows}


def product_exists(conn, name, brand):
    row = conn.execute(
        """
        SELECT id
        FROM products
        WHERE LOWER(name) = LOWER(?)
          AND LOWER(COALESCE(brand, '')) = LOWER(?)
        LIMIT 1
        """,
        (name, brand)
    ).fetchone()

    return row is not None


def add_spec(conn, product_id, spec_name, spec_value):
    if spec_value is None:
        return

    spec_value = str(spec_value).strip()

    if not spec_value:
        return

    conn.execute(
        """
        INSERT OR IGNORE INTO product_specs
        (product_id, spec_name, spec_value)
        VALUES (?, ?, ?)
        """,
        (product_id, spec_name, spec_value)
    )


def main():

    print("=" * 60)
    print("SMARTCART AI - PRODUCT CATALOG IMPORT")
    print("=" * 60)

    if not os.path.exists(DATABASE):
        print("ERROR: smartcart.db nahi mili.")
        return

    conn = sqlite3.connect(DATABASE)
    conn.execute("PRAGMA foreign_keys = ON")

    # ---------------------------------------------------------
    # Create flexible specification table
    # ---------------------------------------------------------

    conn.execute(
        """
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
        """
    )

    conn.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_product_specs_product
        ON product_specs(product_id)
        """
    )

    conn.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_product_specs_name
        ON product_specs(spec_name)
        """
    )

    columns = table_columns(conn, "products")

    required_columns = [
        "platform",
        "mrp",
        "rating",
        "reviews",
        "lifespan_years",
        "energy_kwh",
        "review_text",
        "product_url",
        "updated_at",
        "image",
        "description",
        "stock",
    ]

    missing = [
        column
        for column in required_columns
        if column not in columns
    ]

    if missing:
        print("ERROR: products table mein columns missing hain:")
        print(missing)
        conn.close()
        return

    inserted = 0
    skipped = 0

    # ---------------------------------------------------------
    # Insert products
    # ---------------------------------------------------------

    for item in SMARTPHONES:

        name = item["name"]
        brand = item["brand"]

        if product_exists(conn, name, brand):
            print("SKIP:", name)
            skipped += 1
            continue

        cursor = conn.execute(
            """
            INSERT INTO products
            (
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
                name,
                "Electronics",
                brand,
                "Mobile",
                item["price"],
                item["mrp"],
                item["rating"],
                item["reviews"],
                4,
                0,
                "",
                "#",
                "",
                item["description"],
                25,
            )
        )

        product_id = cursor.lastrowid

        # -----------------------------------------------------
        # Add dynamic specifications
        # -----------------------------------------------------

        specs = {
            "Subcategory": "Smartphones",
            "RAM": item["ram"],
            "Storage": item["storage"],
            "Camera": item["camera"],
            "Front Camera": item["front_camera"],
            "Battery": item["battery"],
            "Display Size": item["display"],
            "Display Type": item["display_type"],
            "Refresh Rate": item["refresh_rate"],
            "Processor": item["processor"],
            "Network": item["network"],
            "Operating System": item["os"],
        }

        for spec_name, spec_value in specs.items():
            add_spec(
                conn,
                product_id,
                spec_name,
                spec_value
            )

        # -----------------------------------------------------
        # Price history
        # -----------------------------------------------------

        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS price_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER NOT NULL,
                price REAL NOT NULL,
                recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(product_id)
                    REFERENCES products(id)
                    ON DELETE CASCADE
            )
            """
        )

        conn.execute(
            """
            INSERT INTO price_history
            (product_id, price)
            VALUES (?, ?)
            """,
            (product_id, item["price"])
        )

        inserted += 1

        print(
            f"ADDED: {name} | "
            f"{brand} | "
            f"₹{item['price']:,}"
        )

    conn.commit()

    total_products = conn.execute(
        "SELECT COUNT(*) FROM products"
    ).fetchone()[0]

    total_specs = conn.execute(
        "SELECT COUNT(*) FROM product_specs"
    ).fetchone()[0]

    conn.close()

    print()
    print("=" * 60)
    print("IMPORT COMPLETE")
    print("=" * 60)
    print("New products :", inserted)
    print("Skipped       :", skipped)
    print("Total products:", total_products)
    print("Total specs   :", total_specs)
    print("=" * 60)


if __name__ == "__main__":
    main()