
/* SMARTCART AI — COMPARE.JS */
(function () {
    "use strict";

    const STORAGE_KEY = "smartcart_compare_products";
    const MAX_ITEMS = 4;

    function getItems() {
        try {
            const data = JSON.parse(localStorage.getItem(STORAGE_KEY) || "[]");
            if (!Array.isArray(data)) return [];

            return [...new Set(data.map(String).filter(Boolean))]
                .slice(0, MAX_ITEMS);
        } catch (error) {
            return [];
        }
    }

    function saveItems(items) {
        try {
            localStorage.setItem(STORAGE_KEY, JSON.stringify(items));
        } catch (error) {
            console.warn("SmartCart: unable to save comparison list.");
        }
    }

    function updateBar() {
        const items = getItems();

        document.querySelectorAll("[data-compare-count]").forEach(function (el) {
            el.textContent = String(items.length);
        });

        document.querySelectorAll(".compare-floating-bar").forEach(function (bar) {
            bar.classList.toggle("active", items.length > 0);

            const count = bar.querySelector(".compare-floating-count");
            if (count) count.textContent = String(items.length);

            bar.setAttribute("aria-hidden", String(items.length === 0));
        });

        document.querySelectorAll("[data-open-compare]").forEach(function (button) {
            button.disabled = items.length === 0;
        });
    }

    function initCompare() {
        // Delegate clicks so dynamically rendered controls also work.
        document.addEventListener("click", function (event) {
            const clearButton = event.target.closest("[data-clear-compare]");

            if (clearButton) {
                event.preventDefault();
                saveItems([]);
                updateBar();

                if (window.SmartCart && typeof window.SmartCart.showToast === "function") {
                    window.SmartCart.showToast("Comparison list cleared.");
                }
                return;
            }

            const openButton = event.target.closest("[data-open-compare]");

            if (openButton) {
                event.preventDefault();

                const items = getItems();
                if (!items.length) return;

                const destination =
                    openButton.getAttribute("data-compare-url") || "/compare";

                window.location.href = destination;
            }
        });

        // main.js owns the add-to-compare button events.
        updateBar();

        window.addEventListener("pageshow", updateBar);
        window.addEventListener("storage", function (event) {
            if (event.key === STORAGE_KEY) updateBar();
        });

        window.SmartCartCompare = {
            getItems: getItems,
            saveItems: saveItems,
            updateBar: updateBar
        };
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", initCompare);
    } else {
        initCompare();
    }
})();
