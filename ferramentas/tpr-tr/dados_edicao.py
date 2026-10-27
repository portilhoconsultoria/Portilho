"""Números de todas as seções do Relatório Diário do Comercial (Verdes Plantas) num JSON.

Entrada: <dir> com negocios.json, agendamentos.json, notas.json, contatos.json, acompanhar.json, meta_edicao.json
(coletar_edicao.js) e cards.json, mensagens.json, meta.json (coletar.js, para TPR/TR e tags).
Opcional: dados.json da edição anterior (séries dia a dia e pedidos de ontem).

Uso: python3 -I dados_edicao.py <dir> <dia AAAA-MM-DD> [dados_anterior.json] > dados.json
Definições: skill relatorio-comercial-vp (seção 5) e kpis-atendimento-comercial-verdes-plantas.md.
"""
import json
import os
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tpr_tr  # noqa: E402

BRT = timezone(timedelta(hours=-3))
S = {44341: "Atendimento Inicial", 69421: "Atendimento de Vendedores", 36971: "Follow-up 1", 113074: "Follow-up 2",
     32318: "Venda Efetivada", 36613: "Venda Perdida", 121919: "Não Comercial", 44334: "Incógnita"}
ENCERRA = (32318, 36613, 121919, 44334)
ATIVAS = (44341, 69421, 36971, 113074)
U = tpr_tr.USUARIOS
TAG_TIPO = {"BUQUES", "GRAMA", "FLOR DE PRESENTE", "FLOR DE CORTE", "PLANTAS ORMAMENTAIS", "PLANTAS ORNAMENTAIS",
            "FRUTÍFERAS", "ARVORES DE SOMBRA", "PALMEIRA", "CEDROS", "EUCALIPTO", "TREPADEIRA", "FORRAÇÃO", "PEDRA",
            "TERRA / SUBSTRATO", "VASOS", "CESTA DE CAFÉ", "PAISAGISMO", "FOLHAGENS", "ADUBOS", "OUTROS"}
VENDA = re.compile(r"j[aá] fez o pedido|fez o pedido|comprou|vem buscar|vai vir|vai passar|passar na loja|entregamos|"
                   r"veio na loja|veio at[eé] a loja|pagou", re.I)
PERDA = re.compile(r"achou caro|\bcaro\b|frete|outra cidade|desistiu|n[aã]o vai querer|mais barato|n[aã]o temos|n[aã]o tinha", re.I)
DATA = re.compile(r"\b\d{1,2}/\d{1,2}\b|\bdia \d{1,2}\b|amanh|segunda|ter[cç]a|quarta|quinta|sexta|s[aá]bado|"
                  r"semana que vem|pr[oó]xima semana", re.I)


def ts(s):
    return datetime.fromisoformat(s.replace("Z", "+00:00")).astimezone(BRT) if s else None


def nome(uid):
    return U.get(uid, f"user {uid}") if uid else "sem dono"


def main(d, dia, anterior=None):
    ld = lambda f: json.load(open(os.path.join(d, f)))
    N, AG, NT, C, ACP = ld("negocios.json"), ld("agendamentos.json"), ld("notas.json"), ld("contatos.json"), ld("acompanhar.json")
    meta_e = ld("meta_edicao.json")
    prev = json.load(open(anterior)) if anterior and os.path.exists(anterior) else {}
    d0 = datetime.fromisoformat(dia).replace(tzinfo=BRT)
    d1 = d0 + timedelta(days=1)
    hoje = lambda s: bool(s) and d0 <= ts(s) < d1
    corte = ts(meta_e["coletadoEm"])
    A = [o for o in N if o["step"] in S]

    def ct(o):
        c = C.get(str(o["contactId"])) or {}
        return c.get("name") or "(sem nome)", c.get("number") or ""

    def nota(o):
        v = sorted(NT.get(str(o["id"])) or [], key=lambda n: n["createdAt"])
        return (v[-1]["body"] if v else "").replace("\n", " ").strip()

    def linha(o, extra=None):
        n, f = ct(o)
        r = {"vendedor": nome(o["userId"]), "cliente": n, "telefone": f, "valor": o["amount"], "status": o["status"], "nota": nota(o)[:160]}
        r.update(extra or {})
        return r

    mov = [o for o in A if hoje(o["moved"])]
    out = {"dia": dia, "coleta": corte.strftime("%d/%m/%Y %H:%M"), "volume": {
        "negocios": meta_e["negocios"], "agendamentos": meta_e["agendamentos"],
        "notas_lidas": sum(len(v) for v in NT.values())}}

    # 1. movimento
    out["s1_movimento"] = {"total": len(mov), "por_destino": Counter(S[o["step"]] for o in mov).most_common(),
                           "anterior_total": (prev.get("s1_movimento") or {}).get("total")}

    # 2. encerramentos
    fech = [o for o in mov if o["step"] in ENCERRA]
    por_acoes = [o for o in fech if o["status"] not in (None, "OPEN")]
    ef = [o for o in mov if o["step"] == 32318]
    ef_ruim = [linha(o, {"problema": ("arrastada" if o["status"] != "WON" else "") + (" sem valor" if not o["amount"] else "")})
               for o in ef if o["status"] != "WON" or not o["amount"]]
    pe = [o for o in mov if o["step"] == 36613]
    pe_ruim = []
    for o in pe:
        if not o["lostReason"]:
            gemeo = any(x["contactId"] == o["contactId"] and x["id"] != o["id"] and x["step"] == 36613 and x["lostReason"] for x in A)
            pe_ruim.append(linha(o, {"duplicado_com_card_certo": gemeo}))
    inc = []
    for o in mov:
        if o["step"] == 44334:
            n = nota(o)
            if o["status"] == "WON" or VENDA.search(n) or PERDA.search(n):
                inc.append(linha(o, {"sinal": "ganho marcado" if o["status"] == "WON" else ("venda" if VENDA.search(n) else "perda")}))
    acum = {"perdida_sem_motivo": sum(1 for o in A if o["step"] == 36613 and not o["lostReason"]),
            "efetivada_sem_valor": sum(1 for o in A if o["step"] == 32318 and not o["amount"]),
            "ganho_status_won_fora_da_efetivada": sum(1 for o in A if o["status"] == "WON" and o["step"] != 32318)}
    serie = dict((prev.get("s2_encerramentos") or {}).get("serie_acumulado") or
                 {"18/10": {"perdida_sem_motivo": 1093, "efetivada_sem_valor": 448},
                  "20/10": {"perdida_sem_motivo": 1093, "efetivada_sem_valor": 448}})
    serie[d0.strftime("%d/%m")] = acum
    out["s2_encerramentos"] = {"encerramentos": len(fech), "por_acoes": len(por_acoes), "arrastados": len(fech) - len(por_acoes),
                               "vendas": len(ef), "vendas_problema": ef_ruim, "perdas": len(pe), "perdas_sem_motivo": pe_ruim,
                               "incognita_com_sinal": inc, "acumulado": acum, "serie_acumulado": serie}

    # 3. follow-up × agendamento
    fu = [o for o in A if o["step"] in (36971, 113074)]
    pend = [a for a in AG if not a["sentAt"] and a["sendAt"] and ts(a["sendAt"]) > corte]
    cp = {a["contactId"] for a in pend}
    com = sum(1 for o in fu if o["contactId"] in cp)
    s3 = dict((prev.get("s3_followup") or {}).get("serie") or {"20/10": {"fu": 71, "com_agendamento": 2}})
    s3[d0.strftime("%d/%m")] = {"fu": len(fu), "com_agendamento": com}
    out["s3_followup"] = {"cards_fu": len(fu), "com_agendamento": com, "sem": len(fu) - com,
                          "pendentes_base": len(pend), "historico_base": len(AG), "serie": s3}

    # 4. notas do dia (nos cards movidos no dia)
    nd = [n for o in mov for n in (NT.get(str(o["id"])) or []) if hoje(n["createdAt"])]
    out["s4_notas"] = {"total": len(nd), "por_autor": Counter(nome(n["userId"]) for n in nd).most_common(),
                       "com_data": [{"autor": nome(n["userId"]), "texto": n["body"][:120]} for n in nd if DATA.search(n["body"] or "")]}

    # 5. coluna atendimento
    at = [o for o in A if o["step"] in (44341, 69421)]
    out["s5_coluna"] = {"por_coluna": [(S[s], sum(1 for o in A if o["step"] == s)) for s in ATIVAS],
                        "atendimento": len(at), "dormiram": sum(1 for o in at if o["moved"] and ts(o["moved"]) < d0)}

    # 6. tempo de resposta
    ev, fora, meta_t = tpr_tr.main(d, dia, dia)
    out["s6_tempo_resposta"] = {"resumo": tpr_tr.resumo(ev), "fora_expediente": dict(fora),
                                "mensagens_lidas": meta_t["mensagens"], "meta_tpr_min": 4, "proposta_tr_min": 15}

    # 7. classificação por tag (cards criados no dia)
    cards = ld("cards.json")
    novos = [c for c in cards if hoje(c["createdAt"])]
    vistos, base = set(), []
    for c in novos:
        if c["id"] not in vistos:
            vistos.add(c["id"]); base.append(c)
    porv = defaultdict(lambda: {"iniciados": 0, "com_tag_tipo": 0, "tags": Counter()})
    sem = []
    for c in base:
        v = nome(c["userId"]); tipo = [t for t in c.get("orderTags") or [] if t in TAG_TIPO]
        porv[v]["iniciados"] += 1
        porv[v]["tags"].update(c.get("orderTags") or [])
        if tipo:
            porv[v]["com_tag_tipo"] += 1
        else:
            sem.append({"vendedor": v, "cliente": c["contact"], "telefone": c.get("number"), "coluna": S.get(c["step"]),
                        "tag_do_contato": c.get("contactTags") or []})
    out["s7_tags"] = {"iniciados": len(base), "com_tag_tipo": sum(1 for c in base if any(t in TAG_TIPO for t in c.get("orderTags") or [])),
                      "por_vendedor": {k: {**v, "tags": v["tags"].most_common()} for k, v in porv.items()},
                      "tags_mais_usadas": Counter(t for c in base for t in c.get("orderTags") or []).most_common(),
                      "sem_tag_de_tipo": sem[:40], "tag_paisagismo_existe": False}

    # 8. carga
    ativos = [o for o in A if o["step"] in ATIVAS]
    carga = Counter(nome(o["userId"]) for o in ativos)
    s8 = dict((prev.get("s8_carga") or {}).get("serie") or {})
    s8[d0.strftime("%d/%m")] = dict(carga)
    out["s8_carga"] = {"ativos": len(ativos), "por_vendedor": carga.most_common(), "serie": s8}

    # 9. o que pedi ontem (situação dos contatos acompanhados)
    sit = []
    for f, ids in ACP.items():
        for o in [o for o in N if o["contactId"] in ids]:
            sit.append({"telefone": f, "cliente": ct(o)[0], "vendedor": nome(o["userId"]), "coluna": S.get(o["step"], o["step"]),
                        "status": o["status"], "valor": o["amount"], "motivo_perda": o["lostReason"]})
    out["s9_pedidos_ontem"] = {"pedidos_anteriores": prev.get("pedidos_amanha") or [], "situacao": sit}
    out["pedidos_amanha"] = []  # a sessão que redige preenche com os pedidos (texto + telefones) antes de salvar
    return out


if __name__ == "__main__":
    print(json.dumps(main(*sys.argv[1:4]), ensure_ascii=False, indent=1, default=str))
