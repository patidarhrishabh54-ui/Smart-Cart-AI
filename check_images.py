
import sqlite3
import urllib.request
import concurrent.futures
import os
import time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, "smartcart.db")
TIMEOUT = 8
MAX_WORKERS = 12
REPORT_FILE = os.path.join(BASE_DIR, "image_check_report.csv")


def get_image_rows():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row

    try:
        products = conn.execute("""
            SELECT id, name, image
            FROM products
            ORDER BY id
        """).fetchall()

        table_exists = conn.execute("""
            SELECT 1
            FROM sqlite_master
            WHERE type='table' AND name='product_images'
        """).fetchone()

        image_rows = []

        if table_exists:
            image_rows = conn.execute("""
                SELECT product_id, image_url
                FROM product_images
                ORDER BY product_id, image_order, id
            """).fetchall()

        return products, image_rows
    finally:
        conn.close()


def check_url(item):
    product_id, name, url = item
    url = str(url or "").strip()

    if not url.startswith(("http://", "https://")):
        return product_id, name, url, "MISSING_OR_LOCAL", ""

    try:
        request = urllib.request.Request(
            url,
            headers={"User-Agent": "Mozilla/5.0"},
            method="HEAD"
        )

        with urllib.request.urlopen(
            request, timeout=TIMEOUT
        ) as response:
            content_type = response.headers.get(
                "Content-Type", ""
            ).lower()

            if response.status >= 400:
                status = "HTTP_ERROR"
            elif content_type.startswith("image/"):
                status = "OK"
            else:
                status = "NOT_AN_IMAGE"

            return (
                product_id, name, url, status,
                str(response.status) + " " + content_type
            )

    except Exception:
        # Some image servers block HEAD requests; retry with GET.
        try:
            request = urllib.request.Request(
                url,
                headers={"User-Agent": "Mozilla/5.0"},
                method="GET"
            )

            with urllib.request.urlopen(
                request, timeout=TIMEOUT
            ) as response:
                content_type = response.headers.get(
                    "Content-Type", ""
                ).lower()
                response.read(32)

                status = (
                    "OK"
                    if response.status < 400
                    and content_type.startswith("image/")
                    else "NOT_AN_IMAGE"
                )

                return (
                    product_id, name, url, status,
                    str(response.status) + " " + content_type
                )
        except Exception as error:
            return product_id, name, url, "ERROR", str(error)


def main():
    products, image_rows = get_image_rows()

    product_image_map = {}

    for row in image_rows:
        url = str(row["image_url"] or "").strip()
        if url:
            product_image_map.setdefault(
                row["product_id"], []
            ).append(url)

    print("Products found:", len(products))
    print("Product image records:", len(image_rows))
    print("Products with 3+ image records:", sum(
        len(set(product_image_map.get(row["id"], []))) >= 3
        for row in products
    ))

    jobs = []

    for row in products:
        product_id = row["id"]
        name = row["name"] or "Unnamed product"
        urls = list(product_image_map.get(product_id, []))

        main_image = str(row["image"] or "").strip()
        if main_image:
            urls.append(main_image)

        # Check each distinct URL only once per product.
        urls = list(dict.fromkeys(urls))

        if not urls:
            jobs.append((
                product_id, name, "", "MISSING", ""
            ))
        else:
            for url in urls:
                jobs.append((product_id, name, url))

    results = []
    start = time.time()

    checks = [job for job in jobs if len(job) == 3]
    missing = [job for job in jobs if len(job) == 5]

    results.extend(missing)

    print("URLs to check:", len(checks))
    print("Checking image URLs. This may take some time...")

    with concurrent.futures.ThreadPoolExecutor(
        max_workers=MAX_WORKERS
    ) as executor:
        for number, result in enumerate(
            executor.map(check_url, checks), start=1
        ):
            results.append(result)

            if number % 100 == 0:
                print(f"Checked {number}/{len(checks)} URLs")

    import csv

    with open(
        REPORT_FILE, "w", newline="", encoding="utf-8-sig"
    ) as file:
        writer = csv.writer(file)
        writer.writerow([
            "product_id", "product_name", "image_url",
            "status", "details"
        ])
        writer.writerows(results)

    counts = {}
    for result in results:
        counts[result[3]] = counts.get(result[3], 0) + 1

    print("\n--- IMAGE CHECK SUMMARY ---")
    for status, count in sorted(counts.items()):
        print(f"{status}: {count}")

    print(f"\nReport saved to: {REPORT_FILE}")
    print(f"Time taken: {time.time() - start:.1f} seconds")
    print("No database records were changed.")


if __name__ == "__main__":
    main()
