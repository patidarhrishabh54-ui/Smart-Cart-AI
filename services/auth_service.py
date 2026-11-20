
import os
import sqlite3
import secrets
import hashlib
import hmac
import time
import re
from pathlib import Path


# ==========================================================
# SMARTCART AI - AUTHENTICATION SERVICE
# Email OTP, SMS OTP, Google account linking
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATABASE_PATH = Path(
    os.getenv(
        "DATABASE_PATH",
        str(BASE_DIR / "smartcart.db")
    )
)

OTP_EXPIRY_SECONDS = int(
    os.getenv("OTP_EXPIRY_MINUTES", "5")
) * 60

OTP_RESEND_SECONDS = int(
    os.getenv("OTP_RESEND_SECONDS", "60")
)

MAX_OTP_ATTEMPTS = 5


# ==========================================================
# DATABASE CONNECTION
# ==========================================================

def get_auth_db():
    """
    Connect to the existing SmartCart database.

    Does not delete or modify existing product data.
    """

    connection = sqlite3.connect(
        str(DATABASE_PATH),
        timeout=30
    )

    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    connection.execute("PRAGMA busy_timeout = 30000")

    return connection


# ==========================================================
# INITIALIZE AUTH TABLES
# ==========================================================

def init_auth_db():
    """
    Create authentication tables if they do not exist.
    Existing product tables are left untouched.
    """

    with get_auth_db() as conn:

        conn.execute("""
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE COLLATE NOCASE,
                phone TEXT UNIQUE,
                full_name TEXT,
                google_sub TEXT UNIQUE,
                email_verified INTEGER NOT NULL DEFAULT 0,
                phone_verified INTEGER NOT NULL DEFAULT 0,
                created_at INTEGER NOT NULL,
                updated_at INTEGER NOT NULL
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS auth_otps (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                identifier TEXT NOT NULL,
                channel TEXT NOT NULL,
                otp_hash TEXT NOT NULL,
                expires_at INTEGER NOT NULL,
                attempts INTEGER NOT NULL DEFAULT 0,
                created_at INTEGER NOT NULL,
                verified_at INTEGER
            )
        """)

        conn.execute("""
            CREATE INDEX IF NOT EXISTS
            idx_auth_otps_identifier
            ON auth_otps(identifier, channel)
        """)

        conn.execute("""
            CREATE INDEX IF NOT EXISTS
            idx_auth_otps_expiry
            ON auth_otps(expires_at)
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS customer_addresses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id INTEGER NOT NULL,
                full_name TEXT NOT NULL,
                phone TEXT NOT NULL,
                address_line1 TEXT NOT NULL,
                address_line2 TEXT,
                city TEXT NOT NULL,
                state TEXT NOT NULL,
                postal_code TEXT NOT NULL,
                country TEXT NOT NULL DEFAULT 'India',
                is_default INTEGER NOT NULL DEFAULT 0,
                created_at INTEGER NOT NULL,
                FOREIGN KEY(customer_id)
                    REFERENCES customers(id)
                    ON DELETE CASCADE
            )
        """)

        conn.commit()


# ==========================================================
# INPUT NORMALIZATION
# ==========================================================

def normalize_email(email):
    if not isinstance(email, str):
        return None

    email = email.strip().lower()

    if len(email) > 254:
        return None

    if not re.fullmatch(
        r"[^@\s]+@[^@\s]+\.[^@\s]+",
        email
    ):
        return None

    return email


def normalize_phone(phone):
    if not isinstance(phone, str):
        return None

    phone = re.sub(
        r"[\s()-]",
        "",
        phone.strip()
    )

    if not re.fullmatch(r"\+?[1-9]\d{7,14}", phone):
        return None

    return phone


def normalize_identifier(identifier, channel):
    if channel == "email":
        return normalize_email(identifier)

    if channel == "sms":
        return normalize_phone(identifier)

    return None


# ==========================================================
# OTP SECRET AND HASHING
# ==========================================================

def _get_otp_secret():
    """
    Requires a strong secret in FLASK_SECRET_KEY.
    """

    secret = os.getenv("FLASK_SECRET_KEY", "")

    if len(secret) < 32:
        raise RuntimeError(
            "Set a strong FLASK_SECRET_KEY in your .env file."
        )

    return secret.encode("utf-8")


def _hash_otp(identifier, channel, otp):
    message = (
        f"{channel}:{identifier}:{otp}"
    ).encode("utf-8")

    return hmac.new(
        _get_otp_secret(),
        message,
        hashlib.sha256
    ).hexdigest()


# ==========================================================
# CREATE OTP
# ==========================================================

def create_otp(identifier, channel):
    """
    Generate and store an OTP.

    The plaintext OTP is returned only to the trusted
    backend delivery function. Never send it to the browser.

    Returns:
        {
            "success": True,
            "otp": "...",
            "expires_in": 300
        }
    """

    if channel not in ("email", "sms"):
        return {
            "success": False,
            "message": "Invalid OTP channel."
        }

    identifier = normalize_identifier(
        identifier, channel
    )

    if not identifier:
        return {
            "success": False,
            "message": "Invalid email address or phone number."
        }

    try:
        _get_otp_secret()
    except RuntimeError:
        return {
            "success": False,
            "message": "Authentication is not configured."
        }

    now = int(time.time())

    otp = f"{secrets.randbelow(1000000):06d}"

    try:
        otp_hash = _hash_otp(
            identifier, channel, otp
        )
    except RuntimeError:
        return {
            "success": False,
            "message": "Authentication is not configured."
        }

    try:
        with get_auth_db() as conn:

            # Enforce resend cooldown.
            recent = conn.execute("""
                SELECT created_at
                FROM auth_otps
                WHERE identifier = ?
                  AND channel = ?
                ORDER BY id DESC
                LIMIT 1
            """, (
                identifier,
                channel
            )).fetchone()

            if recent:
                elapsed = now - recent["created_at"]

                if elapsed < OTP_RESEND_SECONDS:
                    return {
                        "success": False,
                        "message": (
                            "Please wait before requesting "
                            "another OTP."
                        ),
                        "retry_after": (
                            OTP_RESEND_SECONDS - elapsed
                        )
                    }

            # Invalidate previous pending codes.
            conn.execute("""
                UPDATE auth_otps
                SET verified_at = ?
                WHERE identifier = ?
                  AND channel = ?
                  AND verified_at IS NULL
            """, (
                now,
                identifier,
                channel
            ))

            conn.execute("""
                INSERT INTO auth_otps (
                    identifier,
                    channel,
                    otp_hash,
                    expires_at,
                    attempts,
                    created_at
                )
                VALUES (?, ?, ?, ?, 0, ?)
            """, (
                identifier,
                channel,
                otp_hash,
                now + OTP_EXPIRY_SECONDS,
                now
            ))

            conn.commit()

        return {
            "success": True,
            "otp": otp,
            "expires_in": OTP_EXPIRY_SECONDS
        }

    except sqlite3.Error:
        return {
            "success": False,
            "message": "Unable to create OTP."
        }


# ==========================================================
# INVALIDATE OTP
# ==========================================================

def invalidate_otp(identifier, channel):
    """
    Invalidate the latest pending OTP.

    Call this if the email/SMS provider fails to deliver
    the OTP, so an undelivered code cannot be used later.
    """

    identifier = normalize_identifier(
        identifier, channel
    )

    if not identifier:
        return False

    now = int(time.time())

    try:
        with get_auth_db() as conn:

            cursor = conn.execute("""
                UPDATE auth_otps
                SET verified_at = ?
                WHERE id = (
                    SELECT id
                    FROM auth_otps
                    WHERE identifier = ?
                      AND channel = ?
                      AND verified_at IS NULL
                    ORDER BY id DESC
                    LIMIT 1
                )
            """, (
                now,
                identifier,
                channel
            ))

            conn.commit()

            return cursor.rowcount > 0

    except sqlite3.Error:
        return False


# ==========================================================
# VERIFY OTP
# ==========================================================

def verify_otp(identifier, channel, otp):
    """
    Verify the latest unexpired OTP.

    Returns True only when the OTP is valid.
    """

    if channel not in ("email", "sms"):
        return False

    identifier = normalize_identifier(
        identifier, channel
    )

    if not identifier or otp is None:
        return False

    otp = str(otp).strip()

    if not re.fullmatch(r"\d{6}", otp):
        return False

    now = int(time.time())

    try:
        entered_hash = _hash_otp(
            identifier,
            channel,
            otp
        )
    except RuntimeError:
        return False

    try:
        with get_auth_db() as conn:

            record = conn.execute("""
                SELECT *
                FROM auth_otps
                WHERE identifier = ?
                  AND channel = ?
                  AND verified_at IS NULL
                ORDER BY id DESC
                LIMIT 1
            """, (
                identifier,
                channel
            )).fetchone()

            if not record:
                return False

            if record["expires_at"] <= now:
                return False

            if record["attempts"] >= MAX_OTP_ATTEMPTS:
                return False

            if not hmac.compare_digest(
                entered_hash,
                record["otp_hash"]
            ):
                conn.execute("""
                    UPDATE auth_otps
                    SET attempts = attempts + 1
                    WHERE id = ?
                """, (record["id"],))

                conn.commit()
                return False

            conn.execute("""
                UPDATE auth_otps
                SET verified_at = ?
                WHERE id = ?
            """, (
                now,
                record["id"]
            ))

            conn.commit()

            return True

    except sqlite3.Error:
        return False


# ==========================================================
# CREATE OR FIND CUSTOMER
# ==========================================================

def get_or_create_customer(
    email=None,
    phone=None,
    full_name=None
):
    """
    Find or create a customer.

    This function does not automatically link an email
    account to a phone account. Account linking requires
    a separate verified flow.
    """

    email = normalize_email(email) if email else None
    phone = normalize_phone(phone) if phone else None

    if full_name:
        if not isinstance(full_name, str):
            full_name = None
        else:
            full_name = full_name.strip()[:150] or None

    if not email and not phone:
        return None

    now = int(time.time())

    try:
        with get_auth_db() as conn:

            customer = None

            if email:
                customer = conn.execute("""
                    SELECT *
                    FROM customers
                    WHERE email = ?
                """, (email,)).fetchone()

            if not customer and phone:
                customer = conn.execute("""
                    SELECT *
                    FROM customers
                    WHERE phone = ?
                """, (phone,)).fetchone()

            if customer:
                # Update name only if a name was provided
                # and the stored name is currently empty.
                if (
                    full_name
                    and not customer["full_name"]
                ):
                    conn.execute("""
                        UPDATE customers
                        SET full_name = ?,
                            updated_at = ?
                        WHERE id = ?
                    """, (
                        full_name,
                        now,
                        customer["id"]
                    ))

                    conn.commit()

                    customer = conn.execute("""
                        SELECT *
                        FROM customers
                        WHERE id = ?
                    """, (
                        customer["id"],
                    )).fetchone()

                return dict(customer)

            cursor = conn.execute("""
                INSERT INTO customers (
                    email,
                    phone,
                    full_name,
                    created_at,
                    updated_at
                )
                VALUES (?, ?, ?, ?, ?)
            """, (
                email,
                phone,
                full_name,
                now,
                now
            ))

            conn.commit()

            new_customer = conn.execute("""
                SELECT *
                FROM customers
                WHERE id = ?
            """, (
                cursor.lastrowid,
            )).fetchone()

            return dict(new_customer)

    except sqlite3.IntegrityError:
        # A concurrent request may have created the account.
        try:
            with get_auth_db() as conn:
                customer = None

                if email:
                    customer = conn.execute("""
                        SELECT *
                        FROM customers
                        WHERE email = ?
                    """, (email,)).fetchone()

                if not customer and phone:
                    customer = conn.execute("""
                        SELECT *
                        FROM customers
                        WHERE phone = ?
                    """, (phone,)).fetchone()

                return dict(customer) if customer else None

        except sqlite3.Error:
            return None

    except sqlite3.Error:
        return None


# ==========================================================
# MARK CUSTOMER VERIFIED
# ==========================================================

def mark_customer_verified(customer_id, channel):
    """
    Mark a customer's email or phone as verified.

    The channel determines the only column updated.
    """

    if channel not in ("email", "sms"):
        return False

    if channel == "email":
        column = "email_verified"
    else:
        column = "phone_verified"

    now = int(time.time())

    try:
        with get_auth_db() as conn:

            cursor = conn.execute(
                f"""
                UPDATE customers
                SET {column} = 1,
                    updated_at = ?
                WHERE id = ?
                """,
                (
                    now,
                    customer_id
                )
            )

            conn.commit()

            return cursor.rowcount == 1

    except sqlite3.Error:
        return False


# ==========================================================
# GET CUSTOMER
# ==========================================================

def get_customer_by_id(customer_id):
    """
    Fetch a customer by database ID.
    """

    try:
        with get_auth_db() as conn:

            customer = conn.execute("""
                SELECT *
                FROM customers
                WHERE id = ?
            """, (
                customer_id,
            )).fetchone()

            return dict(customer) if customer else None

    except (sqlite3.Error, TypeError, ValueError):
        return None


# ==========================================================
# GOOGLE SIGN-IN CUSTOMER LINKING
# ==========================================================

def get_or_create_google_customer(
    google_sub,
    email,
    full_name=None
):
    """
    Create or find a Google customer.

    IMPORTANT:
    The Google ID token must be verified by the
    Google authentication layer before calling this.

    Existing email accounts are not automatically linked.
    """

    if not google_sub or not email:
        return None

    google_sub = str(google_sub).strip()

    email = normalize_email(email)

    if not email or not google_sub:
        return None

    if len(google_sub) > 255:
        return None

    if full_name:
        if not isinstance(full_name, str):
            full_name = None
        else:
            full_name = full_name.strip()[:150] or None

    now = int(time.time())

    try:
        with get_auth_db() as conn:

            # Existing Google account.
            customer = conn.execute("""
                SELECT *
                FROM customers
                WHERE google_sub = ?
            """, (
                google_sub,
            )).fetchone()

            if customer:
                # Do not silently change an account's
                # email based on an untrusted value.
                return dict(customer)

            # Do not automatically link an existing
            # email account to Google.
            existing = conn.execute("""
                SELECT *
                FROM customers
                WHERE email = ?
            """, (
                email,
            )).fetchone()

            if existing:
                return None

            cursor = conn.execute("""
                INSERT INTO customers (
                    email,
                    full_name,
                    google_sub,
                    email_verified,
                    created_at,
                    updated_at
                )
                VALUES (?, ?, ?, 1, ?, ?)
            """, (
                email,
                full_name,
                google_sub,
                now,
                now
            ))

            conn.commit()

            customer = conn.execute("""
                SELECT *
                FROM customers
                WHERE id = ?
            """, (
                cursor.lastrowid,
            )).fetchone()

            return dict(customer) if customer else None

    except sqlite3.IntegrityError:
        # Handle a concurrent Google login safely.
        try:
            with get_auth_db() as conn:
                customer = conn.execute("""
                    SELECT *
                    FROM customers
                    WHERE google_sub = ?
                """, (
                    google_sub,
                )).fetchone()

                return dict(customer) if customer else None

        except sqlite3.Error:
            return None

    except sqlite3.Error:
        return None