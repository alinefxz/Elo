<<<<<<< HEAD
/* Sugestoes de cidade por UF, mantendo livre o cadastro de outras localidades. */
document.querySelectorAll('input[list]').forEach((campo) => {
    const lista = document.getElementById(campo.getAttribute('list'));
    const estado = campo.form?.querySelector('select[name="estado"]');
    if (!lista || !estado || !lista.querySelector('option[data-uf]')) return;
    const opcoes = Array.from(lista.options, (opcao) => opcao.cloneNode(true));
    const atualizar = () => {
        const filtradas = opcoes.filter((opcao) => !estado.value || opcao.dataset.uf === estado.value);
        lista.replaceChildren(...filtradas.map((opcao) => opcao.cloneNode(true)));
    };
    estado.addEventListener('change', atualizar);
    atualizar();
=======
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
>>>>>>> fix/unboundlocal-form-pedido-2026-10-09
});
