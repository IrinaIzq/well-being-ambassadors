document.querySelectorAll("[data-tabs]").forEach((tabs) => {
    tabs.addEventListener("click", (event) => {
        const button = event.target.closest("[data-tab]");
        if (!button) {
            return;
        }

        const target = button.dataset.tab;
        tabs.querySelectorAll("[data-tab]").forEach((tab) => {
            tab.classList.toggle("active", tab.dataset.tab === target);
        });
        document.querySelectorAll("[data-panel]").forEach((panel) => {
            panel.classList.toggle("active", panel.dataset.panel === target);
        });
    });
});

document.querySelectorAll("[data-add-member]").forEach((button) => {
    button.addEventListener("click", () => {
        const container = document.querySelector("[data-members]");
        const row = document.createElement("div");
        row.className = "member-row";
        row.innerHTML = '<input name="member_name" required placeholder="Full name"><input name="member_email" required type="email" placeholder="Email">';
        container.append(row);
    });
});
