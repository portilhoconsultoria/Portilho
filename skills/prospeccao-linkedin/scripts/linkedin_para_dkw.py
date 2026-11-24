#!/usr/bin/env python3
"""Leva leads aprovados do LinkedIn para a etapa "Claude" do pipeline Prospecção no DKW.

Uso:
    python linkedin_para_dkw.py lote.json                         # modo seco (padrão): só relata
    python linkedin_para_dkw.py lote.json --executar --limite 1   # cria 1 card para conferir na tela
    python linkedin_para_dkw.py lote.json --executar              # cria o resto

Variáveis de ambiente:
    DKW_API_KEY   chave da API oficial (obrigatória para consultar/gravar; nunca versionar)
    DKW_API_BASE  padrão https://api-gestao.portilhoconsultoria.com.br/api
    DKW_PIPELINE  padrão 14833 (Prospecção)
    DKW_ETAPA     padrão "Claude" (a API oficial referencia etapa pelo NOME)
    DKW_TAG       padrão "origem_linkedin"
    NOTA_MINIMA   padrão 7

Rotas usadas (API oficial do DKW): GET /contact/{tel}, POST /commercial-order,
POST /contact/{tel}/tags, POST /contact/{tel}/notes.
"""
import argparse
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request

BASE = os.environ.get("DKW_API_BASE", "https://api-gestao.portilhoconsultoria.com.br/api").rstrip("/")
PIPELINE = os.environ.get("DKW_PIPELINE", "14833")
ETAPA = os.environ.get("DKW_ETAPA", "Claude")
TAG = os.environ.get("DKW_TAG", "origem_linkedin")
NOTA_MINIMA = float(os.environ.get("NOTA_MINIMA", "7"))
# Campo de texto da nota. Conferir contra o uso em produção (grep "notes" em D:\portilho-agente).
NOTA_CAMPO = os.environ.get("DKW_NOTA_CAMPO", "body")


def normalizar(tel):
    """Devolve 55DDD9NNNNNNNN (celular BR) ou None. Fixo e estrangeiro voltam None."""
    d = re.sub(r"\D", "", str(tel or ""))
    if d.startswith("00"):
        d = d[2:]
    if len(d) in (10, 11):
        d = "55" + d
    if not d.startswith("55"):
        return None
    if len(d) == 12:  # 55 + DDD + 8 dígitos: só vale se for celular antigo (começa em 6-9)
        if d[4] in "6789":
            d = d[:4] + "9" + d[4:]
        else:
            return None  # fixo
    if len(d) != 13 or d[4] != "9":
        return None
    return d


def chamar(metodo, caminho, corpo=None, chave=None):
    dados = json.dumps(corpo).encode() if corpo is not None else None
    ultimo = "tentativas esgotadas"
    for tentativa in range(4):
        req = urllib.request.Request(BASE + caminho, data=dados, method=metodo, headers={
            "api-key": chave, "Content-Type": "application/json", "Accept": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                txt = r.read().decode()
                return r.status, (json.loads(txt) if txt.strip() else None)
        except urllib.error.HTTPError as e:
            txt = e.read().decode(errors="ignore")
            if e.code == 429 or e.code >= 500:
                ultimo = f"HTTP {e.code}"
                time.sleep(2 * (tentativa + 1))
                continue
            return e.code, txt[:300]
        except (urllib.error.URLError, TimeoutError) as e:
            time.sleep(2 * (tentativa + 1))
            ultimo = str(e)
    return "falhou", ultimo


def ja_existe(tel, chave):
    st, corpo = chamar("GET", f"/contact/{tel}", chave=chave)
    if st == 200 and corpo:
        return True
    if st == 404:
        return False
    raise RuntimeError(f"consulta do contato {tel} devolveu {st}: {corpo}")


def texto_nota(lead):
    partes = [
        "Origem: LinkedIn" + (f" ({lead['missao']})" if lead.get("missao") else ""),
        f"{lead.get('nome', '')} — {lead.get('cargo', '')} @ {lead.get('empresa', '')}",
        f"Perfil: {lead.get('linkedin', '')}",
        f"Nota {lead.get('nota')}: {lead.get('motivo', '')}",
        f"Gancho: {lead.get('gancho', '')}",
        f"Telefone achado em: {lead.get('fonte_telefone', '?')}",
    ]
    return "\n".join(p for p in partes if p.strip())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("lote")
    ap.add_argument("--executar", action="store_true", help="grava no DKW (sem isso, só relata)")
    ap.add_argument("--limite", type=int, default=0, help="máximo de cards criados nesta execução")
    a = ap.parse_args()

    with open(a.lote, encoding="utf-8") as f:
        lote = json.load(f)

    chave = os.environ.get("DKW_API_KEY")
    if not chave:
        print("⚠️ DKW_API_KEY ausente: relato sem consultar duplicados no DKW.")
        if a.executar:
            sys.exit("Sem chave não há --executar.")

    vistos, aptos, barrados = set(), [], []
    for lead in lote:
        nome = lead.get("nome", "?")
        tel = normalizar(lead.get("telefone"))
        try:
            nota = float(lead.get("nota", 0))
        except (TypeError, ValueError):
            nota = 0
        if not tel:
            barrados.append((nome, "sem celular válido (fixo, estrangeiro ou vazio)"))
        elif nota < NOTA_MINIMA:
            barrados.append((nome, f"nota {nota:g} < {NOTA_MINIMA:g}"))
        elif tel in vistos:
            barrados.append((nome, "duplicado no lote"))
        elif chave and ja_existe(tel, chave):
            barrados.append((nome, f"já é contato no DKW ({tel}) — não reinicia a régua"))
        else:
            vistos.add(tel)
            aptos.append((lead, tel))

    print(f"\nLote: {len(lote)} · aptos: {len(aptos)} · barrados: {len(barrados)}")
    for nome, motivo in barrados:
        print(f"  ✗ {nome}: {motivo}")
    if a.limite:
        aptos = aptos[: a.limite]
    for lead, tel in aptos:
        print(f"  → {lead.get('nome')} · {lead.get('empresa')} · {tel}")

    if not a.executar:
        print("\nModo seco: nada gravado. Rode com --executar --limite 1 para o primeiro card.")
        return

    falhas = 0
    for lead, tel in aptos:
        st, corpo = chamar("POST", "/commercial-order",
                           {"contact": tel, "pipeline": PIPELINE, "commercialStep": ETAPA}, chave)
        if st not in (200, 201):
            falhas += 1
            print(f"  🆘 {lead.get('nome')}: card não criado ({st}: {corpo})")
            continue
        st_t, c_t = chamar("POST", f"/contact/{tel}/tags", {"name": TAG}, chave)
        st_n, c_n = chamar("POST", f"/contact/{tel}/notes", {NOTA_CAMPO: texto_nota(lead)}, chave)
        avisos = []
        if st_t not in (200, 201):
            avisos.append(f"tag {st_t}: {c_t}")
        if st_n not in (200, 201):
            avisos.append(f"nota {st_n}: {c_n}")
        print(f"  ✓ {lead.get('nome')} → {ETAPA}" + (f"  ⚠️ {' · '.join(avisos)}" if avisos else ""))
        time.sleep(1.2)  # a API corta em 60 req/60 s

    print(f"\nCriados: {len(aptos) - falhas} · falhas: {falhas}")
    print("Confira na tela do DKW: card em Claude, nome do contato, tag e nota.")


if __name__ == "__main__":
    main()
