"""TPR/TR da Verdes Plantas a partir de cards.json + mensagens.json (coletar.js).

Definições: wiki/entities/kpis-atendimento-comercial-verdes-plantas.md
- Expediente seg–sex 08:00–18:00 (America/Sao_Paulo). Sábado e domingo fora.
- Fora do expediente, o relógio começa na abertura do dia útil seguinte.
- Só mensagem de vendedor humano para o relógio (automação não conta).
- Reporte em minutos, mediana e P90.

Classificação de mensagem (medida em 21/10/2026 na rota /messages/{ticketId}):
- cliente   = fromMe false
- vendedor  = fromMe true e userId preenchido (o texto traz o prefixo *Nome:*)
- automação = fromMe true sem userId (boas-vindas, avaliação, automação de coluna)
sendBySystem vem true também nas mensagens humanas e por isso não é usado.

Regras assumidas (pendentes de validação com o Fernando):
- Bloco = mensagens consecutivas do cliente; o relógio começa na primeira do bloco.
- Cliente que volta após mais de 24 h de silêncio abre bloco novo; o anterior fecha como abandonado.
- Atendimento novo (TPR) = bloco sem mensagem de vendedor humano no ticket nas 24 h anteriores.
  Os demais blocos são TR.
- Bloco sem resposta humana até o momento da coleta = "sem resposta" (fica fora da mediana
  e é contado à parte, com o tempo em aberto).
- Bloco aberto e respondido fora do expediente (p.ex. sábado) = fora da mediana, contado à parte.

Uso: python3 -I tpr_tr.py <dir> <data_ini AAAA-MM-DD> <data_fim AAAA-MM-DD>
"""
import json
import os
import sys
from collections import defaultdict
from datetime import datetime, timedelta, timezone

BRT = timezone(timedelta(hours=-3))
ABRE, FECHA = 8, 18
USUARIOS = {21035: "Carine", 15948: "Douglas", 12198: "Edimar", 12152: "Fernando", 28637: "Luana", 12197: "Jaqueline"}


def ts(s):
    return datetime.fromisoformat(s.replace("Z", "+00:00")).astimezone(BRT)


def util(d):
    return d.weekday() < 5


def segundos_expediente(a, b):
    """Segundos de expediente entre a e b."""
    if b <= a:
        return 0.0
    tot, dia = 0.0, a.replace(hour=0, minute=0, second=0, microsecond=0)
    while dia <= b:
        if util(dia):
            ini = max(a, dia.replace(hour=ABRE))
            fim = min(b, dia.replace(hour=FECHA))
            if fim > ini:
                tot += (fim - ini).total_seconds()
        dia += timedelta(days=1)
    return tot


MODO = os.environ.get("MODO", "estrito")  # estrito | amplo
TEMPLATES = ("💚 **Obrigado por escolher", "💚 Bem-vindo", "🌿 Enquanto aguarda", "CLIQUE E NOS AVALIE",
             "Vamos continuar o atendimento?", "Olá! Tudo bem? 😊🌿\n\nAqui é a Ma", "🌱 Oii, tudo bem? Aqui é a Mari",
             "Oi, tudo bem? 😊🌿\n\nAqui é a Mar")


def celular(m):
    """Mensagem da loja sem usuário do painel e sem automação: provável resposta pelo celular."""
    b = m.get("body") or ""
    if m.get("colAuto") or m.get("flow") or b.startswith(TEMPLATES):
        return False
    if b == "" or b.isupper() or b[:1] in "🌳🌸🌿🌱☀️🎄":
        return False  # imagem solta ou campanha: conservador, não conta como resposta
    return True


def quem(m):
    if not m["fromMe"]:
        return "cliente"
    if m["userId"]:
        return "vendedor"
    return "vendedor" if MODO == "amplo" and celular(m) else "auto"


def pct(v, p):
    if not v:
        return None
    v = sorted(v)
    k = (len(v) - 1) * p
    f = int(k)
    return v[f] + (v[min(f + 1, len(v) - 1)] - v[f]) * (k - f)


def main(d, ini, fim):
    cards = json.load(open(f"{d}/cards.json"))
    msgs = json.load(open(f"{d}/mensagens.json"))
    meta = json.load(open(f"{d}/meta.json"))
    corte = ts(meta["coletadoEm"])
    j0 = datetime.fromisoformat(ini).replace(tzinfo=BRT)
    j1 = datetime.fromisoformat(fim).replace(tzinfo=BRT) + timedelta(days=1)
    dono = {}
    for c in cards:
        for t in c["ticketIds"] or []:
            dono[str(t)] = c["userId"]

    eventos = []  # (kpi, vendedor, minutos | None, dia, ticket, aberto_min)
    fora = defaultdict(int)
    for t, ms in msgs.items():
        ms = sorted(({**m, "t": ts(m["at"])} for m in ms if not m.get("deleted")), key=lambda m: m["t"])
        ultimo_humano = None
        i = 0
        while i < len(ms):
            m = ms[i]
            if quem(m) == "vendedor":
                ultimo_humano = m["t"]
            if quem(m) != "cliente":
                i += 1
                continue
            inicio = m["t"]
            novo = ultimo_humano is None or (inicio - ultimo_humano) > timedelta(hours=24)
            # avança até a próxima mensagem de vendedor humano; cliente que volta após
            # mais de 24 h de silêncio abre bloco novo e o anterior fecha como abandonado
            j = i + 1
            quebra = False
            while j < len(ms) and quem(ms[j]) != "vendedor":
                if quem(ms[j]) == "cliente" and ms[j]["t"] - ms[j - 1]["t"] > timedelta(hours=24):
                    quebra = True
                    break
                j += 1
            resp = ms[j] if j < len(ms) and not quebra else None
            limite = ms[j]["t"] if quebra else corte
            if j0 <= inicio < j1:
                kpi = "TPR" if novo else "TR"
                if resp:
                    seg = segundos_expediente(inicio, resp["t"])
                    if seg == 0 and not (util(inicio) and ABRE <= inicio.hour < FECHA):
                        fora[kpi] += 1  # aberto e respondido fora do expediente: fora da mediana
                    else:
                        eventos.append((kpi, USUARIOS.get(resp["userId"], f"user {resp['userId']}") if resp["userId"] else "celular (sem usuário)", seg / 60, inicio.date(), t, None))
                else:
                    aberto = segundos_expediente(inicio, limite) / 60
                    v = dono.get(t)
                    eventos.append((kpi, USUARIOS.get(v, f"user {v}"), None, inicio.date(), t, aberto))
            if quebra:
                i = j  # o cliente que voltou abre o próximo bloco
            elif j < len(ms):
                ultimo_humano = ms[j]["t"]
                i = j + 1
            else:
                i = len(ms)
    return eventos, fora, meta


def resumo(eventos):
    out = {}
    for kpi in ("TPR", "TR"):
        por = defaultdict(list)
        sem = defaultdict(list)
        for k, v, mins, _, _, ab in eventos:
            if k != kpi:
                continue
            for chave in (v, "Equipe"):
                (por if mins is not None else sem)[chave].append(mins if mins is not None else ab)
        linhas = {}
        for chave in sorted(set(por) | set(sem), key=lambda x: (x == "Equipe", x)):
            r = por.get(chave, [])
            s = sem.get(chave, [])
            linhas[chave] = {
                "respondidos": len(r),
                "mediana_min": pct(r, 0.5),
                "p90_min": pct(r, 0.9),
                "sem_resposta": len(s),
                "sem_resposta_mediana_aberto_min": pct(s, 0.5),
            }
        out[kpi] = linhas
    return out


if __name__ == "__main__":
    ev, fora, meta = main(*sys.argv[1:4])
    res = resumo(ev)
    dias = defaultdict(lambda: defaultdict(list))
    for k, v, mins, dia, _, _ in ev:
        if mins is not None:
            dias[str(dia)][k].append(mins)
    res["por_dia_equipe"] = {d: {k: {"n": len(x), "mediana": pct(x, 0.5), "p90": pct(x, 0.9)} for k, x in kv.items()} for d, kv in sorted(dias.items())}
    res["respondidos_fora_do_expediente_tempo_zero"] = dict(fora)
    res["meta_coleta"] = meta
    print(json.dumps(res, ensure_ascii=False, indent=1, default=str))
