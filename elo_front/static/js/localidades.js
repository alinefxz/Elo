/* Sugestões pesquisáveis de municípios por UF nos formulários do Elo. */
document.querySelectorAll('input[list]').forEach((campo) => {
    if (campo.dataset.municipiosUrl) return;
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

// O catálogo é servido localmente: não depende de uma chamada ao IBGE ao preencher.
document.querySelectorAll('input[data-municipios-url]').forEach((campo) => {
    const estado = campo.form?.querySelector('select[name="estado"]');
    const lista = document.getElementById(campo.getAttribute('list'));
    if (!estado || !lista) return;
    const status = document.createElement('small');
    status.id = `${campo.id}_localidade_status`;
    status.setAttribute('role', 'status');
    status.setAttribute('aria-live', 'polite');
    campo.insertAdjacentElement('afterend', status);
    const descricao = campo.getAttribute('aria-describedby') || '';
    campo.setAttribute('aria-describedby', `${descricao} ${status.id}`.trim());
    let consulta;
    const carregar = async (mudou = false) => {
        consulta?.abort();
        if (mudou) {
            campo.value = '';
            lista.replaceChildren();
        }
        const uf = estado.value;
        campo.disabled = !uf && !campo.value;
        if (!uf) {
            status.textContent = 'Selecione um estado para buscar os municípios.';
            return;
        }
        campo.disabled = false;
        campo.setAttribute('aria-busy', 'true');
        status.textContent = 'Carregando municípios…';
        const controlador = new AbortController();
        consulta = controlador;
        try {
            const url = new URL(campo.dataset.municipiosUrl, window.location.origin);
            url.searchParams.set('estado', uf);
            const resposta = await fetch(url, {signal: controlador.signal, headers: {'Accept': 'application/json'}});
            if (!resposta.ok) throw new Error('Catálogo indisponível');
            const dados = await resposta.json();
            if (consulta !== controlador || estado.value !== uf) return;
            if (!Array.isArray(dados.cidades)) throw new Error('Resposta inválida');
            lista.replaceChildren(...dados.cidades.map((nome) => new Option(nome, nome)));
            status.textContent = `${dados.cidades.length} municípios disponíveis. Digite para buscar.`;
        } catch (erro) {
            if (erro.name !== 'AbortError' && consulta === controlador) {
                status.textContent = 'Não foi possível carregar as sugestões. Digite seu município; ele será validado ao salvar.';
            }
        } finally {
            if (consulta === controlador) campo.removeAttribute('aria-busy');
        }
    };
    estado.addEventListener('change', () => carregar(true));
    carregar();
});
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
