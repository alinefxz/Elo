# Perfis privados do Elo

O endereço `/perfil/` resolve o papel da conta autenticada. `OBSERVADOR` continua
sendo o valor do usuário comum no banco; nenhum papel foi renomeado ou migrado.
O login abre o perfil correspondente. Um `next` local continua sendo respeitado
pelo Django, e a página de destino aplica suas próprias permissões.

| Papel | Dados editáveis e recursos |
| --- | --- |
| Usuário comum | Dados pessoais, contato, localização, solicitações próprias e notificações. |
| Doador | Dados pessoais, tipo sanguíneo declarado, triagens, solicitações e autorização de alertas. |
| Receptor | Dados pessoais, tipo sanguíneo declarado, solicitações e seus status. |
| Hemocentro | Nome institucional, contato, endereço, localização e funcionamento; validação, histórico institucional e gestão quando aprovado. |
| Administrador | Dados da conta e atividades administrativas próprias; ferramentas de gestão conforme papel e permissões Django. |

Documentos, papel, permissões e situação de aprovação não são editáveis no perfil.
O tipo sanguíneo confirmado pelo hemocentro é protegido inclusive contra
confirmação concorrente durante a edição. A gravação parcial preserva dados
protegidos e campos não alterados. Alterar o e-mail invalida sua verificação.
Alterar a senha exige a senha atual, usa os validadores existentes e mantém a
sessão da própria conta.

## Autorização e privacidade

`accounts/permissoes.py` fornece as capacidades compartilhadas pelos menus e
pelas páginas de perfil. Os serviços existentes continuam validando publicação,
estoque e moderação no servidor. A aprovação institucional é exigida para o
hemocentro gerenciar estoques e analisar pedidos. Ter `is_staff` isoladamente
não concede aprovação institucional nem o papel de administrador.

O perfil nunca recebe um identificador de proprietário: usa `request.user`.
Históricos e avisos são consultados por esse proprietário. O histórico combina
fontes com paginação e evita carregar todos os registros. A área administrativa
do perfil mostra somente atividades próprias, sem metadados ou respostas
clínicas; as consultas gerais ficam nas ferramentas administrativas autorizadas.
As páginas privadas não são armazenadas em cache.

O Django Admin permanece separado do perfil. O link exige staff e permissão no
aplicativo; links de usuários e auditoria também exigem as permissões específicas.
Não são concedidas novas permissões, grupos ou flags a contas existentes.

## Triagens e notificações

Somente doadores realizam triagens, conforme a regra existente. As modalidades
simplificada e extensa continuam independentes, com registros, progresso e
resultados próprios. Outros papéis não recebem acesso a respostas clínicas.

Além das convocações existentes, avisos persistentes são gerados por eventos reais:

- novo cadastro institucional: administradores ativos;
- decisão institucional: hemocentro analisado;
- nova solicitação: hemocentro de destino;
- mudança de status da solicitação: solicitante autenticado.

Os avisos acompanham as transações: uma falha não deixa notificações de uma
operação que foi revertida. As mensagens não copiam dados clínicos. O sino,
a central e a leitura por POST continuam usando a infraestrutura existente.

## Banco e arquivos

A migration `0017_usuario_dados_institucionais` adiciona somente `endereco` e
`horario_funcionamento`, opcionais. Ela não exclui ou reescreve registros e foi
aplicada ao PostgreSQL local durante esta entrega.

Implementação principal: `perfil_forms.py`, `perfil_views.py`, `perfis.py`,
`permissoes.py`, `notificacoes_eventos.py`, templates `perfil*.html`, include
`perfil_campo.html` e `perfil.css`. Integrações em URLs, configurações, menu,
admin, auditoria, cadastro e serviços de validação.

Na verificação dos caminhos do perfil foram corrigidos o template de
`minhas_solicitacoes.html` e o widget de sugestões de municípios. Testes antigos
foram alinhados às regras já existentes de solicitações por doadores/observadores
e ao acesso condicionado ao Django Admin.

O catálogo local oficial do IBGE contém 5.571 municípios nas 27 UFs, com fonte e
data registradas em `accounts/data/municipios_ibge.json`. A busca de municípios
funciona por estado em cadastro, perfil e solicitações, sem depender da API
externa durante o preenchimento. O servidor rejeita pares incompatíveis. Dados
legados do perfil são preservados quando a localização não é editada.
O importador de atualização fica em `scripts/importar_municipios_ibge.py`.

## Validação

`accounts/test_perfis.py` cobre os cinco papéis: login, edição, persistência,
menus, redirecionamentos, notificações, histórico paginado, CSRF, senha,
isolamento, tentativas de elevar privilégios, concorrência e eventos reais.

Execute os testes sem usar o banco de dados da aplicação:

```powershell
python manage.py test --settings=config.settings_test
python manage.py check --settings=config.settings_test
python manage.py makemigrations --check --dry-run --settings=config.settings_test
```

A revisão visual usou contas sintéticas em SQLite isolado e telas de computador,
tablet e celular. As imagens de QA estão em `output/perfis/`.

Resultado final: **231 testes aprovados**, incluindo 45 regressões de perfis e
14 de localidades. A suíte completa usou SQLite e hash simplificado somente
no processo de testes; os validadores de senha foram mantidos. `check`,
`makemigrations --check --dry-run` e `git diff --check` também passaram.

## Limitações existentes

Não há modelo de doações ou recebimentos efetivados; o perfil informa essa
ausência e não trata triagens, solicitações ou entradas de estoque como doações.
Não há armazenamento de fotos; o perfil usa avatar com inicial ou ícone
institucional. Nenhuma conta, triagem ou consentimento sintético foi inserido
no PostgreSQL real durante a revisão visual.

O launcher de `.venv/Scripts/python.exe` aponta a um Python removido. A execução
desta entrega usou o Python fornecido pelo aplicativo com os pacotes locais.
Para PostgreSQL, o driver puro do psycopg utilizou a libpq já instalada no
PostgreSQL 18; nenhuma configuração permanente do ambiente foi alterada.
