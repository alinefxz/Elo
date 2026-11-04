/* Consulta avisos existentes enquanto a aba esta visivel. Nao solicita permissao do navegador. */
(() => {
    const widget = document.querySelector('[data-notificacoes]');
    if (!widget) return;
    const menu = widget.querySelector('details');
    const sino = widget.querySelector('summary');
    const contador = widget.querySelector('.notificacoes-contador');
    const status = widget.querySelector('.notificacoes-status');
    const lista = widget.querySelector('.notificacoes-lista');
    const erro = widget.querySelector('.notificacoes-erro');
    const csrf = widget.querySelector('[name="csrfmiddlewaretoken"]').value;
    const toast = document.querySelector('.notificacoes-toast');
    const chave = `elo-notificacoes-${widget.dataset.usuario}`;
    let ultimoId = Number(widget.dataset.ultimoId) || 0;
    let versao = 0;
    let ativo = true;
    let ocupado = false;
    let temporizadorToast;

    const lembrar = (valor) => {
        ultimoId = Math.max(ultimoId, valor);
        try { sessionStorage.setItem(chave, String(ultimoId)); } catch (_) { /* Storage opcional. */ }
    };
    try { ultimoId = Math.max(ultimoId, Number(sessionStorage.getItem(chave)) || 0); } catch (_) { /* Storage opcional. */ }
    lembrar(ultimoId);

    const elemento = (tag, classe, texto) => {
        const no = document.createElement(tag);
        if (classe) no.className = classe;
        if (texto !== undefined) no.textContent = texto;
        return no;
    };
    const urlInterna = (valor) => {
        try {
            const url = new URL(valor, location.origin);
            return url.origin === location.origin && ['http:', 'https:'].includes(url.protocol) ? url.href : '';
        } catch (_) { return ''; }
    };

    const desenhar = (itens) => {
        const fragmento = document.createDocumentFragment();
        itens.forEach((aviso) => {
            const item = elemento('li', `notificacao-item${aviso.lida ? '' : ' nao-lida'}`);
            item.append(elemento('strong', '', aviso.titulo));
            const data = elemento('time', '', aviso.data);
            data.dateTime = aviso.data_iso;
            item.append(data, elemento('p', '', aviso.mensagem),
                elemento('span', 'notificacao-estado', aviso.lida ? 'Lida' : 'Não lida'));
            const acoes = elemento('div', 'notificacao-acoes');
            if (aviso.url && urlInterna(aviso.url)) {
                const link = elemento('a', '', aviso.acao);
                link.href = urlInterna(aviso.url);
                acoes.append(link);
            }
            if (!aviso.lida && urlInterna(aviso.url_leitura)) {
                const form = elemento('form', 'notificacao-ler');
                form.method = 'post';
                form.action = urlInterna(aviso.url_leitura);
                const token = elemento('input');
                token.type = 'hidden'; token.name = 'csrfmiddlewaretoken'; token.value = csrf;
                const botao = elemento('button', '', 'Marcar como lida');
                botao.type = 'submit';
                form.append(token, botao);
                acoes.append(form);
            }
            item.append(acoes);
            fragmento.append(item);
        });
        if (!itens.length) fragmento.append(elemento('li', 'notificacoes-vazio', 'Você ainda não tem notificações.'));
        // Atualizacoes automaticas nao substituem o controle que esta com foco.
        if (!lista.contains(document.activeElement)) lista.replaceChildren(fragmento);
    };

    const avisar = (novas) => {
        if (!novas.length) return;
        toast.querySelector('.notificacoes-toast-titulo').textContent = novas.length > 1 ? 'Novas notificações' : 'Nova notificação';
        toast.querySelector('.notificacoes-toast-mensagem').textContent = novas.length > 1
            ? 'Chegaram novos avisos. Acesse o sino para conferir.' : novas[0].titulo;
        toast.hidden = false;
        clearTimeout(temporizadorToast);
        temporizadorToast = setTimeout(() => {
            if (!toast.matches(':hover') && !toast.contains(document.activeElement)) toast.hidden = true;
        }, 12000);
    };

    const atualizar = async () => {
        if (!ativo) return;
        const requisicao = ++versao;
        ocupado = true;
        try {
            const url = new URL(widget.dataset.atualizacoes, location.origin);
            url.searchParams.set('depois', ultimoId);
            const resposta = await fetch(url, { credentials: 'same-origin', cache: 'no-store', headers: { Accept: 'application/json' } });
            if (resposta.status === 401 || resposta.redirected) { ativo = false; return; }
            if (!resposta.ok) throw new Error();
            const dados = await resposta.json();
            if (requisicao !== versao) return;
            contador.textContent = dados.nao_lidas > 99 ? '99+' : String(dados.nao_lidas);
            contador.hidden = dados.nao_lidas === 0;
            sino.classList.toggle('tem-nao-lidas', dados.nao_lidas > 0);
            sino.setAttribute('aria-label', `Notificações: ${dados.nao_lidas} não lidas`);
            status.textContent = `${dados.nao_lidas} não lida(s)`;
            desenhar(dados.itens);
            let lembrado = ultimoId;
            try { lembrado = Math.max(lembrado, Number(sessionStorage.getItem(chave)) || 0); } catch (_) { /* Storage opcional. */ }
            avisar(dados.novas.filter((aviso) => aviso.id > lembrado));
            lembrar(dados.ultimo_id);
            erro.hidden = true;
        } catch (_) {
            erro.textContent = 'Não foi possível atualizar agora. Tentaremos novamente em instantes.';
            erro.hidden = false;
        } finally {
            if (requisicao === versao) ocupado = false;
        }
    };

    lista.addEventListener('submit', async (evento) => {
        const form = evento.target.closest('.notificacao-ler');
        if (!form) return;
        evento.preventDefault();
        const botao = form.querySelector('button');
        botao.disabled = true;
        try {
            const resposta = await fetch(form.action, {
                method: 'POST', credentials: 'same-origin', cache: 'no-store',
                headers: { Accept: 'application/json' }, body: new FormData(form),
            });
            if (resposta.redirected || resposta.status === 401) { ativo = false; throw new Error(); }
            if (!resposta.ok) throw new Error();
            sino.focus();
            await atualizar();
        } catch (_) {
            erro.textContent = 'Não foi possível marcar como lida. Tente novamente ou abra a central.';
            erro.hidden = false;
        } finally { botao.disabled = false; }
    });
    menu.addEventListener('toggle', () => { if (menu.open) atualizar(); });
    document.addEventListener('click', (evento) => {
        if (menu.open && !widget.contains(evento.target)) menu.open = false;
    });
    document.addEventListener('keydown', (evento) => {
        if (evento.key === 'Escape' && menu.open) { menu.open = false; sino.focus(); }
    });
    document.addEventListener('visibilitychange', () => { if (!document.hidden) atualizar(); });
    window.addEventListener('focus', () => { if (!document.hidden && !ocupado) atualizar(); });
    toast.querySelector('button').addEventListener('click', () => { toast.hidden = true; });
    setInterval(() => { if (!document.hidden && !ocupado) atualizar(); }, 15000);
    if (!document.hidden) atualizar();
})();
