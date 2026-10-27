#!/usr/bin/env bash
# Coleta e números da análise semanal do comercial (Verdes Plantas). Só leitura no DKW.
# Uso: rodar_semana.sh <segunda AAAA-MM-DD> <último dia AAAA-MM-DD>
# Gera em $TPR_OUT/semana_<segunda>: semana.json + arquivos brutos. A redação é feita pela sessão (proposta em relatorios/semanal/).
set -euo pipefail
cd "$(dirname "$0")"
INI="$1"; FIM="$2"
AMANHA=$(python3 -c "import datetime as d,sys;print(d.date.fromisoformat(sys.argv[1])+d.timedelta(days=1))" "$FIM")
OUT="${TPR_OUT:-/tmp/tpr-tr}/semana_$INI"
NODE_PATH=$(npm root -g) node coletar.js "${INI}T03:00:00Z" "$OUT" | grep -E '^\{|ERRO' || true
test -f "$OUT/meta.json"
NODE_PATH=$(npm root -g) node coletar_semana.js "$INI" "$AMANHA" "$OUT" | grep -E '^\{|ERRO' || true
test -f "$OUT/meta_semana.json"
grep -h empresaAoFinal "$OUT/meta.json" "$OUT/meta_semana.json"
DIARIOS=$(python3 -c "
import glob,os,sys
ini,fim=sys.argv[1],sys.argv[2]
for f in sorted(glob.glob('../../relatorios/diario/dados_edicao_*.json')):
    d=os.path.basename(f)[13:23]
    if ini<=d<=fim and 'semente' not in f: print(f)" "$INI" "$FIM")
python3 -I semana.py "$OUT" "$INI" "$FIM" $DIARIOS > "$OUT/semana.json"
echo "$OUT/semana.json"
