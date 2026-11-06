/* Menu global do Elo: painel lateral, foco controlado e fechamento seguro. */
document.addEventListener("DOMContentLoaded", () => {
    const toggle = document.querySelector(".menu-toggle");
    const menu = document.querySelector(".main-nav");
    const backdrop = document.querySelector(".menu-backdrop");
    if (!toggle || !menu || !backdrop) return;

    let lastFocused = null;
    const focusableSelector = 'a[href], button:not([disabled]), input:not([disabled]), select:not([disabled]), textarea:not([disabled])';

    const setOpen = (open, restoreFocus = true) => {
        if (open) lastFocused = document.activeElement;
        document.body.classList.toggle("menu-open", open);
        menu.classList.toggle("is-open", open);
        backdrop.classList.toggle("is-visible", open);
        menu.setAttribute("aria-hidden", open ? "false" : "true");
        toggle.setAttribute("aria-expanded", open ? "true" : "false");
        toggle.setAttribute("aria-label", open ? "Fechar menu" : "Abrir menu");
        if (open) {
            menu.querySelector(focusableSelector)?.focus();
        } else if (restoreFocus && lastFocused instanceof HTMLElement) {
            lastFocused.focus();
        }
    };

    toggle.addEventListener("click", () => setOpen(!menu.classList.contains("is-open")));
    backdrop.addEventListener("click", () => setOpen(false));
    menu.addEventListener("click", (event) => {
        if (event.target.closest("a")) setOpen(false, false);
    });

    document.addEventListener("keydown", (event) => {
        if (!menu.classList.contains("is-open")) return;
        if (event.key === "Escape") {
            event.preventDefault();
            setOpen(false);
            return;
        }
        if (event.key !== "Tab") return;
        const items = [...menu.querySelectorAll(focusableSelector)];
        if (!items.length) return;
        const first = items[0];
        const last = items[items.length - 1];
        if (event.shiftKey && document.activeElement === first) {
            event.preventDefault();
            last.focus();
        } else if (!event.shiftKey && document.activeElement === last) {
            event.preventDefault();
            first.focus();
        }
    });
});
