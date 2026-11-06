/* Entrada progressiva da home, sem bloquear a leitura nem exigir JavaScript. */
document.addEventListener("DOMContentLoaded", () => {
    const elementos = document.querySelectorAll(".pagina-inicial .home-reveal");
    if (!elementos.length) return;

    if (!("IntersectionObserver" in window)) {
        elementos.forEach((elemento) => elemento.classList.add("is-visible"));
        return;
    }

    const observer = new IntersectionObserver((entries, instancia) => {
        entries.forEach((entry) => {
            if (!entry.isIntersecting) return;
            entry.target.classList.add("is-visible");
            instancia.unobserve(entry.target);
        });
    }, { threshold: 0.12, rootMargin: "0px 0px -8% 0px" });

    elementos.forEach((elemento) => observer.observe(elemento));
});
