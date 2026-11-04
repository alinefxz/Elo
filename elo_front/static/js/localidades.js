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
});
