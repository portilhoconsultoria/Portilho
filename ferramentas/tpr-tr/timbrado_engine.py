# -*- coding: utf-8 -*-
"""
Motor de documentos no padrao timbrado.
Base: D:\\base_conhecimento\\o-conselho\\identidade\\timbrado.md
      + gerar_documento_timbrado.py (script de referencia)

Duas marcas:
  CONSELHO  -> cabecalho.jpg / rodape.jpg  (confidencial, so conselheiros)
  PORTILHO  -> faixa azul #1C6086 + logo branco (documentos de cliente)

Tipografia identica nas duas: Carlito/Calibri (metricas equivalentes).
"""
import os, re, html

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph,
                                Spacer, ListFlowable, ListItem, HRFlowable, Table,
                                TableStyle, KeepTogether, PageBreak)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

BASE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(BASE, "assets")

# ---------------------------------------------------------------- fontes
WF = "/usr/share/fonts/truetype/crosextra"
pdfmetrics.registerFont(TTFont("Carlito",   os.path.join(WF, "Carlito-Regular.ttf")))
pdfmetrics.registerFont(TTFont("Carlito-B", os.path.join(WF, "Carlito-Bold.ttf")))
pdfmetrics.registerFont(TTFont("Carlito-I", os.path.join(WF, "Carlito-Italic.ttf")))
pdfmetrics.registerFont(TTFont("Carlito-BI", os.path.join(WF, "Carlito-BoldItalic.ttf")))
pdfmetrics.registerFontFamily("Carlito", normal="Carlito", bold="Carlito-B",
                              italic="Carlito-I", boldItalic="Carlito-BI")

# ---------------------------------------------------------------- cores
PET    = colors.HexColor("#12343B")   # petroleo  (Conselho)
COBRE  = colors.HexColor("#C1663F")   # cobre     (Conselho)
AZUL   = colors.HexColor("#1C6086")   # azul      (Portilho)
AZUL_C = colors.HexColor("#5E93B0")   # azul claro
CINZA  = colors.HexColor("#5F6F74")
TXT    = colors.HexColor("#1D2A2E")
LINHA  = colors.HexColor("#D9DEDF")
ZEBRA  = colors.HexColor("#F4F6F6")

MARCAS = {
    "conselho": dict(primaria=PET,  acento=COBRE,  rodape_txt="O  C o n s e l h o"),
    "portilho": dict(primaria=AZUL, acento=AZUL_C, rodape_txt=u"P o r t i l h o   I n t e l i g ê n c i a   C o m e r c i a l"),
}

# ---------------------------------------------------------------- estilos
def montar_estilos(m):
    P, A = m["primaria"], m["acento"]
    s = {}
    s["titulo"] = ParagraphStyle("titulo", fontName="Carlito-B", fontSize=14, leading=19,
                                 textColor=P, spaceAfter=2, alignment=TA_LEFT)
    s["subtitulo"] = ParagraphStyle("subtitulo", fontName="Carlito-I", fontSize=10, leading=13,
                                    textColor=CINZA, spaceAfter=10)
    s["h2"] = ParagraphStyle("h2", fontName="Carlito-B", fontSize=11.5, leading=15,
                             textColor=P, spaceBefore=9, spaceAfter=1)
    s["h3"] = ParagraphStyle("h3", fontName="Carlito-B", fontSize=10.5, leading=14,
                             textColor=TXT, spaceBefore=7, spaceAfter=2)
    s["corpo"] = ParagraphStyle("corpo", fontName="Carlito", fontSize=10.5, leading=15.5,
                                textColor=TXT, alignment=TA_JUSTIFY, spaceAfter=6,
                                allowWidows=0, allowOrphans=0)
    s["bullet"] = ParagraphStyle("bullet", parent=s["corpo"], spaceAfter=2, alignment=TA_LEFT,
                                 allowWidows=0, allowOrphans=0)
    s["citacao"] = ParagraphStyle("citacao", fontName="Carlito-I", fontSize=10, leading=14,
                                  textColor=CINZA, leftIndent=10, borderPadding=0,
                                  spaceBefore=3, spaceAfter=7)
    s["th"] = ParagraphStyle("th", fontName="Carlito-B", fontSize=9, leading=11.5,
                             textColor=colors.white, alignment=TA_LEFT)
    s["td"] = ParagraphStyle("td", fontName="Carlito", fontSize=9, leading=11.5,
                             textColor=TXT, alignment=TA_LEFT)
    return s

def rule(cor=PET, w=0.8, sb=1, sa=7):
    return HRFlowable(width="100%", thickness=w, color=cor, spaceBefore=sb,
                      spaceAfter=sa, lineCap="butt")

def LS(t):
    return "&nbsp;".join(list(t))

# ---------------------------------------------------------------- markdown inline
EMOJI = {"\U0001F44D": "(joinha)", "\U0001F91D": "(aperto de mao)",
         "\U0001F600": "", "\u2705": "", "\u2b50": ""}

def limpa(t):
    for k, v in EMOJI.items():
        t = t.replace(k, v)
    # remove qualquer outro caractere fora do alcance da fonte
    t = "".join(ch for ch in t if ord(ch) < 0x2500)
    return t

def inline(t):
    t = limpa(t)
    t = html.escape(t, quote=False)
    t = re.sub(r"`([^`]+)`", r'<font face="Courier" size="9">\1</font>', t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)
    t = re.sub(r"(?<!\*)\*([^*]+?)\*(?!\*)", r"<i>\1</i>", t)
    return t

# ---------------------------------------------------------------- tabela
def montar_tabela(linhas, s, m, largura=170*mm):
    cab = [c.strip() for c in linhas[0].strip().strip("|").split("|")]
    corpo = []
    for ln in linhas[2:]:
        corpo.append([c.strip() for c in ln.strip().strip("|").split("|")])
    ncols = len(cab)
    corpo = [r + [""]*(ncols-len(r)) if len(r) < ncols else r[:ncols] for r in corpo]

    pesos = []
    for i in range(ncols):
        maior = max([len(re.sub(r"[*`]", "", cab[i]))] +
                    [len(re.sub(r"[*`]", "", r[i])) for r in corpo] or [1])
        pesos.append(max(maior, 3) ** 0.75)
    total = sum(pesos)
    widths = [largura * p / total for p in pesos]

    dados = [[Paragraph(inline(c), s["th"]) for c in cab]]
    for r in corpo:
        dados.append([Paragraph(inline(c), s["td"]) for c in r])

    t = Table(dados, colWidths=widths, repeatRows=1, hAlign="LEFT")
    est = [("BACKGROUND", (0, 0), (-1, 0), m["primaria"]),
           ("VALIGN", (0, 0), (-1, -1), "TOP"),
           ("TOPPADDING", (0, 0), (-1, -1), 4),
           ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
           ("LEFTPADDING", (0, 0), (-1, -1), 5),
           ("RIGHTPADDING", (0, 0), (-1, -1), 5),
           ("LINEBELOW", (0, 0), (-1, -1), 0.4, LINHA),
           ("LINEBELOW", (0, 0), (-1, 0), 0.8, m["primaria"])]
    for i in range(1, len(dados)):
        if i % 2 == 0:
            est.append(("BACKGROUND", (0, i), (-1, i), ZEBRA))
    t.setStyle(TableStyle(est))
    return t

# ---------------------------------------------------------------- md -> flowables
def md_para_flowables(md, s, m, titulo_feito=False):
    out = []
    linhas = md.split("\n")
    i = 0
    bullets, numeros = [], []
    pos_titulo_doc = [False]   # so o que vem logo depois do titulo do documento vira subtitulo

    def fecha_listas():
        if bullets:
            out.append(ListFlowable(
                [ListItem(Paragraph(b, s["bullet"]), leftIndent=13, value=u"\u2022") for b in bullets],
                bulletType="bullet", bulletColor=m["acento"], bulletFontSize=9, bulletFontName="Carlito",
                leftIndent=13, bulletOffsetY=-1.5, spaceAfter=6))
            bullets.clear()
        if numeros:
            out.append(ListFlowable(
                [ListItem(Paragraph(n, s["bullet"]), leftIndent=15) for n in numeros],
                bulletType="1", bulletColor=m["primaria"], bulletFontName="Carlito-B",
                bulletFontSize=9.5, leftIndent=15, spaceAfter=6))
            numeros.clear()

    while i < len(linhas):
        ln = linhas[i].rstrip()
        bruta = ln.strip()

        if not bruta:
            fecha_listas(); i += 1; continue

        if re.match(r"^(---+|===+)$", bruta):
            fecha_listas(); i += 1; continue

        if bruta.startswith("|") and i + 1 < len(linhas) and re.match(r"^\s*\|[\s:|-]+\|\s*$", linhas[i+1]):
            fecha_listas(); pos_titulo_doc[0] = False
            bloco = []
            while i < len(linhas) and linhas[i].strip().startswith("|"):
                bloco.append(linhas[i]); i += 1
            out.append(Spacer(1, 3))
            out.append(montar_tabela(bloco, s, m))
            out.append(Spacer(1, 8))
            continue

        if bruta.startswith("#"):
            fecha_listas()
            nivel = len(bruta) - len(bruta.lstrip("#"))
            texto = bruta.lstrip("#").strip()
            if nivel == 1 and not titulo_feito:
                out.append(Paragraph(LS(limpa(texto).upper()), s["titulo"]))
                out.append(rule(m["acento"], 1.1, 1, 9))
                titulo_feito = True
            elif nivel == 1:
                out.append(Spacer(1, 6))
                out.append(Paragraph(LS(limpa(texto).upper()), s["titulo"]))
                out.append(rule(m["acento"], 1.1, 1, 9))
            elif nivel == 2:
                p = Paragraph(inline(texto), s["h2"])
                p._cabeca = 2
                out.append(p)
                out.append(rule(m["primaria"], 0.8, 1, 7))
            else:
                if pos_titulo_doc[0]:
                    out.append(Paragraph(inline(texto), s["subtitulo"]))
                else:
                    p = Paragraph(inline(texto), s["h3"])
                    p._cabeca = 3
                    out.append(p)
            pos_titulo_doc[0] = (nivel == 1)
            i += 1; continue

        if bruta.startswith(">"):
            fecha_listas(); pos_titulo_doc[0] = False
            q = [bruta.lstrip(">").strip()]
            i += 1
            while i < len(linhas) and linhas[i].strip().startswith(">"):
                q.append(linhas[i].strip().lstrip(">").strip()); i += 1
            texto = " ".join(x for x in q if x)
            est = ParagraphStyle("q", parent=s["citacao"],
                                 borderColor=m["acento"], borderWidth=0,
                                 leftIndent=12)
            tb = Table([[Paragraph(inline(texto), est)]], colWidths=[170*mm], hAlign="LEFT")
            tb.setStyle(TableStyle([("LINEBEFORE", (0, 0), (0, -1), 2, m["acento"]),
                                    ("LEFTPADDING", (0, 0), (-1, -1), 8),
                                    ("TOPPADDING", (0, 0), (-1, -1), 3),
                                    ("BOTTOMPADDING", (0, 0), (-1, -1), 3)]))
            out.append(tb); out.append(Spacer(1, 7))
            continue

        mnum = re.match(r"^(\d+)\.\s+(.*)$", bruta)
        if mnum:
            if bullets: fecha_listas()
            numeros.append(inline(mnum.group(2))); i += 1; continue

        if re.match(r"^[-*]\s+", bruta):
            if numeros: fecha_listas()
            bullets.append(inline(re.sub(r"^[-*]\s+", "", bruta))); i += 1; continue

        fecha_listas(); pos_titulo_doc[0] = False
        out.append(Paragraph(inline(bruta), s["corpo"]))
        i += 1

    fecha_listas()
    return agrupar_cabecas(out)

# ------------------------------------------------- orfas de titulo (viuvez)
# Regra Portilho: um titulo nunca fica sozinho no pe da pagina.
# Ele so permanece se levar junto pelo menos ~3 linhas de corpo (MIN_APOS_CABECA).
# Com 1 ou 2 linhas, titulo e conteudo descem inteiros para a pagina seguinte.
MIN_APOS_CABECA = {2: 95.0,   # titulo de secao: ~6 linhas. Secao nao comeca no pe da pagina
                   3: 47.0}   # subtitulo interno: ~3 linhas
MAX_FLOW_ENGOLIDO = 5         # nunca arrastar mais do que isso
ALT_MAX_TABELA = 190          # pt - tabela maior que isso nao e arrastada inteira

def agrupar_cabecas(flows, largura=170*mm):
    out, i = [], 0
    while i < len(flows):
        f = flows[i]
        nivel = getattr(f, "_cabeca", 0)
        if not nivel:
            out.append(f); i += 1; continue

        minimo = MIN_APOS_CABECA.get(nivel, 47.0)
        grupo, alt, usados = [f], 0.0, 0
        i += 1
        while i < len(flows) and usados < MAX_FLOW_ENGOLIDO and alt < minimo:
            prox = flows[i]
            n_prox = getattr(prox, "_cabeca", 0)
            # subtitulo interno logo abaixo de um titulo de secao viaja junto;
            # outro titulo de mesmo nivel (ou acima) encerra o grupo
            if n_prox and n_prox <= nivel:
                break
            if isinstance(prox, HRFlowable):      # regua do titulo nao conta como conteudo
                grupo.append(prox); i += 1; continue
            try:
                _, h = prox.wrap(largura, 10000)
            except Exception:
                h = 20.0
            if isinstance(prox, Table) and h > ALT_MAX_TABELA:
                break                              # tabela longa fica livre para quebrar
            grupo.append(prox); alt += h; i += 1; usados += 1
        out.append(KeepTogether(grupo))
    return out

# ---------------------------------------------------------------- pagina
def fazer_decorador(marca, m, s):
    def decorate(canvas, doc):
        W, H = A4
        canvas.saveState()
        if marca == "conselho":
            canvas.drawImage(os.path.join(ASSETS, "cabecalho.jpg"), 0, H - 26*mm,
                             width=W, height=26*mm, preserveAspectRatio=False, mask=None)
            canvas.drawImage(os.path.join(ASSETS, "rodape.jpg"), 0, 0,
                             width=W, height=10*mm, preserveAspectRatio=False, mask=None)
        else:
            canvas.setFillColor(AZUL)
            canvas.rect(0, H - 26*mm, W, 26*mm, stroke=0, fill=1)
            canvas.setFillColor(AZUL_C)
            canvas.rect(0, H - 26*mm, W, 1.2*mm, stroke=0, fill=1)
            logo_h = 9.5*mm
            logo_w = logo_h * (3753.0/705.0)
            logo = os.path.join(ASSETS, "logo_portilho_ic_branco.png")
            if os.path.exists(logo):
                canvas.drawImage(logo, 20*mm, H - 26*mm + (26*mm - logo_h)/2.0 + 0.6*mm,
                                 width=logo_w, height=logo_h, mask="auto")
            else:  # sem o arquivo do logo: marca em texto
                canvas.setFillColor(colors.white)
                canvas.setFont("Carlito-B", 17)
                canvas.drawString(20*mm, H - 15*mm, "PORTILHO")
                canvas.setFont("Carlito", 10.5)
                canvas.drawString(20*mm + canvas.stringWidth("PORTILHO", "Carlito-B", 17) + 3*mm, H - 15*mm, u"Intelig\u00eancia Comercial")
            canvas.setFillColor(AZUL)
            canvas.rect(0, 0, W, 10*mm, stroke=0, fill=1)
            canvas.setFillColor(AZUL_C)
            canvas.rect(0, 10*mm - 1.0*mm, W, 1.0*mm, stroke=0, fill=1)

        canvas.setFillColor(CINZA)
        canvas.setFont("Carlito", 8.5)
        canvas.drawString(20*mm, 15*mm, m["rodape_txt"])
        canvas.drawRightString(W - 20*mm, 15*mm, u"P á g i n a  " + str(doc.page))
        canvas.restoreState()
    return decorate

def gerar_pdf(caminho, md, marca="portilho", rodape_extra=None):
    """Gera num arquivo temporario e so entao substitui o definitivo.
    Se o PDF estiver aberto num leitor (lock do Windows), nao perde o trabalho:
    mantem o .novo.pdf ao lado e avisa."""
    tmp = caminho + ".novo"
    _gerar_pdf(tmp, md, marca, rodape_extra)
    try:
        os.replace(tmp, caminho)
        return caminho
    except PermissionError:
        destino = caminho.replace(".pdf", "_NOVO.pdf")
        try:
            os.replace(tmp, destino)
        except Exception:
            destino = tmp
        print("  !! ARQUIVO ABERTO NOUTRO PROGRAMA -> gravei em", os.path.basename(destino))
        return destino

def _gerar_pdf(caminho, md, marca="portilho", rodape_extra=None):
    m = dict(MARCAS[marca])
    if rodape_extra:
        m["rodape_txt"] = rodape_extra
    s = montar_estilos(m)
    doc = BaseDocTemplate(caminho, pagesize=A4,
                          leftMargin=20*mm, rightMargin=20*mm,
                          topMargin=40*mm, bottomMargin=21*mm,
                          title=os.path.basename(caminho).replace(".pdf", ""),
                          author="Portilho Inteligencia Comercial")
    frame = Frame(20*mm, 21*mm, A4[0] - 40*mm, A4[1] - 40*mm - 21*mm,
                  leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    doc.addPageTemplates([PageTemplate(id="pad", frames=[frame],
                                       onPage=fazer_decorador(marca, m, s))])
    doc.build(md_para_flowables(md, s, m))
    return caminho
