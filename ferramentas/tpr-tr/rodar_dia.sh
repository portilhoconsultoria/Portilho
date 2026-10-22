#!/usr/bin/env bash
# TPR/TR diário da Verdes Plantas. Uso: rodar_dia.sh [AAAA-MM-DD]  (padrão: dia útil anterior)
# Gera relatorio_<dia>.md, Tempo_de_Resposta_Verdes_Plantas_<dd-mm>.pdf/.docx e email.html em $TPR_OUT/<dia>.
# Requer: VP_ROBO_EMAIL/VP_ROBO_SENHA (login do painel), Playwright global, Chromium em /opt/pw-browsers.
set -euo pipefail
cd "$(dirname "$0")"
DIA="${1:-$(python3 -c 'import datetime as d;t=d.date.today()-d.timedelta(days=1)
while t.weekday()>4: t-=d.timedelta(days=1)
print(t)')}"
OUT="${TPR_OUT:-/tmp/tpr-tr}/$DIA"
NODE_PATH=$(npm root -g) node coletar.js "${DIA}T03:00:00Z" "$OUT" | grep -E '^\{|ERRO' || true
test -f "$OUT/meta.json"
MODO=estrito python3 -I relatorio_tpr_tr.py "$OUT" "$DIA" "$DIA" > "$OUT/relatorio_$DIA.md"
BASE="$OUT/Tempo_de_Resposta_Verdes_Plantas_$(date -d "$DIA" +%d-%m)"
python3 -I gerar_doc.py "$OUT/relatorio_$DIA.md" "$BASE" >/dev/null
python3 -I md_html.py "$OUT/relatorio_$DIA.md" > "$OUT/email.html"
ls "$OUT"/relatorio_$DIA.md "$BASE".pdf "$BASE".docx "$OUT/email.html"
