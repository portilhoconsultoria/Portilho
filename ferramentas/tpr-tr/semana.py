"""Números da análise semanal do comercial (Verdes Plantas) num JSON.

Entrada: <dir> com cards.json + mensagens.json (coletar.js desde <ini>) e negocios.json, agendamentos.json,
notas.json, contatos.json (coletar_semana.js). Opcional: dados_edicao_*.json diários (séries de carga e movimento).

Uso: python3 -I semana.py <dir> <ini AAAA-MM-DD> <fim AAAA-MM-DD inclusive> [dados_diarios.json ...] > semana.json

Limites da base (declarar no relatório):
- negocios.json é uma foto do momento da coleta: "moved" é só a ÚLTIMA movimentação do card. Card movido na
  semana e de novo depois dela some da contagem da semana. Para movimento e carga dia a dia, valem os
  dados_edicao diários quando existem.
- A coorte (cards criados na semana) é lida com o resultado de hoje, não com o do fim da semana.
"""
import json
import os
import re
import statistics as st
import sys
from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tpr_tr  # noqa: E402
from dados_edicao import S, ENCERRA, ATIVAS, TAG_TIPO, DATA, VENDA, PERDA, nome, ts, BRT  # noqa: E402


def dia(s):
    return ts(s).date().isoformat() if s else None


def main(d, ini, fim, diarios):
    ld = lambda f: json.load(open(os.path.join(d, f)))
    N, AG, NT, C, CARDS = ld("negocios.json"), ld("agendamentos.json"), ld("notas.json"), ld("contatos.json"), ld("cards.json")
    meta = ld("meta_semana.json")
    d0 = datetime.fromisoformat(ini).date()
    d1 = datetime.fromisoformat(fim).date()
    dias = [(d0 + timedelta(days=i)).isoformat() for i in range((d1 - d0).days + 1)]
    na = lambda s: bool(s) and d0.isoformat() <= dia(s) <= d1.isoformat()
    A = [o for o in N if o["step"] in S]
    out = {"ini": ini, "fim": fim, "coleta": ts(meta["coletadoEm"]).strftime("%d/%m/%Y %H:%M"),
           "volume": {"negocios": len(N), "agendamentos": len(AG), "notas": sum(len(v) for v in NT.values()),
                      "cards_com_mensagem": len(CARDS), "mensagens": sum(len(v) for v in ld("mensagens.json").values())}}

    # 1. entrada: cards criados por dia e por vendedor
    novos = [o for o in A if na(o["createdAt"])]
    out["entrada"] = {"total": len(novos), "por_dia": {x: sum(1 for o in novos if dia(o["createdAt"]) == x) for x in dias},
                      "por_vendedor": Counter(nome(o["userId"]) for o in novos).most_common()}

    # 2. coorte: o que aconteceu com os cards criados na semana (resultado na data da coleta)
    def destino(o):
        if o["step"] == 32318:
            return "venda" if o["status"] == "WON" else "venda (arrastada)"
        if o["status"] == "WON":
            return "venda (fora da coluna)"
        return {36613: "perdida", 121919: "não comercial", 44334: "incógnita"}.get(o["step"], "em aberto · " + S[o["step"]])
    coorte = Counter(destino(o) for o in novos)
    tf = [(ts(o["moved"]) - ts(o["createdAt"])).total_seconds() / 86400 for o in novos
          if o["step"] in ENCERRA and o["moved"] and o["createdAt"]]
    porv = defaultdict(Counter)
    for o in novos:
        porv[nome(o["userId"])][destino(o).split(" ·")[0]] += 1
    out["coorte"] = {"destino": coorte.most_common(), "dias_ate_encerrar_mediana": round(st.median(tf), 1) if tf else None,
                     "por_vendedor": {k: dict(v) for k, v in porv.items()},
                     "valor_vendido": round(sum(float(o["amount"] or 0) for o in novos if o["status"] == "WON"), 2)}

    # 3. encerramentos da semana (última movimentação dentro da semana para coluna de encerramento)
    fech = [o for o in A if o["step"] in ENCERRA and na(o["moved"])]
    acoes = [o for o in fech if o["status"] not in (None, "OPEN")]
    ef = [o for o in fech if o["step"] == 32318]
    pe = [o for o in fech if o["step"] == 36613]
    out["encerramentos"] = {
        "total": len(fech), "por_acoes": len(acoes),
        "por_dia": {x: [sum(1 for o in fech if dia(o["moved"]) == x), sum(1 for o in acoes if dia(o["moved"]) == x)] for x in dias},
        "por_vendedor": {v: [sum(1 for o in fech if nome(o["userId"]) == v), sum(1 for o in acoes if nome(o["userId"]) == v)]
                         for v in sorted({nome(o["userId"]) for o in fech})},
        "por_coluna": Counter(S[o["step"]] for o in fech).most_common(),
        "vendas": len(ef), "vendas_ok": sum(1 for o in ef if o["status"] == "WON" and o["amount"]),
        "valor_vendas_ok": round(sum(float(o["amount"] or 0) for o in ef if o["status"] == "WON"), 2),
        "vendas_por_vendedor": Counter(nome(o["userId"]) for o in ef if o["status"] == "WON").most_common(),
        "perdas": len(pe), "perdas_com_motivo": sum(1 for o in pe if o["lostReason"]),
        "motivos_perda": Counter((o["lostReason"] or "").strip().lower()[:60] for o in pe if o["lostReason"]).most_common(15),
        "incognita": sum(1 for o in fech if o["step"] == 44334),
        "incognita_ganho": sum(1 for o in fech if o["step"] == 44334 and o["status"] == "WON")}

    # 4. follow-up: agendamentos criados na semana, por vendedor e por dia
    agw = [a for a in AG if na(a["createdAt"])]
    out["agendamentos"] = {"criados": len(agw), "por_dia": {x: sum(1 for a in agw if dia(a["createdAt"]) == x) for x in dias},
                           "por_vendedor": Counter(nome(a["userId"]) for a in agw).most_common(),
                           "enviados_na_semana": sum(1 for a in AG if na(a["sentAt"]))}

    # 5. notas escritas na semana
    nw = [n for v in NT.values() for n in v if na(n["createdAt"])]
    out["notas"] = {"total": len(nw), "com_data": sum(1 for n in nw if DATA.search(n["body"] or "")),
                    "por_autor": {a: [c, sum(1 for n in nw if nome(n["userId"]) == a and DATA.search(n["body"] or ""))]
                                  for a, c in Counter(nome(n["userId"]) for n in nw).most_common()},
                    "por_dia": {x: sum(1 for n in nw if dia(n["createdAt"]) == x) for x in dias}}

    # 6. tempo de resposta: dia a dia e semana (expediente seg–sex) + sábado em hora corrida
    td = {}
    for x in dias:
        if datetime.fromisoformat(x).weekday() > 4:
            continue
        ev, fora, _ = tpr_tr.main(d, x, x)
        td[x] = tpr_tr.resumo(ev)
    evw, foraw, _ = tpr_tr.main(d, dias[0], min(dias[-1], dias[4]))
    out["tempo_resposta"] = {"por_dia": td, "semana": tpr_tr.resumo(evw), "fora_expediente": dict(foraw)}
    # por hora de chegada (TPR da semana): mediana por faixa
    hora = defaultdict(list)
    for kpi, v, mins, _, _, ab, chegada in evw:
        if kpi == "TPR" and mins is not None:
            hora[chegada.hour].append(mins)
    out["tempo_resposta"]["tpr_por_hora"] = {h: [len(v), round(st.median(v), 1)] for h, v in sorted(hora.items())}
    # sábado: só volume (o horário de sábado não foi informado; não há relógio de expediente)
    sab = [x for x in dias if datetime.fromisoformat(x).weekday() == 5]
    M = ld("mensagens.json")
    sm = Counter()
    for ms in M.values():
        for m in ms:
            if sab and dia(m["at"]) in sab:
                sm["cliente" if not m["fromMe"] else (nome(m["userId"]) if m["userId"] else "automação")] += 1
    out["sabado"] = {"dias": sab, "mensagens": sm.most_common()}

    # 7. classificação: cards criados na semana com tag de tipo (tags atuais do card)
    cw = {}
    for c in CARDS:
        if na(c["createdAt"]):
            cw[c["id"]] = c
    tagv = defaultdict(lambda: [0, 0])
    for c in cw.values():
        v = nome(c["userId"]); tagv[v][0] += 1
        if any(t in TAG_TIPO for t in c.get("orderTags") or []):
            tagv[v][1] += 1
    neg = {o["id"]: o for o in N}
    conv_tag = defaultdict(lambda: [0, 0, 0.0])
    for c in cw.values():
        tipo = [t for t in c.get("orderTags") or [] if t in TAG_TIPO] or ["(sem tag de tipo)"]
        o = neg.get(c["id"]) or {}
        for t in tipo:
            conv_tag[t][0] += 1
            if o.get("status") == "WON":
                conv_tag[t][1] += 1; conv_tag[t][2] += float(o.get("amount") or 0)
    out["tags"] = {"cards_criados_com_mensagem": len(cw), "com_tag_tipo": sum(v[1] for v in tagv.values()),
                   "por_vendedor": dict(tagv),
                   "por_tag": sorted(([k, v[0], v[1], round(v[2], 2)] for k, v in conv_tag.items()), key=lambda r: -r[1])}

    # 8. carga: série dos diários + foto atual
    serie = {}
    for f in diarios:
        x = json.load(open(f))
        serie.update((x.get("s8_carga") or {}).get("serie") or {})
    out["carga"] = {"serie": serie, "agora": Counter(nome(o["userId"]) for o in A if o["step"] in ATIVAS).most_common()}

    # 9. movimento: série dos diários (fonte mais fiel que a foto)
    mov = {}
    for f in diarios:
        x = json.load(open(f))
        mov[x["dia"]] = (x.get("s1_movimento") or {}).get("total")
    out["movimento_diarios"] = mov
    return out


if __name__ == "__main__":
    print(json.dumps(main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4:]), ensure_ascii=False, indent=1, default=str))
