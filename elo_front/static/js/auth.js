/* Transição curta entre os dois fluxos de autenticação. Os links continuam
   sendo links normais para manter acessibilidade e funcionamento sem JS. */
document.addEventListener("DOMContentLoaded", () => {
    const body = document.body;
    const transition = new URLSearchParams(window.location.search).get("transition");
    if (transition === "signup" || transition === "login") {
        body.classList.add(`auth-arrival-${transition}`);
        window.setTimeout(() => body.classList.remove(`auth-arrival-${transition}`), 700);
    }

    document.querySelectorAll("[data-auth-transition]").forEach((link) => {
        link.addEventListener("click", () => {
            const destino = link.dataset.authTransition;
            body.classList.add(`auth-leaving-${destino}`);
            const url = new URL(link.href, window.location.href);
            url.searchParams.set("transition", destino);
            link.href = url.toString();
        });
    });
});
