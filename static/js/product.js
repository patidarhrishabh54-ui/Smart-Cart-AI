
/* SMARTCART AI — PRODUCT.JS */
(function () {
    "use strict";

    function initProductPage() {
        // Quantity controls: support buttons marked with data-quantity-action.
        document.addEventListener("click", function (event) {
            const button = event.target.closest("[data-quantity-action]");
            if (!button) return;

            const selector = button.getAttribute("data-quantity-target");
            let input = null;

            if (selector) {
                try {
                    input = document.querySelector(selector);
                } catch (error) {
                    input = null;
                }
            }

            if (!input) {
                input = button.closest(".quantity-control, .quantity-selector")
                    ?.querySelector("input[type='number']");
            }

            if (!input) return;

            event.preventDefault();

            const min = Number(input.min || 1);
            const max = Number(input.max || 99);
            const current = Number(input.value || min);
            const action = button.getAttribute("data-quantity-action");

            let next = current;

            if (action === "increase") next = current + 1;
            if (action === "decrease") next = current - 1;

            input.value = String(Math.min(max, Math.max(min, next)));
            input.dispatchEvent(new Event("input", { bubbles: true }));
            input.dispatchEvent(new Event("change", { bubbles: true }));
        });

        // Keep manually entered quantities within valid bounds.
        document.querySelectorAll("input[type='number'][data-quantity]").forEach(
            function (input) {
                input.addEventListener("change", function () {
                    const min = Number(input.min || 1);
                    const max = Number(input.max || 99);
                    let value = Number(input.value);

                    if (!Number.isFinite(value)) value = min;

                    input.value = String(
                        Math.min(max, Math.max(min, Math.floor(value)))
                    );
                });
            }
        );

        // Optional accessible image zoom for elements using data-product-zoom.
        document.querySelectorAll("[data-product-zoom]").forEach(function (image) {
            image.style.cursor = "zoom-in";
            image.setAttribute("tabindex", "0");
            image.setAttribute("role", "button");
            image.setAttribute("aria-label", "Open larger product image");

            function toggleZoom() {
                const zoomed = image.classList.toggle("is-zoomed");
                image.style.transform = zoomed ? "scale(1.5)" : "";
                image.style.cursor = zoomed ? "zoom-out" : "zoom-in";
                image.style.position = zoomed ? "relative" : "";
                image.style.zIndex = zoomed ? "2" : "";
            }

            image.addEventListener("click", toggleZoom);

            image.addEventListener("keydown", function (event) {
                if (event.key === "Enter" || event.key === " ") {
                    event.preventDefault();
                    toggleZoom();
                }

                if (event.key === "Escape") {
                    image.classList.remove("is-zoomed");
                    image.style.transform = "";
                    image.style.cursor = "zoom-in";
                    image.style.position = "";
                    image.style.zIndex = "";
                }
            });
        });
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", initProductPage);
    } else {
        initProductPage();
    }
})();
