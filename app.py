import os
import re
import sqlite3
import secrets
import statistics
from functools import wraps
from datetime import datetime
 
from flask import (
    Flask, render_template, request, jsonify,
    redirect, url_for, session, flash, abort, Response
)
 
# =========================================================
# CONFIGURATION
# =========================================================
 
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, "smartcart.db")
 
 
def load_env_file(path):
    """Tiny .env loader (no extra package needed). Existing env vars win."""
    if not os.path.exists(path):
        return
 
    with open(path, encoding="utf-8-sig") as handle:
        for line in handle:
            line = line.strip()
 
            if not line or line.startswith("#") or "=" not in line:
                continue
 
            key, value = line.split("=", 1)
            os.environ.setdefault(
                key.strip(), value.strip().strip('"').strip("'")
            )
 
 
load_env_file(os.path.join(BASE_DIR, ".env"))
 
app = Flask(__name__)
app.secret_key = (
    os.environ.get("FLASK_SECRET_KEY")
    or os.environ.get("SMARTCART_SECRET_KEY")
    or "change-this-secret-before-production"
)
app.config["JSON_SORT_KEYS"] = False
 
PER_PAGE = 24
PLACEHOLDER = "/static/images/products/product-placeholder.svg"
 
# These hosts no longer serve images (loremflickr returns HTTP 401 and
# only gives random photos anyway), so we never send them to the browser.
BROKEN_IMAGE_HOSTS = ("loremflickr.com",)
 
# Local category pictures: static/images/products/<name>.svg
CATEGORY_IMAGES = [
    (("mobile", "phone", "smartphone"), "mobiles"),
    (("laptop", "computer"), "laptops"),
    (("audio", "headphone", "speaker", "earbud"), "audio"),
    (("camera",), "cameras"),
    (("gaming", "game", "console"), "gaming"),
    (("tv", "television", "home theatre"), "tv"),
    (("kitchen", "home", "appliance"), "home"),
    (("fashion", "cloth", "shirt", "shoe", "accessor", "wear"), "fashion"),
    (("skin", "beauty", "personal care", "daily"), "beauty"),
    (("book", "stationery"), "books"),
    (("electronic",), "electronics"),
]
 
try:
    from category_filters import (
        get_filters as dynamic_get_filters,
        get_category_data as dynamic_get_category_data,
    )
except Exception:
    dynamic_get_filters = None
    dynamic_get_category_data = None
 
 
# =========================================================
# DATABASE HELPERS
# =========================================================
 
def db():
    if not os.path.exists(DATABASE):
        raise FileNotFoundError(
            f"smartcart.db nahi mili: {DATABASE}"
        )
 
    conn = sqlite3.connect(DATABASE, timeout=30)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA busy_timeout=10000")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn
 
 
def table_exists(conn, name):
    return conn.execute(
        "SELECT 1 FROM sqlite_master WHERE type='table' AND name=?",
        (name,)
    ).fetchone() is not None
 
 
def columns(conn, table):
    if not table_exists(conn, table):
        return set()
 
    return {
        row["name"]
        for row in conn.execute(f'PRAGMA table_info("{table}")')
    }
 
 
def ensure_feature_tables():
    """Missing helper tables banaye; existing products ko touch nahi karta."""
    conn = db()
 
    statements = [
        """
        CREATE TABLE IF NOT EXISTS price_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL,
            price REAL NOT NULL,
            recorded_at TEXT DEFAULT CURRENT_TIMESTAMP,
            source TEXT DEFAULT 'SmartCart'
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS stores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            website TEXT
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS store_prices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL,
            store_id INTEGER,
            store_name TEXT,
            price REAL NOT NULL,
            product_url TEXT,
            checked_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS product_specs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL,
            spec_name TEXT NOT NULL,
            spec_value TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS product_attributes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL,
            attribute_name TEXT NOT NULL,
            attribute_value TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS product_images (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL,
            image_url TEXT NOT NULL,
            image_order INTEGER DEFAULT 0,
            colour TEXT,
            color TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """,
    ]
 
    try:
        for statement in statements:
            conn.execute(statement)
        conn.commit()
    finally:
        conn.close()
 
 
def safe_int(value, default=0):
    try:
        return int(value)
    except (TypeError, ValueError, OverflowError):
        return default
 
 
def safe_float(value, default=0.0):
    try:
        number = float(value)
        if number != number or abs(number) == float("inf"):
            return default
        return number
    except (TypeError, ValueError, OverflowError):
        return default
 
 
def clean(value):
    return str(value or "").strip()
 
 
def money(value):
    return f"₹{safe_float(value):,.0f}"
 
 
# =========================================================
# CATEGORIES AND PRODUCT COUNT
# =========================================================
 
def get_categories():
    conn = db()
 
    try:
        if "category" not in columns(conn, "products"):
            return []
 
        return [
            row["category"]
            for row in conn.execute("""
                SELECT DISTINCT category
                FROM products
                WHERE TRIM(COALESCE(category, '')) <> ''
                ORDER BY category
            """).fetchall()
        ]
    finally:
        conn.close()
 
 
def get_product_count():
    conn = db()
 
    try:
        if not table_exists(conn, "products"):
            return 0
 
        return conn.execute(
            "SELECT COUNT(*) FROM products"
        ).fetchone()[0]
    finally:
        conn.close()
 
 
# =========================================================
# PRODUCT IMAGES
# =========================================================
 
def category_placeholder(category):
    """Local picture for a category (always works, no internet needed)."""
    text = clean(category).lower()
 
    for words, filename in CATEGORY_IMAGES:
        if any(word in text for word in words):
            return f"/img/category/{filename}.svg"
 
    return PLACEHOLDER
 
 
def is_usable_image(url):
    url = clean(url)
 
    if url.startswith(("/static/", "/img/")):
        return True
 
    return (
        url.startswith(("https://", "http://"))
        and not any(host in url for host in BROKEN_IMAGE_HOSTS)
    )
 
 
def product_image(row):
    keys = row.keys()
    image = clean(row["image"]) if "image" in keys else ""
 
    if is_usable_image(image):
        return image
 
    category = row["category"] if "category" in keys else ""
    return category_placeholder(category)
 
 
def get_product_images(conn, product_id):
    images = []
 
    if not table_exists(conn, "product_images"):
        return images
 
    cols = columns(conn, "product_images")
 
    if not {"image_url", "product_id"}.issubset(cols):
        return images
 
    order_col = "image_order" if "image_order" in cols else (
        "id" if "id" in cols else "product_id"
    )
    id_order = ", id" if "id" in cols else ""
 
    try:
        rows = conn.execute(
            f"""
            SELECT image_url
            FROM product_images
            WHERE product_id=?
            ORDER BY "{order_col}"{id_order}
            LIMIT 6
            """,
            (product_id,)
        ).fetchall()
 
        for row in rows:
            image = clean(row["image_url"])
 
            if is_usable_image(image) and image not in images:
                images.append(image)
 
    except sqlite3.Error:
        app.logger.exception("Product images read karne mein error")
 
    return images
 
 
# =========================================================
# PRODUCT SPECIFICATIONS
# =========================================================
 
def get_specs(conn, product_ids):
    result = {product_id: {} for product_id in product_ids}
 
    if not product_ids:
        return result
 
    marks = ",".join("?" for _ in product_ids)
 
    tables = [
        ("product_specs", "spec_name", "spec_value"),
        ("product_attributes", "attribute_name", "attribute_value"),
    ]
 
    for table, name_col, value_col in tables:
        if not table_exists(conn, table):
            continue
 
        cols = columns(conn, table)
 
        if not {
            "product_id", name_col, value_col
        }.issubset(cols):
            continue
 
        order_clause = " ORDER BY id" if "id" in cols else ""
 
        try:
            rows = conn.execute(
                f"""
                SELECT product_id,
                       "{name_col}" AS spec_name,
                       "{value_col}" AS spec_value
                FROM "{table}"
                WHERE product_id IN ({marks})
                {order_clause}
                """,
                product_ids
            ).fetchall()
 
            for row in rows:
                name = clean(row["spec_name"])
                value = clean(row["spec_value"])
 
                if name and value:
                    result.setdefault(
                        row["product_id"], {}
                    )[name] = value
 
        except sqlite3.Error:
            app.logger.exception(
                "Specifications read karne mein error: %s",
                table
            )
 
    return result
 
 
def prepare_products(conn, rows):
    products = [dict(row) for row in rows]
    ids = [product["id"] for product in products if "id" in product]
    specs = get_specs(conn, ids)
 
    for product in products:
        product["price"] = safe_float(product.get("price"))
        product["mrp"] = safe_float(
            product.get("mrp"),
            product["price"]
        ) or product["price"]
 
        product["rating"] = safe_float(product.get("rating"))
        product["reviews"] = safe_int(product.get("reviews"))
        product["stock"] = safe_int(product.get("stock"), 1)
 
        mrp = product["mrp"]
        price = product["price"]
 
        product["discount"] = (
            round(max(0, (mrp - price) * 100 / mrp))
            if mrp > 0 else 0
        )
 
        product["image_url"] = product_image(product)
        # search/compare/deals/related templates read product.image
        product["image"] = product["image_url"]
        product["specs"] = specs.get(product.get("id"), {})
        product["attributes"] = product["specs"]
        product["url"] = product.get("product_url") or "#"
        product["formatted_price"] = money(price)
 
    return products
# =========================================================
# SEARCH, FILTERING AND SORTING
# =========================================================
 
def fetch_products(
    query="",
    category="",
    brand="",
    min_price=None,
    max_price=None,
    min_rating=None,
    sort="relevance",
    page=1,
    limit=PER_PAGE,
    extra_filters=None,
):
    conn = db()
 
    try:
        product_cols = columns(conn, "products")
 
        if not product_cols:
            return {
                "products": [],
                "total": 0,
                "page": 1,
                "per_page": limit,
                "pages": 1,
            }
 
        where = []
        args = []
 
        # Search across available product text columns.
        if query:
            searchable = [
                col for col in (
                    "name", "brand", "category", "description"
                )
                if col in product_cols
            ]
 
            for term in [
                term for term in re.split(r"\s+", query) if term
            ]:
                if searchable:
                    conditions = [
                        f'COALESCE("{col}", \'\') LIKE ?'
                        for col in searchable
                    ]
                    where.append("(" + " OR ".join(conditions) + ")")
                    args.extend([f"%{term}%"] * len(searchable))
 
        # Standard filters.
        for field, value, operator in [
            ("category", category, "="),
            ("brand", brand, "="),
            ("price", min_price, ">="),
            ("price", max_price, "<="),
            ("rating", min_rating, ">="),
        ]:
            if (
                value is not None
                and value != ""
                and field in product_cols
            ):
                where.append(f'"{field}" {operator} ?')
                args.append(value)
 
        # Dynamic category filters.
        reserved_fields = {
            "id", "name", "description", "image",
            "image_url", "product_url",
        }
 
        for key, values in (extra_filters or {}).items():
            if (
                key not in product_cols
                or key in reserved_fields
                or key in {
                    "category", "brand", "price", "rating"
                }
            ):
                continue
 
            if not isinstance(values, list):
                values = [values]
 
            values = [
                clean(value)
                for value in values
                if clean(value)
            ]
 
            if values:
                placeholders = ",".join("?" for _ in values)
                where.append(
                    f'CAST("{key}" AS TEXT) IN ({placeholders})'
                )
                args.extend(values)
 
        clause = (
            " WHERE " + " AND ".join(where)
            if where else ""
        )
 
        # Only fixed, trusted SQL order expressions are used.
        sort_options = {
            "price_asc": "price ASC",
            "price_desc": "price DESC",
            "rating": "rating DESC, reviews DESC",
            "discount": "(COALESCE(mrp, price)-price) DESC",
            "newest": "id DESC",
            "relevance": "rating DESC, reviews DESC",
        }
 
        if sort == "newest" and "updated_at" in product_cols:
            order = "updated_at DESC"
        else:
            order = sort_options.get(
                sort,
                "name COLLATE NOCASE ASC"
            )
 
        if (
            order.startswith("name")
            and "name" not in product_cols
        ):
            order = "id DESC" if "id" in product_cols else "rowid DESC"
 
        total = conn.execute(
            "SELECT COUNT(*) FROM products" + clause,
            args
        ).fetchone()[0]
 
        page = max(1, safe_int(page, 1))
        limit = min(100, max(1, safe_int(limit, PER_PAGE)))
 
        rows = conn.execute(
            "SELECT * FROM products"
            + clause
            + f" ORDER BY {order} LIMIT ? OFFSET ?",
            args + [limit, (page - 1) * limit]
        ).fetchall()
 
        return {
            "products": prepare_products(conn, rows),
            "total": total,
            "page": page,
            "per_page": limit,
            "pages": max(1, (total + limit - 1) // limit),
        }
 
    finally:
        conn.close()
 
 
def get_product(product_id):
    conn = db()
 
    try:
        row = conn.execute(
            "SELECT * FROM products WHERE id=?",
            (product_id,)
        ).fetchone()
 
        if not row:
            return None
 
        product = prepare_products(conn, [row])[0]
        images = get_product_images(conn, product_id)
 
        if (
            is_usable_image(product["image_url"])
            and not product["image_url"].endswith(".svg")
            and product["image_url"] not in images
        ):
            images.insert(0, product["image_url"])
 
        product["images"] = images or [product["image_url"]]
        return product
 
    finally:
        conn.close()
 
 
# =========================================================
# PRICE HISTORY AND STORE COMPARISON
# =========================================================
 
def get_price_history(product_id):
    conn = db()
 
    try:
        if not table_exists(conn, "price_history"):
            return []
 
        cols = columns(conn, "price_history")
 
        if not {"product_id", "price"}.issubset(cols):
            return []
 
        date_col = (
            "recorded_at"
            if "recorded_at" in cols
            else ("id" if "id" in cols else "product_id")
        )
 
        rows = conn.execute(
            f"""
            SELECT *
            FROM price_history
            WHERE product_id=?
            ORDER BY "{date_col}" ASC
            LIMIT 500
            """,
            (product_id,)
        ).fetchall()
 
        return [dict(row) for row in rows]
 
    finally:
        conn.close()
 
 
def get_store_prices(product_id):
    conn = db()
 
    try:
        if not table_exists(conn, "store_prices"):
            return []
 
        cols = columns(conn, "store_prices")
 
        if not {"product_id", "price"}.issubset(cols):
            return []
 
        rows = conn.execute(
            """
            SELECT *
            FROM store_prices
            WHERE product_id=?
            ORDER BY price ASC
            """,
            (product_id,)
        ).fetchall()
 
        return [dict(row) for row in rows]
 
    finally:
        conn.close()
 
 
def price_intelligence(product, history):
    prices = [
        safe_float(item.get("price"))
        for item in history
        if safe_float(item.get("price")) > 0
    ]
 
    if prices:
        low = min(prices)
        high = max(prices)
        average = round(statistics.mean(prices), 2)
    else:
        low = high = average = product["price"]
 
    if len(prices) < 3:
        suggestion = (
            "Historical data kam hai. "
            "Available store prices compare karein."
        )
        trend = "Not enough historical data"
 
    elif product["price"] < average:
        suggestion = "Current price recorded average se kam hai."
        trend = "Below historical average"
 
    else:
        suggestion = "Buy karne se pehle price track karein."
        trend = "Compare before buying"
 
    return {
        "history": history,
        "low": low,
        "high": high,
        "average": average,
        "trend": trend,
        "suggestion": suggestion,
        "forecast": [],
    }
 
 
# =========================================================
# DYNAMIC CATEGORY FILTERS
# =========================================================
 
def get_dynamic_filter_data(category="", subcategory=""):
    categories = get_categories()
 
    if dynamic_get_category_data and dynamic_get_filters:
        try:
            category_data = dynamic_get_category_data(
                main_category=category or None,
                subcategory=subcategory or None,
            )
 
            filters = dynamic_get_filters(
                main_category=category or None,
                subcategory=subcategory or None,
            )
 
            if filters:
                return category_data, filters
 
        except Exception:
            app.logger.exception("Dynamic filters fallback")
 
    conn = db()
 
    try:
        if "brand" not in columns(conn, "products"):
            brands = []
 
        elif category:
            rows = conn.execute(
                """
                SELECT DISTINCT brand
                FROM products
                WHERE category=?
                  AND COALESCE(brand, '') <> ''
                ORDER BY brand
                """,
                (category,)
            ).fetchall()
            brands = [row["brand"] for row in rows]
 
        else:
            rows = conn.execute("""
                SELECT DISTINCT brand
                FROM products
                WHERE COALESCE(brand, '') <> ''
                ORDER BY brand
            """).fetchall()
            brands = [row["brand"] for row in rows]
 
    finally:
        conn.close()
 
    category_data = {
        "categories": categories,
        "brands": brands,
        "subcategories": [],
    }
 
    filters = [{
        "key": "brand",
        "label": "Brand",
        "type": "checkbox",
        "options": brands,
    }]
 
    return category_data, filters
# =========================================================
# TEMPLATE GLOBALS AND AUTH DECORATOR
# =========================================================
 
def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get("user"):
            flash("Is feature ke liye pehle login karein.", "info")
            return redirect(url_for("auth"))
        return view(*args, **kwargs)
    return wrapped
 
 
@app.context_processor
def inject_globals():
    count = 0
 
    if os.path.exists(DATABASE):
        try:
            count = get_product_count()
        except Exception:
            app.logger.exception("Product count unavailable")
 
    return {
        "current_user": session.get("user"),
        "money": money,
        "product_count": count,
        "now": datetime.now(),
    }
 
 
# =========================================================
# HOME
# =========================================================
 
@app.route("/")
def index():
    popular = fetch_products(
        sort="rating", limit=8
    )["products"]
 
    newest = fetch_products(
        sort="newest", limit=12
    )["products"]
 
    all_deals = fetch_products(
        sort="discount", limit=40
    )["products"]
 
    deals = [
        product for product in all_deals
        if product["discount"] > 0
    ][:8]
 
    return render_template(
        "index.html",
        products=newest,
        featured_products=popular,
        deals=deals,
        categories=get_categories(),
        product_count=get_product_count(),
    )
 
 
# =========================================================
# SEARCH
# =========================================================
 
@app.route("/search")
def search():
    query = clean(request.args.get("q"))
    category = clean(request.args.get("category"))
    brand = clean(request.args.get("brand"))
    sort = clean(request.args.get("sort", "relevance"))
 
    min_price = request.args.get("min_price", type=float)
    max_price = request.args.get("max_price", type=float)
    rating = request.args.get("rating", type=float)
    page = request.args.get("page", 1, type=int)
 
    # Dynamic filters ke liye selected values hamesha define honge.
    selected_filter_values = {
        key: request.args.getlist(key)
        for key in request.args.keys()
    }
 
    # Standard parameters ko dynamic filters se alag rakho.
    reserved = {
        "q", "category", "brand", "sort",
        "min_price", "max_price", "rating",
        "page", "id", "ids",
    }
 
    extra_filters = {
        key: request.args.getlist(key)
        for key in request.args.keys()
        if key not in reserved
    }
 
    result = fetch_products(
        query=query,
        category=category,
        brand=brand,
        min_price=min_price,
        max_price=max_price,
        min_rating=rating,
        sort=sort,
        page=page,
        limit=PER_PAGE,
        extra_filters=extra_filters,
    )
 
    category_data, dynamic_filters = get_dynamic_filter_data(
        category
    )
 
    return render_template(
        "search.html",
        **result,
        query=query,
        q=query,
        category=category,
        selected_category=category,
        brand=brand,
        sort=sort,
        categories=get_categories(),
        category_data=category_data,
        dynamic_filters=dynamic_filters,
        filters=dynamic_filters,
        selected_filter_values=selected_filter_values,
        min_price=min_price,
        max_price=max_price,
        rating=rating,
    )
 
 
# =========================================================
# PRODUCT DETAIL
# =========================================================
 
@app.route("/product/<int:product_id>")
def product_detail(product_id):
    product = get_product(product_id)
 
    if not product:
        abort(404)
 
    related = fetch_products(
        category=product.get("category", ""),
        sort="rating",
        limit=8,
    )["products"]
 
    related = [
        item for item in related
        if item["id"] != product_id
    ][:6]
 
    history = get_price_history(product_id)
    intelligence = price_intelligence(product, history)
    store_prices = get_store_prices(product_id)
 
    return render_template(
        "product_detail.html",
        product=product,
        related_products=related,
        related=related,
        history=history,
        price_history=history,
        store_prices=store_prices,
        stores=store_prices,
        intelligence=intelligence,
        price_intelligence=intelligence,
        specs=product.get("specs", {}),
    )
 
 
# =========================================================
# COMPARE 2–4 PRODUCTS
# =========================================================
 
def requested_product_ids():
    raw_ids = (
        request.args.getlist("id")
        + clean(request.args.get("ids")).split(",")
    )
 
    ids = []
 
    for raw in raw_ids:
        product_id = safe_int(raw)
 
        if product_id > 0 and product_id not in ids:
            ids.append(product_id)
 
    return ids[:4]
 
 
@app.route("/compare")
def compare():
    ids = requested_product_ids()
 
    products = [
        product
        for product in (get_product(pid) for pid in ids)
        if product
    ]
 
    return render_template(
        "compare.html",
        products=products,
        categories=get_categories(),
    )
 
 
@app.route("/add-to-compare/<int:product_id>")
def add_to_compare(product_id):
    if not get_product(product_id):
        abort(404)
 
    ids = requested_product_ids()
 
    if product_id not in ids:
        ids.append(product_id)
 
    return redirect(
        url_for("compare", id=ids[:4])
    )
 
 
# =========================================================
# DEALS
# =========================================================
 
@app.route("/deals")
def deals():
    category = clean(request.args.get("category"))
    page = request.args.get("page", 1, type=int)
 
    result = fetch_products(
        category=category,
        sort="discount",
        page=page,
        limit=PER_PAGE,
    )
 
    products = [
        product for product in result["products"]
        if product["discount"] > 0
    ]
 
    return render_template(
        "deals.html",
        products=products,
        deals=products,
        categories=get_categories(),
        category=category,
        total=result["total"],
        page=result["page"],
        pages=result["pages"],
        per_page=result["per_page"],
    )
 
 
# =========================================================
# ABOUT
# =========================================================
 
@app.route("/about")
def about():
    count = get_product_count()
 
    conn = db()
    try:
        category_count = conn.execute(
            "SELECT COUNT(DISTINCT category) FROM products"
        ).fetchone()[0]
    finally:
        conn.close()
 
    return render_template(
        "about.html",
        product_count=count,
        category_count=category_count,
    )
 
 
# =========================================================
# DEMO OTP AUTHENTICATION
# OTP terminal par print hota hai; SMS/email send nahi hota.
# =========================================================
 
@app.route("/auth", methods=["GET", "POST"])
def auth():
    if request.method == "POST":
        phone = clean(request.form.get("phone"))
        email = clean(request.form.get("email"))
        identity = phone or email
 
        if not identity:
            flash("Phone ya email enter karein.", "warning")
            return render_template("auth.html")
 
        otp = f"{secrets.randbelow(1000000):06d}"
 
        session["otp"] = otp
        session["auth_phone"] = phone
        session["auth_email"] = email
 
        app.logger.warning(
            "SMARTCART DEMO OTP for %s: %s",
            identity,
            otp,
        )
 
        print(f"\nSMARTCART DEMO OTP for {identity}: {otp}\n")
 
        flash(
            "Demo OTP terminal mein print hua hai. SMS/email send nahi hua.",
            "info",
        )
 
        return render_template(
            "auth.html",
            otp_sent=True,
            phone=phone,
            email=email,
        )
 
    return render_template("auth.html")
 
 
@app.route("/verify-otp", methods=["POST"])
def verify_otp():
    entered = clean(request.form.get("otp"))
    saved = session.get("otp")
 
    if not saved or entered != saved:
        flash("OTP missing ya galat hai.", "danger")
        return redirect(url_for("auth"))
 
    session["user"] = (
        session.get("auth_phone")
        or session.get("auth_email")
        or "SmartCart User"
    )
 
    session.pop("otp", None)
 
    flash("Demo login successful.", "success")
    return redirect(url_for("index"))
 
 
@app.route("/logout")
def logout():
    for key in (
        "user", "otp", "auth_phone", "auth_email"
    ):
        session.pop(key, None)
 
    flash("Aap logout ho gaye hain.", "success")
    return redirect(url_for("index"))
# =========================================================
# JSON API: CATEGORIES
# =========================================================
 
@app.route("/api/categories")
def api_categories():
    return jsonify(
        success=True,
        categories=get_categories(),
    )
 
 
# =========================================================
# JSON API: FILTERS
# =========================================================
 
@app.route("/api/filters")
def api_filters():
    category = clean(request.args.get("category"))
    subcategory = clean(request.args.get("subcategory"))
 
    category_data, filters = get_dynamic_filter_data(
        category,
        subcategory,
    )
 
    return jsonify(
        success=True,
        category_data=category_data,
        filters=filters,
    )
 
 
# =========================================================
# JSON API: PRODUCTS
# =========================================================
 
@app.route("/api/products")
def api_products():
    limit = min(
        100,
        max(1, request.args.get("limit", 24, type=int)),
    )
 
    result = fetch_products(
        query=clean(request.args.get("q")),
        category=clean(request.args.get("category")),
        brand=clean(request.args.get("brand")),
        min_price=request.args.get("min_price", type=float),
        max_price=request.args.get("max_price", type=float),
        min_rating=request.args.get("rating", type=float),
        sort=clean(request.args.get("sort", "relevance")),
        page=request.args.get("page", 1, type=int),
        limit=limit,
    )
 
    return jsonify(success=True, **result)
 
 
# =========================================================
# JSON API: ONE PRODUCT
# =========================================================
 
@app.route("/api/product/<int:product_id>")
def api_product(product_id):
    product = get_product(product_id)
 
    if not product:
        return jsonify(
            success=False,
            message="Product not found",
        ), 404
 
    return jsonify(
        success=True,
        product=product,
    )
 
 
# =========================================================
# JSON API: PRODUCT IMAGES
# =========================================================
 
@app.route("/api/products/<int:product_id>/images")
def api_images(product_id):
    product = get_product(product_id)
 
    if not product:
        return jsonify(
            success=False,
            images=[],
        ), 404
 
    return jsonify(
        success=True,
        product_id=product_id,
        images=product["images"],
    )
 
 
# =========================================================
# JSON API: PRICE HISTORY
# =========================================================
 
@app.route("/api/products/<int:product_id>/history")
def api_history(product_id):
    product = get_product(product_id)
 
    if not product:
        return jsonify(
            success=False,
            message="Product not found",
        ), 404
 
    return jsonify(
        success=True,
        product_id=product_id,
        history=get_price_history(product_id),
    )
 
 
# =========================================================
# JSON API: STORE PRICES
# =========================================================
 
@app.route("/api/products/<int:product_id>/stores")
def api_stores(product_id):
    product = get_product(product_id)
 
    if not product:
        return jsonify(
            success=False,
            stores=[],
        ), 404
 
    return jsonify(
        success=True,
        product_id=product_id,
        stores=get_store_prices(product_id),
    )
 
 
# =========================================================
# JSON API: PRICE INSIGHTS / FORECAST
# =========================================================
 
@app.route("/api/products/<int:product_id>/forecast")
def api_forecast(product_id):
    product = get_product(product_id)
 
    if not product:
        return jsonify(
            success=False,
            message="Product not found",
        ), 404
 
    history = get_price_history(product_id)
    insights = price_intelligence(product, history)
 
    return jsonify(
        success=True,
        product_id=product_id,
        current_price=product["price"],
        history=insights["history"],
        low=insights["low"],
        high=insights["high"],
        average=insights["average"],
        trend=insights["trend"],
        suggestion=insights["suggestion"],
        forecast=insights["forecast"],
    )
 
 
# =========================================================
# JSON API: PRODUCT COMPARISON
# =========================================================
 
@app.route("/api/compare")
def api_compare():
    ids = requested_product_ids()
 
    products = [
        product
        for product in (get_product(pid) for pid in ids)
        if product
    ]
 
    return jsonify(
        success=True,
        products=products,
    )
 
 
# =========================================================
# HEALTH CHECK
# =========================================================
 
@app.route("/health")
def health():
    conn = None
 
    try:
        conn = db()
 
        count = conn.execute(
            "SELECT COUNT(*) FROM products"
        ).fetchone()[0]
 
        integrity = conn.execute(
            "PRAGMA integrity_check"
        ).fetchone()[0]
 
        return jsonify(
            status="ok" if integrity == "ok" else "warning",
            database_exists=True,
            products=count,
            integrity=integrity,
        )
 
    except Exception as exc:
        app.logger.exception("Health check failed")
 
        return jsonify(
            status="error",
            error=str(exc),
        ), 500
 
    finally:
        if conn is not None:
            conn.close()
 
 
# =========================================================
# ERROR HANDLERS
# =========================================================
 
@app.errorhandler(404)
def not_found(error):
    try:
        return render_template("404.html"), 404
    except Exception:
        return "Page not found", 404
 
 
@app.errorhandler(500)
def server_error(error):
    app.logger.exception("Unhandled server error")
 
    try:
        return render_template("500.html"), 500
    except Exception:
        return (
            "Internal server error. VS Code terminal check karein.",
            500,
        )
 
 
# =========================================================
# START APP
# =========================================================
 
# =====================================================================
# BUILT-IN PICTURES (category pictures + ad banners)
# Created by the app itself, so no image files need to be copied.
# =====================================================================
 
CATEGORY_ART = {
    "mobiles": ("#e0e7ff", "#c7d2fe", "#4f46e5", "Mobiles",
        '<rect x="165" y="55" width="70" height="130" rx="12" fill="#fff" stroke="{a}" stroke-width="6"/><circle cx="200" cy="168" r="6" fill="{a}"/><rect x="185" y="66" width="30" height="5" rx="2.5" fill="{a}"/>'),
    "laptops": ("#dbeafe", "#bfdbfe", "#2563eb", "Laptops",
        '<rect x="140" y="70" width="120" height="78" rx="8" fill="#fff" stroke="{a}" stroke-width="6"/><path d="M120 160h160l-12 18H132z" fill="{a}"/>'),
    "audio": ("#fce7f3", "#fbcfe8", "#db2777", "Audio",
        '<path d="M150 150v-20a50 50 0 0 1 100 0v20" fill="none" stroke="{a}" stroke-width="10" stroke-linecap="round"/><rect x="138" y="136" width="26" height="48" rx="10" fill="{a}"/><rect x="236" y="136" width="26" height="48" rx="10" fill="{a}"/>'),
    "cameras": ("#ede9fe", "#ddd6fe", "#7c3aed", "Cameras",
        '<rect x="130" y="85" width="140" height="90" rx="14" fill="#fff" stroke="{a}" stroke-width="6"/><rect x="170" y="72" width="40" height="18" rx="5" fill="{a}"/><circle cx="200" cy="130" r="26" fill="none" stroke="{a}" stroke-width="7"/><circle cx="200" cy="130" r="9" fill="{a}"/>'),
    "gaming": ("#dcfce7", "#bbf7d0", "#16a34a", "Gaming",
        '<rect x="125" y="95" width="150" height="80" rx="38" fill="#fff" stroke="{a}" stroke-width="6"/><path d="M160 120v30M145 135h30" stroke="{a}" stroke-width="7" stroke-linecap="round"/><circle cx="238" cy="126" r="7" fill="{a}"/><circle cx="256" cy="144" r="7" fill="{a}"/>'),
    "tv": ("#cffafe", "#a5f3fc", "#0891b2", "TV &amp; Home",
        '<rect x="120" y="78" width="160" height="96" rx="10" fill="#fff" stroke="{a}" stroke-width="6"/><path d="M170 190h60" stroke="{a}" stroke-width="8" stroke-linecap="round"/>'),
    "home": ("#ffedd5", "#fed7aa", "#ea580c", "Home &amp; Kitchen",
        '<path d="M135 110h130v50a22 22 0 0 1-22 22H157a22 22 0 0 1-22-22z" fill="#fff" stroke="{a}" stroke-width="6"/><path d="M265 125h14a14 14 0 0 1 0 28h-14" fill="none" stroke="{a}" stroke-width="6"/>'),
    "fashion": ("#fef3c7", "#fde68a", "#d97706", "Fashion",
        '<path d="M165 70l-45 25 18 32 22-10v68h80v-68l22 10 18-32-45-25q-15 18-35 0-20 18-35 0z" fill="#fff" stroke="{a}" stroke-width="6" stroke-linejoin="round"/>'),
    "beauty": ("#ffe4e6", "#fecdd3", "#e11d48", "Personal Care",
        '<rect x="178" y="62" width="44" height="26" rx="6" fill="{a}"/><rect x="165" y="88" width="70" height="100" rx="16" fill="#fff" stroke="{a}" stroke-width="6"/><circle cx="200" cy="138" r="16" fill="none" stroke="{a}" stroke-width="5"/>'),
    "books": ("#f1f5f9", "#e2e8f0", "#475569", "Books",
        '<path d="M130 80h62v110h-62zM208 80h62v110h-62z" fill="#fff" stroke="{a}" stroke-width="6" stroke-linejoin="round"/><path d="M145 105h32M145 125h32M223 105h32M223 125h32" stroke="{a}" stroke-width="5" stroke-linecap="round"/>'),
    "electronics": ("#e0f2fe", "#bae6fd", "#0284c7", "Electronics",
        '<rect x="150" y="75" width="100" height="100" rx="14" fill="#fff" stroke="{a}" stroke-width="6"/><rect x="178" y="103" width="44" height="44" rx="6" fill="{a}"/>'),
}
 
BANNER_ART = {
    "mobiles": ("#312e81", "#6366f1", "#fde68a", "MEGA MOBILE FEST",
        "Up to 40% OFF on top smartphones", "Shop Mobiles",
        '<rect x="880" y="50" width="120" height="240" rx="22" fill="#fff" opacity=".95"/><rect x="892" y="66" width="96" height="190" rx="10" fill="#c7d2fe"/><circle cx="940" cy="274" r="7" fill="#6366f1"/><rect x="1010" y="90" width="110" height="200" rx="20" fill="#fff" opacity=".6"/>'),
    "laptops": ("#0f172a", "#2563eb", "#7dd3fc", "LAPTOP &amp; GAMING DEALS",
        "Work hard, play harder - best prices today", "Shop Laptops",
        '<rect x="840" y="80" width="260" height="160" rx="12" fill="#fff" opacity=".95"/><rect x="856" y="96" width="228" height="128" rx="6" fill="#bfdbfe"/><path d="M810 248h320l-24 30H834z" fill="#e2e8f0"/>'),
    "fashion": ("#9f1239", "#f43f5e", "#fef3c7", "FASHION SALE",
        "Minimum 50% OFF on styles you love", "Shop Fashion",
        '<path d="M930 60l-80 45 32 58 40-18v125h140V145l40 18 32-58-80-45q-28 32-62 0-34 32-62 0z" transform="translate(-20 0) scale(.95)" fill="#fff" opacity=".95"/>'),
    "home": ("#7c2d12", "#f97316", "#ffedd5", "HOME &amp; KITCHEN",
        "Smart appliances for a smarter home", "Shop Deals",
        '<path d="M860 130h240v80a40 40 0 0 1-40 40H900a40 40 0 0 1-40-40z" fill="#fff" opacity=".95"/><path d="M1100 150h26a26 26 0 0 1 0 52h-26" fill="none" stroke="#fff" stroke-width="12" opacity=".95"/><path d="M910 105c-10-18 10-26 0-44M980 105c-10-18 10-26 0-44M1050 105c-10-18 10-26 0-44" fill="none" stroke="#fff" stroke-width="9" stroke-linecap="round" opacity=".8"/>'),
}
 
 
def svg_response(svg):
    return Response(
        svg,
        mimetype="image/svg+xml",
        headers={"Cache-Control": "public, max-age=86400"}
    )
 
 
@app.route("/img/category/<name>.svg")
def category_image(name):
    data = CATEGORY_ART.get(name) or CATEGORY_ART["electronics"]
    b1, b2, a, label, icon = data
 
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300" width="400" height="300" role="img" aria-label="{label}">
  <defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{b1}"/><stop offset="1" stop-color="{b2}"/></linearGradient></defs>
  <rect width="400" height="300" rx="20" fill="url(#g)"/>
  {icon.format(a=a)}
  <text x="200" y="246" text-anchor="middle" font-family="Arial,sans-serif" font-size="20" font-weight="700" fill="{a}">{label}</text>
  <text x="200" y="268" text-anchor="middle" font-family="Arial,sans-serif" font-size="11" fill="#64748b">SmartCart AI</text>
</svg>"""
 
    return svg_response(svg)
 
 
@app.route("/img/banner/<name>.svg")
def banner_image(name):
    data = BANNER_ART.get(name)
 
    if not data:
        abort(404)
 
    c1, c2, hl, title, sub, btn, art = data
 
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 340" width="1200" height="340" role="img" aria-label="{title}">
  <defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{c1}"/><stop offset="1" stop-color="{c2}"/></linearGradient></defs>
  <rect width="1200" height="340" fill="url(#g)"/>
  <circle cx="1080" cy="40" r="170" fill="#fff" opacity=".07"/><circle cx="780" cy="330" r="130" fill="#fff" opacity=".06"/>
  {art}
  <text x="70" y="130" font-family="Arial,Helvetica,sans-serif" font-size="54" font-weight="800" fill="#fff">{title}</text>
  <text x="70" y="180" font-family="Arial,Helvetica,sans-serif" font-size="26" fill="{hl}">{sub}</text>
  <rect x="70" y="212" width="190" height="52" rx="26" fill="{hl}"/>
  <text x="165" y="246" text-anchor="middle" font-family="Arial,Helvetica,sans-serif" font-size="20" font-weight="700" fill="{c1}">{btn}</text>
</svg>"""
 
    return svg_response(svg)
 
 
if __name__ == "__main__":
    if not os.path.exists(DATABASE):
        raise SystemExit(
            f"ERROR: smartcart.db nahi mili: {DATABASE}"
        )
 
    ensure_feature_tables()
 
    conn = db()
 
    try:
        count = conn.execute(
            "SELECT COUNT(*) FROM products"
        ).fetchone()[0]
 
        integrity = conn.execute(
            "PRAGMA integrity_check"
        ).fetchone()[0]
    finally:
        conn.close()
 
    print("\n" + "=" * 52)
    print(" SMARTCART AI")
    print("=" * 52)
    print(f"Database: {DATABASE}")
    print(f"Products: {count}")
    print(f"Integrity: {integrity}")
    print("Open: http://127.0.0.1:5000")
    print("=" * 52 + "\n")
 
    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000,
    )
