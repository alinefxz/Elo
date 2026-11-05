document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll("select[data-estado]").forEach((cidade) => {
        const estado = document.getElementById(`id_${cidade.dataset.estado}`);

        if (!estado) {
            return;
        }

        const cidadesPorEstado = JSON.parse(
            cidade.dataset.cidadesPorEstado || "{}",
        );

        const atualizarCidades = () => {
            const cidadeSelecionada = cidade.value;
            const cidades = cidadesPorEstado[estado.value] || [];

            cidade.replaceChildren(new Option("Selecione uma cidade", ""));
            cidades.forEach((nome) => {
                cidade.add(new Option(nome, nome, false, nome === cidadeSelecionada));
            });
        };

        estado.addEventListener("change", atualizarCidades);
    });
});
