
/* SMARTCART AI — SEARCH.JS */
(function () {
    "use strict";

    function initSearch() {
        const fields = document.querySelectorAll(
            '.header-search input, .search-page-search input, ' +
            '.hero-search input, .luxury-search-form input, ' +
            'form[role="search"] input[type="search"]'
        );

        fields.forEach(function (input) {
            const form = input.closest("form");

            if (form && !form.dataset.smartcartSearchReady) {
                form.dataset.smartcartSearchReady = "true";

                form.addEventListener("submit", function (event) {
                    input.value = input.value.trim();

                    if (!input.value) {
                        event.preventDefault();
                        input.focus();
                    }
                });
            }

            input.setAttribute("aria-label",
                input.getAttribute("aria-label") || "Search products");

            // Escape clears the field; Enter keeps normal form submission.
            input.addEventListener("keydown", function (event) {
                if (event.key === "Escape" && input.value) {
                    input.value = "";
                    input.dispatchEvent(new Event("input", { bubbles: true }));
                }
            });
        });

        document.querySelectorAll("[data-search-clear]").forEach(function (button) {
            button.addEventListener("click", function () {
                const selector = button.getAttribute("data-search-clear");
                let input = null;

                if (selector) {
                    try {
                        input = document.querySelector(selector);
                    } catch (error) {
                        input = null;
                    }
                }

                if (!input) {
                    input = button.closest("form")?.querySelector("input");
                }

                if (input) {
                    input.value = "";
                    input.focus();
                    input.dispatchEvent(new Event("input", { bubbles: true }));
                }
            });
        });
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", initSearch);
    } else {
        initSearch();
    }
})();
