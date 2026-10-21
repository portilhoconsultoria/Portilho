# TPR/TR — Verdes Plantas

Coleta só leitura no painel DKW (gestao.portilhoconsultoria.com.br), personificando a Verdes Plantas (7078).
A personificação é desfeita ao final. O token do painel nunca sai da página.

- `rodar_dia.sh [AAAA-MM-DD]` — relatório do dia (padrão: dia útil anterior).
- `coletar.js <desde ISO> <dir>` — cards do funil 10541 com mensagem desde a data + histórico de cada ticket.
- `tpr_tr.py` — cálculo (definições no topo do arquivo). `MODO=amplo` conta respostas pelo celular.
- `relatorio_tpr_tr.py` — markdown.

Definições: `kpis-atendimento-comercial-verdes-plantas.md` (vault). Rotas: `wiki/entities/dkw-api.md`.
