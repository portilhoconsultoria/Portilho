"""Gera o relatório markdown de TPR/TR a partir da saída de tpr_tr.py.

Uso: python3 -I relatorio_tpr_tr.py <dir> <data_ini> <data_fim> > relatorio.md
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tpr_tr  # noqa: E402

META_TPR = 4  # min, Fernando 19/10
META_TR = 15  # min, proposta (não aprovada)


def fmt(v):
    if v is None:
        return "—"
    if v < 1:
        return f"{v * 60:.0f} s"
    if v < 120:
        return f"{v:.1f} min".replace(".", ",")
    return f"{v / 60:.1f} h".replace(".", ",")


def tabela(linhas, meta):
    out = ["| Vendedor | Respondidos | Mediana | P90 | Sem resposta | Em aberto (mediana) | Após 18h |", "|---|---|---|---|---|---|---|"]
    for v, r in linhas.items():
        med = fmt(r["mediana_min"])
        if r["mediana_min"] is not None and meta is not None:
            med += " ✅" if r["mediana_min"] <= meta else " ❌"
        nome = f"**{v}**" if v == "Equipe" else ("sem dono no card" if v == "user None" else v)
        out.append(f"| {nome} | {r['respondidos']} | {med} | {fmt(r['p90_min'])} | {r['sem_resposta']} | {fmt(r['sem_resposta_mediana_aberto_min'])} | {r['aguardando_abertura']} |")
    return "\n".join(out)


def main(d, ini, fim):
    ev, fora, meta = tpr_tr.main(d, ini, fim)
    res = tpr_tr.resumo(ev)
    periodo = ini if ini == fim else f"{ini} a {fim}"
    L = [
        f"# TPR / TR — Verdes Plantas — {periodo}",
        "",
        f"Coleta: {tpr_tr.ts(meta['coletadoEm']):%d/%m/%Y %H:%M} (Brasília) · {meta['cards']} cards com mensagem no período · "
        f"{meta['tickets']} tickets · {meta['mensagens']} mensagens lidas.",
        "Tempo contado só no expediente (seg–sex 08–18h). Só resposta de vendedor humano para o relógio.",
        "",
        f"## TPR — tempo de primeira resposta (meta: {META_TPR} min)",
        "",
        tabela(res["TPR"], META_TPR),
        "",
        f"## TR — tempo de resposta em conversa andando (meta proposta: {META_TR} min, não aprovada)",
        "",
        tabela(res["TR"], META_TR),
        "",
    ]
    if ini != fim:
        L += ["## Por dia (equipe)", "",
              "| Dia | TPR n | TPR mediana | TPR P90 | TR n | TR mediana | TR P90 |",
              "|---|---|---|---|---|---|---|"]
    from collections import defaultdict
    dias = defaultdict(lambda: defaultdict(list))
    for k, _, mins, dia, _, _ in ev:
        if mins is not None:
            dias[str(dia)][k].append(mins)
    for dia in sorted(dias) if ini != fim else []:
        a, b = dias[dia]["TPR"], dias[dia]["TR"]
        L.append(f"| {dia} | {len(a)} | {fmt(tpr_tr.pct(a, .5))} | {fmt(tpr_tr.pct(a, .9))} | {len(b)} | {fmt(tpr_tr.pct(b, .5))} | {fmt(tpr_tr.pct(b, .9))} |")
    L += [
        "",
        "## Como ler",
        "",
        "- **Respondidos:** blocos de mensagem do cliente que tiveram resposta humana. A mediana e o P90 usam só esses.",
        "- **Sem resposta:** blocos sem resposta humana até a coleta, com prazo já correndo. O tempo em aberto é contado em horas de expediente.",
        "- **Após 18h:** sem resposta, mas o relógio só começa na próxima abertura (08h do dia útil seguinte). Ainda não são atraso.",
        f"- **Atendidos fora do expediente** (cliente escreveu e foi respondido antes da abertura, p.ex. sábado): "
        f"TPR {fora.get('TPR', 0)} · TR {fora.get('TR', 0)}. Ficam fora da mediana; sábado depende de confirmação do Fernando.",
        "- **Atendimento novo (TPR)** = mensagem do cliente sem resposta humana no ticket nas 24 h anteriores. Cliente que volta após mais de 24 h de silêncio abre bloco novo. Regras assumidas, a validar com o Fernando.",
        "- Vendedor = quem respondeu. Nos sem resposta, é o dono do card.",
        "- **Limitação conhecida:** um \"tá bom\"/\"obrigado\" de encerramento do cliente conta como bloco. Sem resposta, entra em \"sem resposta\"; se o vendedor volta a falar dias depois, vira um TR longo e pesa no P90. As medianas são pouco afetadas.",
        "- Mensagens da loja enviadas pelo celular (sem usuário do painel) não param o relógio nesta versão. Com elas contando, a mediana da equipe varia menos de 1 min.",
        "- Base: cards do funil Verdes Plantas (10541) com mensagem no período. Conversas sem card no funil ficam de fora.",
    ]
    print("\n".join(L))


if __name__ == "__main__":
    main(*sys.argv[1:4])
