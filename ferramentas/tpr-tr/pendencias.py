"""Pendências do comercial (Verdes Plantas): lista acumulada, por vendedor, do que falta fazer nos cards.

Entrada: <dir> com negocios.json, agendamentos.json, notas.json, contatos.json, cards.json, mensagens.json,
meta_edicao.json (rodar_edicao.sh) e tickets_abertos.json (coletar_pendencias.js).
Opcional: pendencias.json do dia anterior — dá "pendente desde" e "feito hoje".

Uso: python3 -I pendencias.py <dir> <dia AAAA-MM-DD> [pendencias_anterior.json] > pendencias.json
     python3 -I pendencias.py --md pendencias.json > Pendencias.md

Regras (reunião de 28/10 e pedido do Fernando de 30/10):
- encerrar_acoes: card em coluna de encerramento sem status (arrastado), movido desde 21/10 (20/10 foi a limpeza).
- encerrar_conversa: card em coluna de encerramento cuja conversa segue aberta (open/pending) e cujo contato
  não tem outro card ativo.
- venda_reaberta: card com status de ganho/encerrado de volta ao Atendimento Inicial ou de Vendedores.
- venda_fora: ganho (WON) fora da Venda Efetivada, movido desde 21/10 (20/10 foi a limpeza).
- followup_sem_agenda: card em Follow-up 1/2 sem mensagem agendada pendente.
- parado_inicial: card no Atendimento Inicial sem movimento há mais de 1 dia útil (avisos da Maria à parte).
- sem_tag: card criado desde 28/10 já em Vendedores ou adiante, sem tag de tipo (só cards com conversa no dia).
"""
import json
import os
import sys
from collections import defaultdict
from datetime import datetime, timedelta, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dados_edicao import S, ENCERRA, ATIVAS, TAG_TIPO, nome, ts, BRT  # noqa: E402

DESDE_ACOES = datetime(2026, 10, 21, tzinfo=BRT)  # 20/10 foi o dia da limpeza, antes do Ações valer
DESDE_TAG = datetime(2026, 10, 28, tzinfo=BRT)
O_QUE = {
    "venda_reaberta": "Venda voltou ao atendimento: responder e devolver para Venda Efetivada (Ações → Venda ganha). Não reencerrar na Incógnita",
    "venda_fora": "Ganho fora da Venda Efetivada: mover para Venda Efetivada",
    "encerrar_acoes": "Card arrastado: encerrar pelo Ações (status, motivo e valor); se for duplicado, arquivar",
    "encerrar_conversa": "Card encerrado com a conversa aberta: finalizar o atendimento em Conversas",
    "parado_inicial": "Parado no Atendimento Inicial há mais de 1 dia útil: atender ou repassar",
    "followup_sem_agenda": "Follow-up sem mensagem agendada: agendar com dia e hora",
    "sem_tag": "Sem tag de tipo: classificar",
}
ORDEM = list(O_QUE)


def dias_uteis(a, b):
    n, d = 0, a.date()
    while d < b.date():
        d += timedelta(days=1)
        n += d.weekday() < 5
    return n


def main(d, dia, anterior=None):
    ld = lambda f: json.load(open(os.path.join(d, f)))
    N, AG, C, CA = ld("negocios.json"), ld("agendamentos.json"), ld("contatos.json"), ld("cards.json")
    TK = ld("tickets_abertos.json")
    corte = ts(ld("meta_edicao.json")["coletadoEm"])
    A = [o for o in N if o["step"] in S]
    ativos_por_contato = defaultdict(int)
    for o in A:
        if o["step"] in ATIVAS:
            ativos_por_contato[o["contactId"]] += 1
    aberto = {t["contactId"] for t in TK if t.get("contactId")}
    agendado = {a["contactId"] for a in AG if not a["sentAt"] and a["sendAt"] and ts(a["sendAt"]) > corte}
    tags = {c["id"]: c.get("orderTags") or [] for c in CA}

    itens = []

    def add(tipo, o, extra=""):
        c = C.get(str(o["contactId"])) or {}
        itens.append({"chave": f"{tipo}:{o['id']}", "tipo": tipo, "card": o["id"], "vendedor": nome(o["userId"]),
                      "telefone": c.get("number") or "", "cliente": c.get("name") or "(sem nome)",
                      "coluna": S[o["step"]], "valor": o["amount"], "obs": extra})

    for o in A:
        mov = ts(o["moved"]) if o["moved"] else None
        if o["step"] in (44341, 69421) and o["status"] not in (None, "OPEN"):
            add("venda_reaberta", o, "ganho" if o["status"] == "WON" else "encerrado")
        elif o["status"] == "WON" and o["step"] in (36613, 121919, 44334) and mov and mov >= DESDE_ACOES:
            add("venda_fora", o)
        if o["step"] in ENCERRA and o["status"] in (None, "OPEN") and mov and mov >= DESDE_ACOES:
            add("encerrar_acoes", o)
        if (o["step"] in ENCERRA and mov and mov >= DESDE_ACOES and o["contactId"] in aberto
                and not ativos_por_contato[o["contactId"]]):
            add("encerrar_conversa", o)
        if o["step"] in (36971, 113074) and o["contactId"] not in agendado:
            add("followup_sem_agenda", o, f"na coluna há {(corte - mov).days} dia(s)" if mov else "")
        if o["step"] == 44341 and o["status"] in (None, "OPEN") and mov and dias_uteis(mov, corte) > 1:
            add("parado_inicial", o, ("aviso da Maria? " if o["userId"] == 28637 else "") + f"{dias_uteis(mov, corte)} dias úteis")
        if (o["step"] not in (44341,) and o["id"] in tags and ts(o["createdAt"]) >= DESDE_TAG
                and not any(t in TAG_TIPO for t in tags[o["id"]])):
            add("sem_tag", o)

    prev = {}
    if anterior and os.path.exists(anterior):
        prev = {i["chave"]: i for i in json.load(open(anterior)).get("itens", [])}
    hoje = {i["chave"] for i in itens}
    for i in itens:
        i["desde"] = prev[i["chave"]]["desde"] if i["chave"] in prev else dia
    feitos = [dict(p, feito_em=dia) for k, p in prev.items() if k not in hoje]
    # avisos da Maria: cards do usuário da Luana (28637) levados hoje para Não Comercial; retorno = cliente
    # escreveu depois disso (só cards com conversa no dia, em cards.json/mensagens.json)
    d0 = datetime.fromisoformat(dia).replace(tzinfo=BRT)
    M = ld("mensagens.json")
    avisos = [o for o in A if o["step"] == 121919 and o["userId"] == 28637 and o["moved"] and d0 <= ts(o["moved"]) < d0 + timedelta(days=1)]
    nc_maria = {o["id"]: o for o in A if o["step"] == 121919 and o["userId"] == 28637 and o["moved"]}
    retornos = []
    for c in CA:
        o = nc_maria.get(c["id"])
        if not o:
            continue
        if any(not m["fromMe"] and ts(m["at"]) > ts(o["moved"]) for t in c.get("ticketIds") or [] for m in M.get(str(t), [])):
            cc = C.get(str(o["contactId"])) or {}
            retornos.append({"telefone": cc.get("number") or "", "cliente": cc.get("name") or "(sem nome)"})
    return {"dia": dia, "coleta": corte.strftime("%d/%m/%Y %H:%M"), "itens": itens, "feitos_hoje": feitos,
            "maria": {"avisos_hoje": len(avisos), "retornos": retornos}}


def brl(v):
    return ("R$ " + f"{float(v):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")) if v else ""


def ddmm(s):
    return f"{s[8:10]}/{s[5:7]}"


def md(p):
    out = [f"# Pendências do comercial", f"### Floricultura Verdes Plantas · situação em {ddmm(p['dia'])}/{p['dia'][:4]} · leitura às {p['coleta'][-5:]}", ""]
    por = defaultdict(list)
    for i in p["itens"]:
        por[i["vendedor"]].append(i)
    feitos = defaultdict(list)
    for i in p["feitos_hoje"]:
        feitos[i["vendedor"]].append(i)
    tot = len(p["itens"])
    out.append(f"Fernando, esta é a lista do que falta fazer nos cards, separada por vendedor, para você repassar. "
               f"**{tot} pendências abertas; {len(p['feitos_hoje'])} resolvidas desde a leitura anterior.** "
               f"Cada item fica na lista até ser feito; quando é feito, aparece uma vez como resolvido e sai.")
    out.append("")
    out.append("| Vendedor | Abertas | Resolvidas hoje | " + " | ".join(t.replace("_", " ") for t in []) + "")
    out[-1] = "| Vendedor | Abertas | Resolvidas desde ontem |"
    out.append("|---|---|---|")
    vend = sorted(set(por) | set(feitos), key=lambda v: (-len(por[v]), v))
    for v in vend:
        out.append(f"| {v} | {len(por[v])} | {len(feitos[v])} |")
    out.append(f"| **Total** | **{tot}** | **{len(p['feitos_hoje'])}** |")
    out.append("")
    curto = {"venda_reaberta": "Venda reaberta", "venda_fora": "Ganho fora", "encerrar_acoes": "Arrastado",
             "encerrar_conversa": "Conversa aberta", "parado_inicial": "Parado no Inicial",
             "followup_sem_agenda": "FU sem agenda", "sem_tag": "Sem tag"}
    out.append("Por tipo de pendência:")
    out.append("")
    out.append("| Tipo | " + " | ".join(vend) + " | Total |")
    out.append("|---|" + "---|" * (len(vend) + 1))
    for tipo in ORDEM:
        n = [sum(1 for i in por[v] if i["tipo"] == tipo) for v in vend]
        if sum(n):
            out.append(f"| {curto[tipo]} | " + " | ".join(str(x) if x else "—" for x in n) + f" | {sum(n)} |")
    out.append("")
    m = p.get("maria") or {}
    if m:
        out.append(f"**Avisos da Maria (usuário da Luana):** {m['avisos_hoje']} cards levados hoje para Não Comercial. "
                   f"Clientes desses avisos que voltaram a escrever: {len(m['retornos'])}" + (" — " + ", ".join(f"{r['cliente']} ({r['telefone']})" for r in m['retornos']) if m['retornos'] else "") + ".")
        out.append("")
    titulos = {"venda_reaberta": "Vendas que voltaram ao atendimento", "venda_fora": "Ganhos fora da Venda Efetivada",
               "encerrar_acoes": "Cards arrastados — encerrar pelo Ações", "encerrar_conversa": "Cards encerrados com a conversa aberta",
               "parado_inicial": "Parados no Atendimento Inicial", "followup_sem_agenda": "Follow-up sem mensagem agendada",
               "sem_tag": "Sem tag de tipo"}
    for v in vend:
        out.append(f"## {v.upper()}")
        out.append("")
        for tipo in ORDEM:
            its = [i for i in por[v] if i["tipo"] == tipo]
            if not its:
                continue
            out.append(f"### {titulos[tipo]} — {len(its)}")
            out.append("")
            out.append(f"O que fazer: {O_QUE[tipo]}.")
            out.append("")
            out.append("| Telefone | Cliente | Coluna | Valor | Desde | Obs. |")
            out.append("|---|---|---|---|---|---|")
            for i in sorted(its, key=lambda i: i["desde"]):
                out.append(f"| {i['telefone']} | {i['cliente'][:28]} | {i['coluna']} | {brl(i['valor'])} | {ddmm(i['desde'])} | {i['obs']} |")
            out.append("")
        if feitos[v]:
            out.append(f"### Resolvidas desde a leitura anterior — {len(feitos[v])}")
            out.append("")
            out.append("| Telefone | Cliente | O que era |")
            out.append("|---|---|---|")
            for i in feitos[v]:
                out.append(f"| {i['telefone']} | {i['cliente'][:28]} | {titulos[i['tipo']]} |")
            out.append("")
    out.append("## COMO ESTA LISTA É FEITA")
    out.append("")
    out.append("Leitura direta da base do CRM, junto com o relatório diário. As regras de cada grupo são as combinadas na reunião de 28/10. "
               "\"Desde\" é o primeiro dia em que o item apareceu na lista. Cards encerrados contam a partir de 21/10 (o dia 20/10 foi a limpeza da coluna, antes do botão Ações valer); o acumulado anterior está no relatório diário (seção 2.4).")
    return "\n".join(out)


if __name__ == "__main__":
    if sys.argv[1] == "--md":
        print(md(json.load(open(sys.argv[2]))))
    else:
        print(json.dumps(main(*sys.argv[1:4]), ensure_ascii=False, indent=1, default=str))
