"""PROTÓTIPO — números do relatório de GERÊNCIA (Verdes Plantas) e do sinal diário da coordenação.

Desenho: comunicacoes/2026-11-24_Desenho_Relatorio_Gerencia_VP.md (v2). Regra de corte: só equipe e tendência —
nenhum nome de vendedor, telefone ou quebra por vendedor; grupos com menos de 5 casos não são publicados.

Entrada: <dir> da coleta semanal (rodar_semana.sh: negocios, cards, mensagens, notas, agendamentos, contatos),
         semana <ini> <fim>, e os arquivos de apoio do repositório (pendências diárias e dados_edicao diários).
Uso: python3 -I gerencia.py <dir> <ini AAAA-MM-DD> <fim AAAA-MM-DD> > gerencia.json
"""
import glob
import json
import os
import statistics as st
import sys
from collections import Counter, defaultdict
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dados_edicao import S, ENCERRA, ATIVAS, TAG_TIPO, ts  # noqa: E402

REPO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "relatorios")
COORD, DONO = 15948, 12152          # Douglas (coordenador), Fernando (dono)
# telefones da equipe (conversas internas pelo WhatsApp da loja) — CONFIRMAR a lista completa com o Jhonatan/Fernando
INTERNOS = {"5542999102910": "Edimar", "5542999589335": "Fernando (Financeiro Verdes Plantas)", "5542999902654": "Luana Loja"}
MIN_N = 5                           # mínimo de casos para publicar um grupo (vale também para totais/subtotais)


def dia(s):
    return ts(s).date().isoformat() if s else None


def pct(a, b):
    return round(100 * a / b) if b else None


def sinal_diario():
    """A1 por dia: % da lista da coordenação de ontem resolvida hoje (pendências diárias)."""
    arqs = sorted(f for f in glob.glob(os.path.join(REPO, "pendencias", "pendencias_*.json")))
    out, ant = [], None
    for f in arqs:
        d = json.load(open(f))
        if ant is not None:
            aberta_ontem = len(ant["itens"])
            out.append({"dia": d["dia"], "lista_ontem": aberta_ontem, "resolvidos": len(d["feitos_hoje"]),
                        "a1_pct": pct(len(d["feitos_hoje"]), aberta_ontem)})
        ant = d
    return out


def main(d, ini, fim):
    ld = lambda f: json.load(open(os.path.join(d, f)))
    N, CARDS, M, NT, AG = ld("negocios.json"), ld("cards.json"), ld("mensagens.json"), ld("notas.json"), ld("agendamentos.json")
    meta = ld("meta_semana.json")
    coleta = ts(meta["coletadoEm"])
    na = lambda s: bool(s) and ini <= dia(s) <= fim
    A = [o for o in N if o["step"] in S]
    out = {"semana": [ini, fim], "coleta": coleta.strftime("%d/%m/%Y %H:%M")}

    # ---------- A. rotina da coordenação
    sd = [x for x in sinal_diario() if ini <= x["dia"] <= fim]
    out["A1_lista_resolvida_24h"] = {"por_dia": sd, "media_pct": round(st.mean(x["a1_pct"] for x in sd)) if sd else None}
    out["A2_relatorio_lido_9h"] = "não medido: o relatório de coordenação ainda não vai para o coordenador"
    out["A3_reuniao_semanal"] = "não medido: falta o funil 'Rotina da coordenação'"

    # quem resolve as exceções: mensagens e notas do coordenador × do dono nos cards das listas de pendência da semana
    pend_cards = set()
    for f in glob.glob(os.path.join(REPO, "pendencias", "pendencias_*.json")):
        p = json.load(open(f))
        if ini <= p["dia"] <= fim:
            pend_cards |= {i["card"] for i in p["itens"]}
    tk_de = {c["id"]: c["ticketIds"] for c in CARDS}
    dono_card = {c["id"]: c["userId"] for c in CARDS}
    acoes = Counter()
    for cid in pend_cards:
        if dono_card.get(cid) in (COORD, DONO):   # card do próprio coordenador/dono é trabalho de venda, não de coordenação
            continue
        for t in tk_de.get(cid, []):
            for m in M.get(str(t), []):
                if m.get("fromMe") and m.get("userId") in (COORD, DONO) and na(m["at"]):
                    acoes["coord" if m["userId"] == COORD else "dono"] += 1
        for n in NT.get(str(cid), []):
            if n.get("userId") in (COORD, DONO) and na(n["createdAt"]):
                acoes["coord" if n["userId"] == COORD else "dono"] += 1
    out["divisao_excecoes"] = {"coordenador": acoes["coord"], "dono": acoes["dono"],
                               "pct_coordenador": pct(acoes["coord"], acoes["coord"] + acoes["dono"]),
                               "cards_na_lista": len(pend_cards)}

    # ---------- B. processo (equipe)
    tr = ld("semana.json")["tempo_resposta"]["semana"] if os.path.exists(os.path.join(d, "semana.json")) else None
    if tr:
        e1, e2 = tr["TPR"]["Equipe"], tr["TR"]["Equipe"]
        dias_uteis = sum(1 for x in ld("semana.json")["tempo_resposta"]["por_dia"])
        out["B1_sem_resposta"] = {"total_semana": e1["sem_resposta"]}
        out["B2_primeira_resposta"] = {"mediana_min": round(e1["mediana_min"], 1), "p90_min": round(e1["p90_min"])}
        out["resposta_na_conversa"] = {"mediana_min": round(e2["mediana_min"], 1), "p90_min": round(e2["p90_min"])}

    fech = [o for o in A if o["step"] in ENCERRA and na(o["moved"])]
    arrast = sum(1 for o in fech if o["status"] in (None, "OPEN"))
    sem_motivo = sum(1 for o in fech if o["step"] == 36613 and not o["lostReason"])
    # cliente como último a falar no momento do encerramento (cards com conversa coletada)
    card_de_neg = {c["id"]: c for c in CARDS}
    ultimo_cliente, lidos = 0, 0
    for o in fech:
        c = card_de_neg.get(o["id"])
        if not c:
            continue
        msgs = [m for t in c["ticketIds"] for m in M.get(str(t), []) if m["at"] <= o["moved"] and not (m.get("fromMe") and not m.get("userId"))]
        if not msgs:
            continue
        lidos += 1
        if not max(msgs, key=lambda m: m["at"]).get("fromMe"):
            ultimo_cliente += 1
    out["B3_encerramentos_fora_da_regra"] = {"encerramentos": len(fech), "arrastados": arrast, "perda_sem_motivo": sem_motivo,
                                              "cliente_ultimo_a_falar": ultimo_cliente, "conversas_lidas": lidos,
                                              "pct_cliente_ultimo": pct(ultimo_cliente, lidos)}
    ef = [o for o in fech if o["step"] == 32318]
    out["B6_venda_com_valor"] = {"vendas": len(ef), "com_valor": sum(1 for o in ef if o["amount"] and float(o["amount"]) > 0)}

    # efeito do follow-up: agendamentos enviados na semana com resposta do cliente em até 7 dias
    tickets_do_contato = defaultdict(set)
    num_de = {cid: v.get("number") for cid, v in ld("contatos.json").items()}
    for c in CARDS:
        tickets_do_contato[c["number"]] |= set(c["ticketIds"])
    env = [a for a in AG if a.get("sentAt") and na(a["sentAt"])]
    resp, med = 0, 0
    for a in env:
        num = num_de.get(str(a["contactId"]))
        tks = tickets_do_contato.get(num)
        if not tks:
            continue
        med += 1
        t0 = ts(a["sentAt"])
        if any(not m.get("fromMe") and t0 < ts(m["at"]) <= t0 + timedelta(days=7) for t in tks for m in M.get(str(t), [])):
            resp += 1
    out["efeito_followup"] = {"mensagens_enviadas": len(env), "com_conversa_lida": med, "cliente_respondeu_7d": resp, "pct": pct(resp, med)}

    # funil entupido em R$: cards ativos parados acima de 1,5× a mediana da própria coluna (tempo desde a última mudança de coluna)
    ativos = [o for o in A if o["step"] in ATIVAS and o["moved"]]
    idade = lambda o: (coleta - ts(o["moved"])).total_seconds() / 86400
    por_col = defaultdict(list)
    for o in ativos:
        por_col[o["step"]].append(o)
    entup = {}
    for step, L in por_col.items():
        if len(L) < MIN_N:
            continue
        med_col = st.median(idade(o) for o in L)
        lim = 1.5 * med_col
        par = [o for o in L if idade(o) > lim]
        tot_rs = sum(float(o["amount"] or 0) for o in L)
        entup[S[step]] = {"cards": len(L), "mediana_dias": round(med_col, 1), "parados": len(par), "pct": pct(len(par), len(L)),
                          "rs_parado": round(sum(float(o["amount"] or 0) for o in par), 2), "rs_total": round(tot_rs, 2)}
    out["funil_entupido"] = entup

    # higiene: tag de tipo nos cards criados na semana; contatos com mais de um card ativo
    novos = [c for c in CARDS if na(c["createdAt"]) and c["step"] in S]
    com_tag = sum(1 for c in novos if any(t in TAG_TIPO for t in (c.get("orderTags") or [])))
    dup = Counter(o["contactId"] for o in ativos)
    out["higiene"] = {"cards_novos": len(novos), "com_tag_tipo": com_tag, "pct_tag": pct(com_tag, len(novos)),
                      "contatos_com_2_ou_mais_ativos": sum(1 for v in dup.values() if v > 1), "contatos_ativos": len(dup)}

    # ---------- C. resultado
    perdas = sum(1 for o in fech if o["step"] == 36613)
    vendas = sum(1 for o in ef if o["status"] == "WON")
    out["C_resultado"] = {"vendas": vendas, "valor": round(sum(float(o["amount"] or 0) for o in ef if o["status"] == "WON"), 2),
                          "perdas": perdas, "conversao_pct": pct(vendas, vendas + perdas)}

    # ---------- D. dono na operação
    num_tk = {str(t): c["number"] for c in CARDS for t in c["ticketIds"]}
    dono_msgs = Counter()
    for t, ms in M.items():
        k = "equipe" if num_tk.get(t) in INTERNOS else "cliente"
        n = sum(1 for m in ms if m.get("fromMe") and m.get("userId") == DONO and na(m["at"]))
        if n:
            dono_msgs[k + "_msgs"] += n
            dono_msgs[k + "_conversas"] += 1
    out["D1_dono_na_operacao"] = {"com_clientes": {"mensagens": dono_msgs["cliente_msgs"], "conversas": dono_msgs["cliente_conversas"]},
                                  "com_equipe_pelo_whatsapp_da_loja": {"mensagens": dono_msgs["equipe_msgs"], "conversas": dono_msgs["equipe_conversas"]},
                                  "cards_novos_no_usuario_dele": sum(1 for c in novos if c["userId"] == DONO),
                                  "encerramentos_no_usuario_dele": sum(1 for o in fech if o["userId"] == DONO)}
    return out


if __name__ == "__main__":
    print(json.dumps(main(*sys.argv[1:4]), ensure_ascii=False, indent=1))
