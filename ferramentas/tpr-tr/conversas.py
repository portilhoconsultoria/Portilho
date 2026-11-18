"""Leitura das conversas dos cards movidos no dia (decisões da reunião de 18/11/2026). Só leitura dos arquivos da coleta.

Uso: conversas.py <pasta_da_coleta> <AAAA-MM-DD>  -> JSON em stdout (conversas.json)

1. ciclo da venda: do início da negociação (card criado) até a Venda ganha, por categoria (tag de tipo);
2. venda ganha: pedido/PDF enviado, Pix, comprovante do cliente — o processo definido em 18/11;
3. onde travou: cards que foram para Incógnita / Venda Perdida no dia, com a etapa em que a conversa parou
   (1ª passagem por palavra-chave + trechos, para revisão humana);
4. rotina do follow-up: cards que entraram em FU1/FU2 no dia — tag, valor, mensagem agendada e nota;
5. conversão por categoria entre os encerrados do dia.
Limite: a coleta traz as mensagens do dia e das 24 h anteriores; conversas mais longas aparecem só no trecho final.
"""
import json
import os
import re
import statistics
import sys
from collections import Counter, defaultdict
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dados_edicao import BRT, S, TAG_TIPO, motivo_cat, nome, ts  # noqa: E402

EFET, PERD, INC, NC, FU1, FU2 = 32318, 36613, 44334, 121919, 36971, 113074
PDF_T = {"application/pdf", "application"}
IMG_T = {"image", "imageMessage", "application/pdf", "application"}
PIX = re.compile(r"\bpix\b|chave|cnpj|copia e cola|qr ?code", re.I)
PEDIDO = re.compile(r"pedido|or[cç]amento", re.I)
COMPROV = re.compile(r"comprovante|paguei|pago|transferi|fiz o pix|segue o pix", re.I)
LIGOU = re.compile(r"liguei|liga[cç][aã]o|ligou|ligar|telefon|por fone", re.I)
LOJA = re.compile(r"vou (a[ií]|passar|buscar)|passo a[ií]|na loja|vou retirar|retiro|pago a[ií]|pagar a[ií]", re.I)
ETAPAS = (
    ("produto em falta", re.compile(r"n[aã]o temos|em falta|sem estoque|n[aã]o trabalhamos|acabou", re.I)),
    ("depois do preço", re.compile(r"r\$|\d+,\d{2}|valor|reais|custa|pre[cç]o|fica (em|por)|sai (a|por)", re.I)),
    ("depois de cidade / entrega / frete", re.compile(r"entreg|frete|cidade|retir|buscar|endere[cç]|cep|envi(o|amos)", re.I)),
    ("depois de quantidade / medida", re.compile(r"metro|m²|m2\b|quantidade|quantas|quantos|unidade", re.I)),
    ("depois de foto / opções", re.compile(r"foto|imagem|op[cç][oõ]es|modelo|segue", re.I)),
)


def humanas(ms):
    """Mensagens de pessoas (sem automação de coluna, fluxo ou sistema)."""
    return [m for m in ms if not m.get("colAuto") and not m.get("flow") and not m.get("deleted")
            and not (m.get("fromMe") and m.get("sys") and not m.get("userId"))]


def txt(m, n=220):
    b = re.sub(r"^\*[^*]{1,40}:\*\s*", "", (m.get("body") or "").replace("\n", " ")).strip()
    return (b or f"[{m.get('type')}]")[:n]


def inicio_conversa(ms, fim, gap_h=72):
    """1ª mensagem da conversa sobre esta venda: depois do último silêncio de 3 dias ou mais antes do fechamento."""
    ms = [m for m in ms if ts(m["at"]) <= fim]
    if not ms:
        return None
    ini = ts(ms[0]["at"])
    for x, y in zip(ms, ms[1:]):
        if ts(y["at"]) - ts(x["at"]) >= timedelta(hours=gap_h):
            ini = ts(y["at"])
    return ini


def categoria(card):
    tags = [t.upper().strip() for t in (card.get("orderTags") or []) + (card.get("contactTags") or [])]
    tipo = [t for t in tags if t in TAG_TIPO]
    return tipo[0] if tipo else "sem tag de tipo"


def med(v):
    return round(statistics.median(v), 1) if v else None


def main(d, dia):
    ld = lambda f: json.load(open(os.path.join(d, f)))
    N, CARDS, M, NT, AG, C = (ld("negocios.json"), ld("cards.json"), ld("mensagens.json"), ld("notas.json"),
                              ld("agendamentos.json"), ld("contatos.json"))
    corte = ts(ld("meta_edicao.json")["coletadoEm"])
    d0 = datetime.fromisoformat(dia).replace(tzinfo=BRT)
    d1 = d0 + timedelta(days=1)
    hoje = lambda s: bool(s) and d0 <= ts(s) < d1
    card = {c["id"]: c for c in CARDS}
    pend = {a["contactId"] for a in AG if not a["sentAt"] and a["sendAt"] and ts(a["sendAt"]) > corte}
    mov = [o for o in N if o["step"] in S and hoje(o["moved"])]

    def conversa(o):
        c = card.get(o["id"]) or {}
        ms = sorted((m for t in c.get("ticketIds") or [] for m in M.get(str(t), [])), key=lambda m: m["at"])
        return c, humanas(ms)

    def notas(o):
        v = sorted(NT.get(str(o["id"])) or [], key=lambda n: n["createdAt"])
        return [{"em": ts(n["createdAt"]).strftime("%d/%m %H:%M"), "autor": nome(n.get("userId")),
                 "texto": (n.get("body") or "").replace("\n", " ").strip()[:240]} for n in v[-3:]]

    def base(o, c):
        cc = C.get(str(o["contactId"])) or {}
        return {"card": o["id"], "vendedor": nome(o["userId"]), "cliente": cc.get("name") or c.get("contact") or "(sem nome)",
                "telefone": cc.get("number") or c.get("number") or "", "categoria": categoria(c), "valor": o["amount"],
                "notas": notas(o), "ligacao_anotada": any(LIGOU.search(n["texto"]) for n in notas(o))}

    out = {"dia": dia, "definicao": __doc__.strip().splitlines()[0]}

    # 1 e 2. vendas ganhas no dia
    vendas = []
    for o in mov:
        if o["step"] != EFET:
            continue
        c, hs = conversa(o)
        fim = ts(o.get("wonAt") or o["moved"])
        ini_conv = inicio_conversa(hs, fim) if fim else None
        ini = ini_conv or ts(o["createdAt"])
        h = round((fim - ini).total_seconds() / 3600, 1) if ini and fim else None
        eu = [m for m in hs if m["fromMe"]]
        cli = [m for m in hs if not m["fromMe"]]
        r = base(o, c)
        r.update({"ciclo_horas": h, "ciclo_dias": round(h / 24, 1) if h is not None else None,
                  "inicio": ini.strftime("%d/%m %H:%M") if ini else None,
                  "inicio_pela_conversa": bool(ini_conv),
                  "card_reaproveitado": bool(h and h > 24 * 60),
                  "pdf_enviado": any(m.get("type") in PDF_T for m in eu),
                  "pedido_citado": any(PEDIDO.search(m.get("body") or "") for m in eu),
                  "pix_enviado": any(PIX.search(m.get("body") or "") for m in eu),
                  "comprovante_cliente": any(m.get("type") in IMG_T or COMPROV.search(m.get("body") or "") for m in cli),
                  "vai_pagar_na_loja": any(LOJA.search(m.get("body") or "") for m in cli),
                  "mensagens_lidas": len(hs)})
        vendas.append(r)
    ok = [v for v in vendas if v["ciclo_horas"] is not None and not v["card_reaproveitado"]]
    por_cat = defaultdict(list)
    for v in ok:
        por_cat[v["categoria"]].append(v["ciclo_horas"])
    out["vendas_ganhas"] = {
        "itens": vendas,
        "ciclo_mediana_horas": med([v["ciclo_horas"] for v in ok]),
        "ciclo_por_categoria_horas": {k: {"vendas": len(x), "mediana_horas": med(x)} for k, x in sorted(por_cat.items())},
        "processo": {"vendas": len(vendas), "pdf_enviado": sum(v["pdf_enviado"] for v in vendas),
                     "pix_enviado": sum(v["pix_enviado"] for v in vendas),
                     "comprovante_cliente": sum(v["comprovante_cliente"] for v in vendas),
                     "vai_pagar_na_loja": sum(v["vai_pagar_na_loja"] for v in vendas)}}

    # série de 30 dias (sem categoria: a base de negócios não traz tags)
    h30 = []
    for o in N:
        if o["step"] == EFET and o.get("wonAt") and d1 - timedelta(days=30) <= ts(o["wonAt"]) < d1 and o.get("createdAt"):
            h = (ts(o["wonAt"]) - ts(o["createdAt"])).total_seconds() / 3600
            if 0 <= h <= 24 * 60:
                h30.append(h)
    faixas = Counter("mesmo dia" if h < 24 else "1 a 3 dias" if h < 72 else "4 a 7 dias" if h < 168 else "mais de 7 dias"
                     for h in h30)
    out["ciclo_30_dias"] = {"vendas": len(h30), "mediana_horas": med(h30), "faixas": dict(faixas),
                            "definicao": "criação do card → venda ganha (aproximação: card reaproveitado conta desde a criação; acima de 60 dias fica de fora)"}

    # 3. onde travou (Incógnita e Venda Perdida do dia)
    trav = []
    for o in mov:
        if o["step"] not in (PERD, INC):
            continue
        c, hs = conversa(o)
        eu = [m for m in hs if m["fromMe"]]
        cli = [m for m in hs if not m["fromMe"]]
        ult_eu, ult_cli = (eu[-1] if eu else None), (cli[-1] if cli else None)
        ultimo = hs[-1] if hs else None
        nts = notas(o)
        if len(cli) <= 1 and not eu and nts:
            etapa = "sem conversa no WhatsApp, só nota (ler a nota)"
        elif len(cli) <= 1 and not eu:
            etapa = "sem interação (ninguém respondeu)"
        elif len(cli) <= 1:
            etapa = "sem interação do cliente depois do 1º contato"
        elif ultimo and not ultimo["fromMe"]:
            etapa = "cliente escreveu por último (ficou sem resposta)"
        else:
            alvo = " ".join(txt(m, 400) for m in eu[-2:])
            etapa = next((n for n, rx in ETAPAS if rx.search(alvo)), "outra (ler a conversa)")
        r = base(o, c)
        r.update({"coluna": S[o["step"]], "motivo": (o.get("lostReason") or "").strip()[:160],
                  "motivo_categoria": motivo_cat(o.get("lostReason")) if o["step"] == PERD else None,
                  "etapa": etapa, "mensagens_lidas": len(hs),
                  "ultima_do_vendedor": txt(ult_eu) if ult_eu else None,
                  "ultima_do_cliente": txt(ult_cli) if ult_cli else None})
        trav.append(r)
    out["onde_travou"] = {"itens": trav, "por_etapa": Counter(t["etapa"] for t in trav).most_common(),
                          "por_vendedor": {v: Counter(t["etapa"] for t in trav if t["vendedor"] == v).most_common()
                                           for v in sorted({t["vendedor"] for t in trav})}}

    # 4. rotina do follow-up (definida em 18/11: tag, valor, mensagem agendada, nota)
    fu = []
    for o in mov:
        if o["step"] not in (FU1, FU2):
            continue
        c, _ = conversa(o)
        r = base(o, c)
        r.update({"coluna": S[o["step"]], "tem_tag": r["categoria"] != "sem tag de tipo",
                  "tem_valor": bool(o["amount"] and float(o["amount"]) > 0),
                  "tem_agenda": o["contactId"] in pend,
                  "tem_nota_hoje": any(hoje(n["createdAt"]) for n in NT.get(str(o["id"])) or [])})
        r["completo"] = r["tem_tag"] and r["tem_valor"] and r["tem_agenda"] and r["tem_nota_hoje"]
        fu.append(r)
    pv = defaultdict(lambda: Counter())
    for r in fu:
        p = pv[r["vendedor"]]
        p["cards"] += 1
        for k in ("tem_tag", "tem_valor", "tem_agenda", "tem_nota_hoje", "completo"):
            p[k] += r[k]
    out["rotina_followup"] = {"itens": fu, "por_vendedor": {k: dict(v) for k, v in pv.items()},
                              "total": dict(sum(pv.values(), Counter()))}

    # 5. conversão por categoria entre os encerrados do dia
    cv = defaultdict(lambda: Counter())
    for o in mov:
        if o["step"] in (EFET, PERD, INC):
            c = card.get(o["id"]) or {}
            k = categoria(c)
            cv[k]["encerrados"] += 1
            cv[k]["vendas"] += o["step"] == EFET
            if o["step"] == EFET and o["amount"]:
                cv[k]["valor"] += float(o["amount"])
    out["conversao_por_categoria"] = {k: {"encerrados": v["encerrados"], "vendas": v["vendas"],
                                          "valor": round(v["valor"], 2),
                                          "conversao": round(v["vendas"] / v["encerrados"], 2)}
                                      for k, v in sorted(cv.items(), key=lambda x: -x[1]["encerrados"])}
    return out


if __name__ == "__main__":
    json.dump(main(sys.argv[1], sys.argv[2]), sys.stdout, ensure_ascii=False, indent=1, default=str)
