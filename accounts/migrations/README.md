# Como as migrations funcionam

Esta pasta guarda o histórico da estrutura do banco de dados.

- `0001_initial.py` foi gerada pelo Django e criou as tabelas iniciais.
- Novas alterações em `models.py` devem gerar um novo arquivo numerado.
- Uma migration aplicada não deve ser reescrita ou apagada.

Fluxo correto após alterar models:

```powershell
python manage.py makemigrations
python manage.py migrate
```

`makemigrations` compara os models atuais com o último estado conhecido e cria
as operações necessárias. `migrate` traduz essas operações em SQL e as executa
no PostgreSQL.

O Django registra migrations aplicadas na tabela `django_migrations`. Por isso,
editar manualmente `0001_initial.py` depois de aplicá-la poderia fazer o arquivo
deixar de representar o que realmente aconteceu no banco.

## Relação com o código

Os models são a definição atual das tabelas. As migrations são o caminho usado
para transformar uma versão antiga do banco na versão atual.

Exemplos de operações geradas:

- `CreateModel`: cria uma tabela;
- `AddField`: adiciona uma coluna;
- `RemoveField`: remove uma coluna;
- `AlterField`: muda uma coluna existente;
- `AddConstraint`: cria uma regra, como unicidade.

O arquivo `0001_initial.py` foi mantido sem comentários adicionais porque é um
arquivo automático e já aplicado. Esta documentação explica sua função sem
alterar o histórico.
