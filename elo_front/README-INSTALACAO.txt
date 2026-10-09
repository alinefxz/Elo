ELO — FRONTEND VISUAL

Arquivos incluídos:
- templates/base.html
- templates/accounts/inicio.html
- static/css/elo.css

Como instalar:
1. Faça backup dos arquivos atuais.
2. Copie base.html para:
   templates/base.html
3. Copie inicio.html para:
   templates/accounts/inicio.html
4. Copie elo.css para:
   static/css/elo.css
5. Execute:
   python manage.py runserver

Observações:
- O frontend usa as URLs existentes do app accounts.
- Não altera models.py, views.py ou urls.py.
- A seção de estoque usa estoque_geral que já é enviado pela view inicio.
- O CSS também fornece estilo base para formulários das outras telas.
