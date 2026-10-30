#!/usr/bin/env bash
# Coleta e números do Relatório Diário do Comercial (Verdes Plantas). Só leitura no DKW.
# Uso: rodar_edicao.sh [AAAA-MM-DD] [dados_anterior.json]   (padrão: dia útil anterior)
# Gera em $TPR_OUT/<dia>: dados.json (todas as seções) + arquivos brutos. A redação é feita pela sessão, seguindo a skill.
set -euo pipefail
cd "$(dirname "$0")"
DIA="${1:-$(python3 -c 'import datetime as d;t=d.date.today()-d.timedelta(days=1)
while t.weekday()>4: t-=d.timedelta(days=1)
print(t)')}"
ANT="${2:-}"
OUT="${TPR_OUT:-/tmp/tpr-tr}/$DIA"
FONES=""
if [ -n "$ANT" ] && [ -f "$ANT" ]; then
  FONES=$(python3 -I -c 'import json,sys;d=json.load(open(sys.argv[1]));print(",".join(sorted({f for p in d.get("pedidos_amanha",[]) for f in p.get("telefones",[])})))' "$ANT")
fi
NODE_PATH=$(npm root -g) node coletar.js "${DIA}T03:00:00Z" "$OUT" | grep -E '^\{|ERRO' || true
test -f "$OUT/meta.json"
NODE_PATH=$(npm root -g) node coletar_edicao.js "$DIA" "$OUT" "$FONES" | grep -E '^\{|ERRO' || true
test -f "$OUT/meta_edicao.json"
python3 -I dados_edicao.py "$OUT" "$DIA" ${ANT:+"$ANT"} > "$OUT/dados.json"
# pendências (PDF à parte, desde 30/10): conversas abertas + contatos, e a lista acumulada
NODE_PATH=$(npm root -g) node coletar_pendencias.js "$OUT" | grep -E '^\{|ERRO' || true
test -f "$OUT/meta_pendencias.json"
PANT=$(ls -1 ../../relatorios/pendencias/pendencias_*.json 2>/dev/null | grep -v "_$DIA" | tail -1 || true)
python3 -I pendencias.py "$OUT" "$DIA" ${PANT:+"$PANT"} > "$OUT/pendencias.json"
mkdir -p ../../relatorios/pendencias && cp "$OUT/pendencias.json" "../../relatorios/pendencias/pendencias_$DIA.json"
python3 -I pendencias.py --md "$OUT/pendencias.json" > "../../relatorios/pendencias/Pendencias_Comercial_$DIA.md"
echo "$OUT/dados.json"
