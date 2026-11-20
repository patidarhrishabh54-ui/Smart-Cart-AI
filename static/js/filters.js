
/* SMARTCART AI — FILTERS.JS */
(function () {
    "use strict";

    function initFilters() {
        const button = document.querySelector("[data-filter-toggle], .mobile-filter-button");
        const sidebar = document.querySelector("[data-filter-sidebar], .filter-sidebar");
        const overlay = document.querySelector("[data-filter-overlay], .filter-overlay");
        const closeButton = document.querySelector("[data-filter-close]");

        if (!sidebar) return;

        function openFilters() {
            sidebar.classList.add("open", "is-open");
            if (overlay) overlay.classList.add("is-visible");
            document.body.classList.add("filters-open");

            if (button) {
                button.setAttribute("aria-expanded", "true");
            }
        }

        function closeFilters() {
            sidebar.classList.remove("open", "is-open");
            if (overlay) overlay.classList.remove("is-visible");
            document.body.classList.remove("filters-open");

            if (button) {
                button.setAttribute("aria-expanded", "false");
            }
        }

        // Keep the state synchronized with the existing main.js handler.
        if (button) {
            button.addEventListener("click", function () {
                window.setTimeout(function () {
                    const isOpen =
                        sidebar.classList.contains("open") ||
                        sidebar.classList.contains("is-open");

                    if (isOpen) openFilters();
                    else closeFilters();
                }, 0);
            });
        }

        if (closeButton) {
            closeButton.addEventListener("click", closeFilters);
        }

        if (overlay) {
            overlay.addEventListener("click", closeFilters);
        }

        document.addEventListener("keydown", function (event) {
            if (event.key === "Escape") closeFilters();
        });

        // Highlight selected filter options without changing form behaviour.
        sidebar.querySelectorAll("input").forEach(function (input) {
            function updateOption() {
                const option = input.closest(
                    ".filter-option, .filter-checkbox, .filter-radio, label"
                );
                if (option) {
                    option.classList.toggle("selected", input.checked);
                }
            }

            input.addEventListener("change", updateOption);
            updateOption();
        });
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", initFilters);
    } else {
        initFilters();
    }
})();
