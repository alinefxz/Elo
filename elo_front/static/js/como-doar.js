document.addEventListener("DOMContentLoaded", () => {
    const page = document.querySelector(".pagina-como-doar");
    if (!page) return;

    const revealItems = [...page.querySelectorAll(".doar-reveal")];
    const progress = page.querySelector(".journey-track-line span");
    const track = page.querySelector("[data-journey-track]");
    const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

    if (reduceMotion || !("IntersectionObserver" in window)) {
        revealItems.forEach((item) => item.classList.add("is-visible"));
    } else {
        const revealObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach((entry) => {
                if (!entry.isIntersecting) return;
                entry.target.classList.add("is-visible");
                observer.unobserve(entry.target);
            });
        }, { threshold: 0.12, rootMargin: "0px 0px -8%" });

        revealItems.forEach((item) => revealObserver.observe(item));
    }

    const updateProgress = () => {
        if (!progress || !track || reduceMotion) return;
        const rect = track.getBoundingClientRect();
        const viewportAnchor = window.innerHeight * .58;
        const total = Math.max(1, rect.height);
        const current = Math.min(total, Math.max(0, viewportAnchor - rect.top));
        progress.style.height = `${(current / total) * 100}%`;
    };

    updateProgress();
    window.addEventListener("scroll", updateProgress, { passive: true });
    window.addEventListener("resize", updateProgress);
});
