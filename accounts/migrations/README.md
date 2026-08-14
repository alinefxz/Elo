# Como as migrations funcionam

Esta pasta guarda o historico da estrutura do banco de dados. Pense nela como
uma lista numerada de alteracoes que o Django executa na ordem.

## Historico atual

- `0001_initial.py`: criou as tabelas iniciais, incluindo os campos completos
  do usuario e a tabela de consentimentos;
- `0002_remove_usuario_cidade_remove_usuario_cnpj_and_more.py`: registrou uma
  simplificacao temporaria do model;
- `0003_usuario_cidade_usuario_cnpj_usuario_cpf_and_more.py`: restaurou os
  campos completos quando ficou definido que a funcionalidade deveria ser
  mantida, mas explicada de maneira mais simples.

As migrations `0002` e `0003` devem continuar no projeto. Embora uma retire e a
outra recoloque campos, elas representam o que realmente aconteceu no banco.
Apagar ou reescrever uma migration ja aplicada pode deixar o codigo e o banco
em estados diferentes.

## Comandos usados

Depois de alterar `models.py`, o fluxo correto e:

```powershell
python manage.py makemigrations
python manage.py migrate
```

`makemigrations` compara o model atual com o ultimo estado conhecido e cria um
novo arquivo numerado. Ele prepara a alteracao, mas ainda nao mexe nas tabelas.

`migrate` le os arquivos numerados e executa no PostgreSQL os comandos SQL
necessarios. O Django registra o que ja foi aplicado na tabela interna
`django_migrations`, evitando executar a mesma migration duas vezes.

Em outro computador, depois de clonar o repositorio e configurar o `.env`, a
pessoa precisa executar somente:

```powershell
python manage.py migrate
```

O Django aplicara automaticamente todas as migrations que ainda estiverem
pendentes.

## Relacao com o codigo

- `models.py` descreve como as tabelas devem estar na versao atual;
- as migrations descrevem o caminho usado para chegar a essa versao;
- o PostgreSQL guarda as tabelas e os dados reais;
- o ORM do Django transforma chamadas Python em consultas SQL.

Exemplo: `Usuario.objects.filter(email=email)` vira uma consulta `SELECT` na
tabela `usuarios`. `usuario.save()` pode virar `INSERT` ou `UPDATE`, dependendo
de o objeto ser novo ou ja existir.

Operacoes comuns em uma migration:

- `CreateModel`: cria uma tabela;
- `AddField`: adiciona uma coluna;
- `RemoveField`: remove uma coluna;
- `AlterField`: altera uma coluna;
- `AddConstraint`: cria uma regra no banco, como uma combinacao unica.

Os arquivos numerados sao gerados pelo Django e normalmente nao devem receber
comentarios manuais. Este README explica a logica da pasta sem modificar o
historico executavel.
