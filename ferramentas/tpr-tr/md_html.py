"""Relatório markdown -> HTML de e-mail (mesmo conteúdo do PDF). Uso: python3 -I md_html.py <md>"""
import html, re, sys
sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
from gerar_doc import preparar

AZUL = "#1C6086"
def inl(t):
    t = html.escape(t)
    return re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)

md = preparar(open(sys.argv[1], encoding="utf-8").read()).splitlines()
out = ['<div style="font-family:Calibri,Arial,sans-serif;font-size:14px;color:#1D2A2E;max-width:720px">',
       f'<div style="background:{AZUL};color:#fff;padding:12px 16px;font-size:18px"><b>PORTILHO</b> <span style="font-size:13px">Inteligência Comercial</span></div>']
i, lista = 0, False
while i < len(md):
    l = md[i].rstrip()
    if lista and not l.startswith("- "):
        out.append("</ul>"); lista = False
    if l.startswith("|") and i + 1 < len(md) and re.match(r"^\s*\|[\s:|-]+\|\s*$", md[i + 1]):
        rows = []
        while i < len(md) and md[i].startswith("|"):
            rows.append([c.strip() for c in md[i].strip().strip("|").split("|")]); i += 1
        t = ['<table style="border-collapse:collapse;font-size:13px;margin:6px 0 14px">']
        t.append("<tr>" + "".join(f'<th style="background:{AZUL};color:#fff;padding:5px 8px;text-align:left">{inl(c)}</th>' for c in rows[0]) + "</tr>")
        for k, r in enumerate(rows[2:]):
            bg = "#F4F6F6" if k % 2 else "#fff"
            t.append(f'<tr style="background:{bg}">' + "".join(f'<td style="padding:5px 8px;border-bottom:1px solid #D9DEDF">{inl(c)}</td>' for c in r) + "</tr>")
        out.append("".join(t) + "</table>"); continue
    if l.startswith("# "):
        out.append(f'<h2 style="color:{AZUL};letter-spacing:2px;margin:18px 0 4px">{inl(l[2:].upper())}</h2>')
    elif l.startswith("### "):
        out.append(f'<p style="color:#5F6F74;font-style:italic;margin:0 0 10px">{inl(l[4:])}</p>')
    elif l.startswith("## "):
        out.append(f'<h3 style="color:{AZUL};border-bottom:1px solid {AZUL};padding-bottom:3px;margin:16px 0 6px">{inl(l[3:])}</h3>')
    elif l.startswith("> "):
        out.append(f'<p style="margin:6px 0;padding-left:10px;border-left:2px solid #5E93B0;color:#5F6F74;font-style:italic">{inl(l[2:])}</p>')
    elif l.startswith("- "):
        if not lista: out.append("<ul>"); lista = True
        out.append(f"<li>{inl(l[2:])}</li>")
    elif l.strip():
        out.append(f"<p style=\"margin:4px 0\">{inl(l)}</p>")
    i += 1
if lista: out.append("</ul>")
out.append("</div>")
print("".join(out))
