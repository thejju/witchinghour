
document.addEventListener("DOMContentLoaded", function () {

    // Mobile navigation
    const menuButton = document.querySelector(".menu-toggle");
    const navigation = document.querySelector(".nav-links");

    if (menuButton && navigation) {
        menuButton.addEventListener("click", function () {
            const isOpen = navigation.classList.toggle("open");

            menuButton.setAttribute("aria-expanded", String(isOpen));
            menuButton.textContent = isOpen ? "✕" : "☰";
        });
    }

    // Reveal cards when they enter the screen
    const revealItems = document.querySelectorAll(".reveal");

    if ("IntersectionObserver" in window) {
        const observer = new IntersectionObserver(function (items) {
            items.forEach(function (item) {
                if (item.isIntersecting) {
                    item.target.classList.add("visible");
                    observer.unobserve(item.target);
                }
            });
        }, { threshold: 0.12 });

        revealItems.forEach(function (item) {
            observer.observe(item);
        });
    } else {
        revealItems.forEach(function (item) {
            item.classList.add("visible");
        });
    }

    // Search and filter content cards
    const searchInput = document.querySelector("[data-search]");
    const cards = document.querySelectorAll("[data-search-card]");

    if (searchInput) {
        searchInput.addEventListener("input", function () {
            const query = searchInput.value.toLowerCase().trim();

            cards.forEach(function (card) {
                const text = card.textContent.toLowerCase();
                card.hidden = !text.includes(query);
            });
        });
    }

    // Journal edit buttons
    const editButtons = document.querySelectorAll("[data-edit-entry]");
    const titleInput = document.querySelector("#entry-title");
    const contentInput = document.querySelector("#entry-content");
    const entryIdInput = document.querySelector("#entry-id");
    const journalForm = document.querySelector("#journal-form");

    editButtons.forEach(function (button) {
        button.addEventListener("click", function () {
            if (!titleInput || !contentInput ||
                !entryIdInput || !journalForm) {
                return;
            }

            titleInput.value = button.dataset.title || "";
            contentInput.value = button.dataset.content || "";
            entryIdInput.value = button.dataset.editEntry || "";

            titleInput.focus();

            journalForm.scrollIntoView({
                behavior: "smooth",
                block: "center"
            });
        });
    });

});

