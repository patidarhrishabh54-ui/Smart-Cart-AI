
/* =========================================================
   SMARTCART AI — MAIN.JS
   Shared frontend interactions
   ========================================================= */

(function () {
    "use strict";

    const COMPARE_KEY = "smartcart_compare_products";
    const MAX_COMPARE = 4;

    document.addEventListener("DOMContentLoaded", function () {
        initImageFallbacks();
        initSearch();
        initCategoryMenu();
        initFlashMessages();
        initCompareSystem();
        initSortForm();
        initProductCards();
        initPasswordToggle();
        initPriceChart();
        initSmoothScroll();
        initMobileNavigation();
        initKeyboardAccessibility();
    });

    /* -----------------------------------------------------
       IMAGE FALLBACKS
       ----------------------------------------------------- */

        function initImageFallbacks() {
        document.querySelectorAll(
            ".product-image, [data-product-image], " +
            ".gallery-thumb img, .main-product-image img, " +
            ".luxury-product-image img"
        ).forEach(function (image) {
            if (image.dataset.fallbackReady === "1") return;

            image.dataset.fallbackReady = "1";

            function applyFallback() {
                if (image.dataset.fallbackApplied === "1") return;

                image.dataset.fallbackApplied = "1";

                const fallback =
                    "/static/images/products/product-placeholder.svg";

                if (!image.src.endsWith("product-placeholder.svg")) {
                    image.src = fallback;
                } else {
                    image.alt = image.alt || "Product image unavailable";
                }
            }

            image.addEventListener("error", applyFallback);

            // The image may have already failed before this script ran
            // (scripts are deferred), so the error event was missed.
            if (image.complete && image.naturalWidth === 0 && image.src) {
                applyFallback();
            }
        });
    }
    /* -----------------------------------------------------
       SEARCH
       ----------------------------------------------------- */

    function initSearch() {
        document.querySelectorAll(
            ".header-search, .search-page-search, " +
            ".hero-search, .luxury-search-form"
        ).forEach(function (form) {
            if (form.dataset.mainSearchReady === "1") return;

            form.dataset.mainSearchReady = "1";

            const input = form.querySelector(
                'input[name="q"], input[type="search"], input[type="text"]'
            );

            if (!input) return;

            form.addEventListener("submit", function (event) {
                input.value = input.value.trim();

                if (!input.value) {
                    event.preventDefault();
                    input.focus();
                }
            });
        });
    }

    /* -----------------------------------------------------
       CATEGORY MENU
       ----------------------------------------------------- */

    function initCategoryMenu() {
        const wrappers = document.querySelectorAll(
            ".nav-category-wrapper"
        );

        wrappers.forEach(function (wrapper) {
            const button = wrapper.querySelector("[data-category-menu]");
            const menu = wrapper.querySelector(".category-mega-menu");

            if (!button || !menu) return;

            function closeMenu() {
                wrapper.classList.remove("is-open");
                button.setAttribute("aria-expanded", "false");
            }

            button.addEventListener("click", function (event) {
                event.preventDefault();
                event.stopPropagation();

                const open = !wrapper.classList.contains("is-open");

                wrappers.forEach(function (other) {
                    other.classList.remove("is-open");

                    const otherButton = other.querySelector(
                        "[data-category-menu]"
                    );

                    if (otherButton) {
                        otherButton.setAttribute("aria-expanded", "false");
                    }
                });

                if (open) {
                    wrapper.classList.add("is-open");
                    button.setAttribute("aria-expanded", "true");
                }
            });

            document.addEventListener("click", function (event) {
                if (!wrapper.contains(event.target)) closeMenu();
            });

            document.addEventListener("keydown", function (event) {
                if (event.key === "Escape") closeMenu();
            });
        });
    }

    /* -----------------------------------------------------
       FLASH MESSAGES
       ----------------------------------------------------- */

    function initFlashMessages() {
        document.querySelectorAll("[data-close-flash]").forEach(
            function (button) {
                button.addEventListener("click", function () {
                    const message = button.closest(".flash-message");
                    if (!message) return;

                    message.style.opacity = "0";
                    message.style.transform = "translateY(-5px)";

                    window.setTimeout(function () {
                        message.remove();
                    }, 200);
                });
            }
        );
    }

    /* -----------------------------------------------------
       COMPARE SYSTEM
       compare.js can use the same storage key.
       ----------------------------------------------------- */

    function getCompareItems() {
        try {
            const data = JSON.parse(
                localStorage.getItem(COMPARE_KEY) || "[]"
            );

            if (!Array.isArray(data)) return [];

            return [...new Set(
                data.map(String).filter(Boolean)
            )].slice(0, MAX_COMPARE);
        } catch (error) {
            return [];
        }
    }

    function saveCompareItems(items) {
        try {
            localStorage.setItem(
                COMPARE_KEY,
                JSON.stringify(items.slice(0, MAX_COMPARE))
            );
        } catch (error) {
            console.warn("SmartCart: unable to save comparison list.");
        }
    }

    function updateCompareBar() {
        const items = getCompareItems();

        document.querySelectorAll("[data-compare-count]").forEach(
            function (element) {
                element.textContent = String(items.length);
            }
        );

        document.querySelectorAll(".compare-floating-bar").forEach(
            function (bar) {
                bar.classList.toggle("active", items.length > 0);

                const count = bar.querySelector(
                    ".compare-floating-count"
                );

                if (count) count.textContent = String(items.length);

                bar.setAttribute(
                    "aria-hidden",
                    String(items.length === 0)
                );
            }
        );
    }

    function showToast(message) {
        let toast = document.querySelector(".smartcart-toast");

        if (!toast) {
            toast = document.createElement("div");
            toast.className = "smartcart-toast";
            toast.setAttribute("role", "status");
            toast.setAttribute("aria-live", "polite");

            Object.assign(toast.style, {
                position: "fixed",
                right: "18px",
                bottom: "18px",
                zIndex: "9999",
                maxWidth: "calc(100vw - 36px)",
                padding: "13px 17px",
                borderRadius: "11px",
                background: "#172033",
                color: "#ffffff",
                fontSize: "13px",
                boxShadow: "0 10px 30px rgba(0,0,0,.18)",
                opacity: "0",
                transition: "opacity .2s ease"
            });

            document.body.appendChild(toast);
        }

        toast.textContent = message;
        toast.style.opacity = "1";

        window.clearTimeout(toast._timer);

        toast._timer = window.setTimeout(function () {
            toast.style.opacity = "0";
        }, 2500);
    }

    function addCompareItem(productId) {
        if (!productId) return;

        const items = getCompareItems();
        const id = String(productId);

        if (items.includes(id)) {
            showToast("This product is already in your comparison list.");
            return;
        }

        if (items.length >= MAX_COMPARE) {
            showToast("You can compare up to 4 products.");
            return;
        }

        items.push(id);
        saveCompareItems(items);
        updateCompareBar();
        showToast("Product added to comparison.");
    }

    function initCompareSystem() {
        // One delegated listener avoids binding every button separately.
        document.addEventListener("click", function (event) {
            const addButton = event.target.closest("[data-compare-product]");

            if (addButton) {
                event.preventDefault();
                event.stopPropagation();

                const before = getCompareItems().length;
                const productId = addButton.getAttribute(
                    "data-compare-product"
                );

                addCompareItem(productId);

                const after = getCompareItems().length;

                if (
                    after > before &&
                    addButton.dataset.compareRedirect === "true"
                ) {
                    window.location.href =
                        addButton.dataset.compareUrl || "/compare";
                }

                return;
            }

            const clearButton = event.target.closest("[data-clear-compare]");

            if (clearButton) {
                event.preventDefault();
                saveCompareItems([]);
                updateCompareBar();
                showToast("Comparison list cleared.");
                return;
            }

            const openButton = event.target.closest("[data-open-compare]");

            if (openButton) {
                event.preventDefault();

                if (getCompareItems().length === 0) {
                    showToast("Add a product before comparing.");
                    return;
                }

                window.location.href =
                    openButton.dataset.compareUrl || "/compare";
            }
        });

        window.addEventListener("pageshow", updateCompareBar);

        window.addEventListener("storage", function (event) {
            if (event.key === COMPARE_KEY) updateCompareBar();
        });

        updateCompareBar();
    }

    /* -----------------------------------------------------
       SORTING
       ----------------------------------------------------- */

    function initSortForm() {
        document.querySelectorAll(
            ".sort-select, .sort-form select"
        ).forEach(function (select) {
            if (select.dataset.mainSortReady === "1") return;

            select.dataset.mainSortReady = "1";

            select.addEventListener("change", function () {
                const url = new URL(window.location.href);

                url.searchParams.set("sort", select.value);
                url.searchParams.delete("page");

                window.location.href = url.toString();
            });
        });
    }

    /* -----------------------------------------------------
       PRODUCT CARD INTERACTIONS
       ----------------------------------------------------- */

    function initProductCards() {
        document.querySelectorAll(
            ".product-card, .luxury-product-card"
        ).forEach(function (card) {
            card.addEventListener("mouseenter", function () {
                card.classList.add("is-hovered");
            });

            card.addEventListener("mouseleave", function () {
                card.classList.remove("is-hovered");
            });
        });
    }

    /* -----------------------------------------------------
       PASSWORD TOGGLE
       ----------------------------------------------------- */

    function initPasswordToggle() {
        document.querySelectorAll("[data-password-toggle]").forEach(
            function (button) {
                button.addEventListener("click", function () {
                    const selector = button.getAttribute(
                        "data-password-toggle"
                    );

                    if (!selector) return;

                    let input;

                    try {
                        input = document.querySelector(selector);
                    } catch (error) {
                        return;
                    }

                    if (!input) return;

                    const show = input.type === "password";
                    input.type = show ? "text" : "password";
                    button.textContent = show ? "Hide" : "Show";
                    button.setAttribute("aria-pressed", String(show));
                });
            }
        );
    }

    /* -----------------------------------------------------
       PRICE HISTORY CHART
       ----------------------------------------------------- */

    function initPriceChart() {
        const chart = document.querySelector("#smartPriceChart");
        if (!chart) return;

        let history = [];
        let forecast = [];

        try {
            history = JSON.parse(
                chart.getAttribute("data-history") || "[]"
            );

            forecast = JSON.parse(
                chart.getAttribute("data-forecast") || "[]"
            );
        } catch (error) {
            history = [];
            forecast = [];
        }

        if (!history.length && Array.isArray(window.smartcartHistory)) {
            history = window.smartcartHistory;
        }

        if (!forecast.length && Array.isArray(window.smartcartForecast)) {
            forecast = window.smartcartForecast;
        }

        renderPriceChart(chart, history, forecast);
    }

    function getPrice(item) {
        let value = item;

        if (item && typeof item === "object") {
            value = item.price ?? item.value ?? item.amount ??
                item.predicted_price ?? item.forecast_price;
        }

        if (typeof value === "string") {
            value = parseFloat(value.replace(/[^0-9.-]/g, ""));
        }

        const number = Number(value);

        return Number.isFinite(number) ? number : null;
    }

    function getLabel(item, index) {
        if (item && typeof item === "object") {
            return String(
                item.month || item.date || item.label ||
                item.period || index + 1
            );
        }

        return String(index + 1);
    }

    function normalizeData(data) {
        if (!Array.isArray(data)) return [];

        return data.map(function (item, index) {
            return {
                label: getLabel(item, index),
                price: getPrice(item)
            };
        }).filter(function (item) {
            return item.price !== null && item.price >= 0;
        });
    }

    function escapeHTML(value) {
        return String(value)
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    }

    function renderPriceChart(container, rawHistory, rawForecast) {
        const history = normalizeData(rawHistory);
        const forecast = normalizeData(rawForecast);
        const data = history.concat(forecast);

        if (!data.length) {
            container.textContent =
                "Price history is not available for this product yet.";
            return;
        }

        const width = 900;
        const height = 340;
        const pad = { top: 30, right: 25, bottom: 55, left: 75 };
        const plotWidth = width - pad.left - pad.right;
        const plotHeight = height - pad.top - pad.bottom;

        const prices = data.map(function (item) {
            return item.price;
        });

        let min = Math.min(...prices);
        let max = Math.max(...prices);

        if (min === max) {
            min = Math.max(0, min * 0.9);
            max = max * 1.1 || 1;
        }

        const extra = (max - min) * 0.12;
        min = Math.max(0, min - extra);
        max += extra;

        function x(index) {
            if (data.length === 1) return pad.left + plotWidth / 2;

            return pad.left + index / (data.length - 1) * plotWidth;
        }

        function y(price) {
            return pad.top +
                (1 - (price - min) / (max - min)) * plotHeight;
        }

        function points(items, offset) {
            return items.map(function (item, index) {
                return x(index + offset).toFixed(1) + "," +
                    y(item.price).toFixed(1);
            }).join(" ");
        }

        let svg = '<svg viewBox="0 0 ' + width + " " + height +
            '" width="100%" role="img" aria-label="Price history and forecast">';

        for (let i = 0; i <= 4; i++) {
            const lineY = pad.top + i / 4 * plotHeight;
            const value = max - i / 4 * (max - min);

            svg += '<line x1="' + pad.left + '" y1="' + lineY +
                '" x2="' + (width - pad.right) + '" y2="' + lineY +
                '" stroke="#e5e9f2" stroke-width="1"></line>';

            svg += '<text x="' + (pad.left - 10) + '" y="' +
                (lineY + 4) +
                '" text-anchor="end" font-size="11" fill="#697386">₹' +
                Math.round(value).toLocaleString("en-IN") +
                "</text>";
        }

        if (history.length) {
            svg += '<polyline points="' + points(history, 0) +
                '" fill="none" stroke="#4f46e5" stroke-width="3.5" ' +
                'stroke-linecap="round" stroke-linejoin="round"></polyline>';
        }

        if (forecast.length) {
            svg += '<polyline points="' +
                points(forecast, history.length) +
                '" fill="none" stroke="#d97706" stroke-width="3.5" ' +
                'stroke-dasharray="7 6" stroke-linecap="round"></polyline>';
        }

        data.forEach(function (item, index) {
            const isForecast = index >= history.length;

            svg += '<circle cx="' + x(index) + '" cy="' + y(item.price) +
                '" r="4.5" fill="#fff" stroke="' +
                (isForecast ? "#d97706" : "#4f46e5") +
                '" stroke-width="3"></circle>';
        });

        const labelStep = Math.max(1, Math.ceil(data.length / 7));

        data.forEach(function (item, index) {
            if (index % labelStep !== 0 && index !== data.length - 1) return;

            svg += '<text x="' + x(index) + '" y="' + (height - 18) +
                '" text-anchor="middle" font-size="10" fill="#697386">' +
                escapeHTML(item.label) + "</text>";
        });

        svg += "</svg>";

        svg += '<div class="price-chart-legend">' +
            '<span><strong style="color:#4f46e5">●</strong> Historical</span>' +
            '<span><strong style="color:#d97706">●</strong> Forecast</span>' +
            "</div>";

        container.innerHTML = svg;
    }

    /* -----------------------------------------------------
       SMOOTH SCROLL
       ----------------------------------------------------- */

    function initSmoothScroll() {
        document.querySelectorAll('a[href^="#"]').forEach(function (link) {
            link.addEventListener("click", function (event) {
                const selector = link.getAttribute("href");

                if (!selector || selector === "#") return;

                let target;

                try {
                    target = document.querySelector(selector);
                } catch (error) {
                    return;
                }

                if (!target) return;

                event.preventDefault();

                target.scrollIntoView({
                    behavior: window.matchMedia(
                        "(prefers-reduced-motion: reduce)"
                    ).matches ? "auto" : "smooth",
                    block: "start"
                });
            });
        });
    }

    /* -----------------------------------------------------
       MOBILE NAVIGATION ACTIVE STATE
       ----------------------------------------------------- */

    function initMobileNavigation() {
        const currentPath = window.location.pathname;

        document.querySelectorAll(".mobile-bottom-nav a").forEach(
            function (link) {
                try {
                    const url = new URL(link.href, window.location.origin);

                    if (url.pathname === currentPath) {
                        link.classList.add("active");
                        link.setAttribute("aria-current", "page");
                    }
                } catch (error) {
                    // Ignore malformed links.
                }
            }
        );
    }

    /* -----------------------------------------------------
       KEYBOARD ACCESSIBILITY
       ----------------------------------------------------- */

    function initKeyboardAccessibility() {
        document.addEventListener("keydown", function (event) {
            if (event.key !== "Escape") return;

            document.querySelectorAll(".nav-category-wrapper.is-open")
                .forEach(function (wrapper) {
                    wrapper.classList.remove("is-open");

                    const button = wrapper.querySelector(
                        "[data-category-menu]"
                    );

                    if (button) button.setAttribute("aria-expanded", "false");
                });
        });
    }

    /* -----------------------------------------------------
       PUBLIC API
       ----------------------------------------------------- */

    window.SmartCart = {
        addCompare: addCompareItem,
        getCompare: getCompareItems,
        updateCompareBar: updateCompareBar,
        showToast: showToast
    };

})();
