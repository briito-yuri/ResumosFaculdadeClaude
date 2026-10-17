"""Converte resumos/<tema>/rascunho.md em resumo.html.

Uso: python3 templates/gerar_html.py resumos/<tema> [layout]

layout: "sinalizacao" (padrão) ou "editorial-suico". Cada layout está descrito em
templates/<layout>.md e o CSS em templates/<layout>.css.
O cabeçalho pode ser trocado no rascunho com <!-- kicker: Texto do cabeçalho -->.
O rascunho deve seguir a estrutura padrão: "# Título", subtítulo, parágrafo(s) de abertura,
seções "## N. Nome", subseções "### N.M Nome" e exemplos "#### Exemplo ...".
Seções com nome especial ganham estilo próprio: "Erros comuns", "Atalhos", "Exercícios",
"Gabarito" (começa em página nova), "Fontes" e "não conseguiu conferir" (destaque de limitações).
Etiquetas de origem ([ISUOG], [Outra fonte]...) e avisos "⚠ ver seção N" viram selos e links.
"""
import html
import os
import re
import sys

pasta = sys.argv[1]
src = os.path.join(pasta, "rascunho.md")
dst = os.path.join(pasta, "resumo.html")
layout = sys.argv[2] if len(sys.argv) > 2 else "sinalizacao"
css_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), layout + ".css")
FONTS = {
    "sinalizacao": "JetBrains+Mono:wght@400;700&family=Space+Grotesk:wght@400;600;700",
    "editorial-suico": "IBM+Plex+Mono:wght@400;600&family=Inter:wght@400;500;700;800",
}
md = open(src, encoding="utf-8").read()
m = re.search(r"<!--\s*kicker:\s*(.*?)\s*-->", md)
kicker = m.group(1) if m else "Sistemas de Informação · CESMAC"
md = md.split("<!-- STATUS")[0].rstrip().rstrip("-").rstrip()
md = re.sub(r"<!--.*?-->\n?", "", md, flags=re.S)  # comentários (ex.: <!-- layout: ... -->)
lines = md.split("\n")


ORIGEM = {"ISUOG": "isuog", "Consenso ISUOG": "consenso", "Outra fonte": "outra", "Prática/ensino": "pratica"}


def inline(t):
    t = html.escape(t, quote=False).replace(" ✔", "\u00a0✔")
    t = re.sub(r"(?:\*\*)?\[((ISUOG|Consenso ISUOG|Outra fonte|Prática/ensino)[^\]]*)\](?:\*\*)?",
               lambda m: f'<span class="origem origem-{ORIGEM[m.group(2)]}">{m.group(1)}</span>', t)
    t = re.sub(r"(?:\*\*)?⚠ ver seção (\d+)(?:\*\*)?", r'<a class="aviso" href="#s\1">⚠ ver seção \1</a>', t)
    t = re.sub(r"`([^`]+)`", r"<code>\1</code>", t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"(?<![\w*])\*([^*]+)\*(?!\w)", r"<em>\1</em>", t)
    return t


# ---------- 1. tokenizar em blocos ----------
blocks = []
i = 0
while i < len(lines):
    ln = lines[i]
    if not ln.strip() or ln.strip() == "---":
        i += 1
        continue
    if ln.startswith("```"):
        j = i + 1
        while not lines[j].startswith("```"):
            j += 1
        blocks.append(("code", "\n".join(lines[i + 1:j])))
        i = j + 1
        continue
    m = re.match(r"(#{1,4}) (.*)", ln)
    if m:
        blocks.append(("h%d" % len(m.group(1)), m.group(2)))
        i += 1
        continue
    if ln.startswith("|"):
        rows = []
        while i < len(lines) and lines[i].startswith("|"):
            cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
            if not all(re.fullmatch(r"-+", c) for c in cells):
                rows.append(cells)
            i += 1
        blocks.append(("table", rows))
        continue
    if ln.startswith(">"):
        q = []
        while i < len(lines) and lines[i].startswith(">"):
            q.append(lines[i].lstrip("> ").strip())
            i += 1
        blocks.append(("quote", " ".join(x for x in q if x)))
        continue
    if re.match(r"\d+\. ", ln):
        items = []
        while i < len(lines) and re.match(r"\d+\. ", lines[i]):
            items.append(re.sub(r"^\d+\. ", "", lines[i]))
            i += 1
        blocks.append(("ol", items))
        continue
    if ln.startswith("- "):
        items = []
        while i < len(lines) and lines[i].startswith("- "):
            items.append(lines[i][2:])
            i += 1
        blocks.append(("ul", items))
        continue
    para = []
    while i < len(lines) and lines[i].strip() and not re.match(r"(#|```|\||>|- |\d+\. |---)", lines[i]):
        para.append(lines[i])
        i += 1
    blocks.append(("p", para))

# ---------- 2. renderizar ----------
SPECIAL = [("erros", "erros"), ("atalhos", "atalhos"), ("exercicios", "exercícios"),
           ("gabarito", "gabarito"), ("fontes", "fontes"), ("limites", "conferir")]
KEY = ' class="key"'
out = []
section = None          # número da seção "##" atual
kind_of = ""            # tipo especial da seção: erros, atalhos, exercicios, gabarito, fontes
box_open = False


def close_box():
    global box_open
    if box_open:
        out.append("</div>")
        box_open = False


def result(text):
    return f'<p class="result"><mark>{inline(text)}</mark></p>'


def render_p(para):
    first = para[0]
    # gabarito: "**1. 77₁₀ = 1001101₂**"
    if first.startswith("Resultado:"):
        return result(first.replace("**", ""))
    # "... Logo, **X**." / "... → **X**."
    m = re.fullmatch(r"(.*?)(Logo, |→ )\*\*([^*]+)\*\*\.", first)
    if m and len(para) == 1:
        if m.group(2) == "→ ":
            return f"<p>{inline(m.group(1) + '→')}</p>" + result(m.group(3) + ".")
        return f"<p>{inline(m.group(1).rstrip())}</p>" + result("Logo, " + m.group(3) + ".")
    if first.startswith("**Conferência") or first.startswith("Conferência"):
        body = "<br>".join(inline(x) for x in para)
        if re.fullmatch(r"\*\*Conferência[^*]*:\*\*", first) and len(para) == 1:
            return f'<p class="conf-label">{inline(first.replace("**", ""))}</p>'
        return f'<p class="conf">{body}</p>'
    return "<p>" + "<br>".join(inline(x) for x in para) + "</p>"


def titled_item(text):
    """'**Título.** resto' ou '**Título:** resto' → título em negrito + explicação."""
    m = re.match(r"\*\*(.+?)\*\*\s*(.*)", text)
    if not m:
        return None
    title = m.group(1).rstrip(":")
    return title, m.group(2)


# cabeçalho: título, subtítulo e parágrafo(s) de abertura (tudo antes da primeira seção "##")
doc_title = blocks[0][1]
first_h2 = next(n for n, b in enumerate(blocks) if b[0] == "h2")
abertura = [" ".join(b[1]) for b in blocks[1:first_h2] if b[0] == "p"]
subtitle, intro = abertura[0], abertura[1:]

for kind, data in blocks[first_h2:]:
    if kind == "h1":
        continue  # cabeçalho montado à parte
    if kind == "h2":
        close_box()
        if section is not None:
            out.append("</section>")
        m = re.match(r"(\d+)\. (.*)", data)
        section = m.group(1)
        nome = m.group(2).lower()
        kind_of = next((k for k, chave in SPECIAL if chave in nome), "")
        extra = {"gabarito": ' class="page-break"', "limites": ' class="limites"'}.get(kind_of, "")
        out.append(f'<section id="s{section}"{extra}>')
        out.append(f'<h2><span class="tag">{section}</span><span>{inline(m.group(2))}</span></h2>')
        continue
    if kind == "h3":
        close_box()
        m = re.match(r"([\d.]+) (.*)", data)
        out.append(f'<h3><span class="tag tag-outline">{m.group(1)}</span><span>{inline(m.group(2))}</span></h3>')
        continue
    if kind == "h4":
        close_box()
        if data.startswith("Exemplo"):
            out.append('<div class="box">')
            box_open = True
            out.append(f"<h4>{inline(data)}</h4>")
        else:
            out.append(f'<h4 class="sub">{inline(data)}</h4>')
        continue
    if kind == "p":
        m = re.fullmatch(r"\*\*(\d+\. .+)\*\*", data[0])
        if kind_of == "gabarito" and m and len(data) == 1:
            close_box()
            out.append('<div class="box">')
            box_open = True
            out.append(result(m.group(1)))
            continue
        if kind_of == "fontes":
            close_box()
            out.append(f'<div class="important"><p>{inline(" ".join(data))}</p></div>')
            continue
        out.append(render_p(data))
        continue
    if kind == "code":
        out.append(f'<pre class="bits">{html.escape(data, quote=False)}</pre>')
        continue
    if kind == "quote":
        out.append(f'<div class="important"><p>{inline(data)}</p></div>')
        continue
    if kind == "table":
        head, *rows = data
        cls = "table-wrap text-table" if any(len(v) > 30 for r in rows for v in r) else "table-wrap"
        t = [f'<div class="{cls}"><table>', "<thead><tr>"]
        t += [f'<th{KEY if c == 0 else ""}>{inline(h)}</th>' for c, h in enumerate(head)]
        t.append("</tr></thead><tbody>")
        for r in rows:
            t.append("<tr>" + "".join(
                f'<td{KEY if c == 0 else ""}>{inline(v)}</td>' for c, v in enumerate(r)) + "</tr>")
        t.append("</tbody></table></div>")
        out.append("".join(t))
        continue
    if kind == "ol":
        if kind_of == "erros":
            lis = []
            for it in data:
                if not titled_item(it):
                    lis.append(f"<li>{inline(it)}</li>")
                    continue
                title, body = titled_item(it)
                lis.append(f'<li><strong class="item-title">{inline(title)}</strong> {inline(body)}</li>')
            out.append('<ol class="titled">' + "".join(lis) + "</ol>")
        elif kind_of == "exercicios":
            out.append('<ol class="ruled">' + "".join(f"<li>{inline(x)}</li>" for x in data) + "</ol>")
        else:
            out.append("<ol>" + "".join(f"<li>{inline(x)}</li>" for x in data) + "</ol>")
        continue
    if kind == "ul":
        if kind_of == "atalhos":
            lis, tail = [], ""
            for it in data:
                if not titled_item(it):
                    lis.append(f"<li>{inline(it)}</li>")
                    continue
                title, body = titled_item(it)
                body = body or " "
                if title.startswith("Sempre confira"):
                    tail = (f'<div class="important"><p><strong class="item-title">{inline(title)}</strong> '
                            f"{inline(body[0].upper() + body[1:])}</p></div>")
                    continue
                lis.append(f'<li><strong class="item-title">{inline(title)}</strong> '
                           f"{inline(body[0].upper() + body[1:])}</li>")
            out.append('<ul class="titled">' + "".join(lis) + "</ul>" + tail)
        elif kind_of == "fontes":
            lis = []
            for it in data:
                if " Disponível em: " not in it:
                    lis.append(f"<li><span>{inline(it)}</span></li>")
                    continue
                ref, rest = it.split(" Disponível em: ", 1)
                url, _, desc = rest.partition(" — ")
                desc = desc or " "
                lis.append(f'<li><strong>{inline(ref)}</strong>'
                           f'<a class="url" href="{html.escape(url)}">{html.escape(url)}</a>'
                           f"<span>{inline(desc[0].upper() + desc[1:])}</span></li>")
            out.append('<ul class="sources">' + "".join(lis) + "</ul>")
        else:
            out.append("<ul>" + "".join(f"<li>{inline(x)}</li>" for x in data) + "</ul>")
        continue

close_box()
out.append("</section>")

body = "\n".join(x for x in out if x)

css = open(css_path, encoding="utf-8").read().replace("{{RODAPE}}", doc_title.upper().replace('"', ""))
page = f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(doc_title)}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family={FONTS[layout]}&display=swap" rel="stylesheet">
<style>
{css}
</style>
</head>
<body>
<main>
<header>
<p class="kicker"><span>Resumo</span> {html.escape(kicker)}</p>
<h1>{inline(doc_title)}</h1>
<p class="subtitle">{inline(subtitle)}</p>
</header>
{"".join(f'<p class="intro">{inline(p)}</p>' for p in intro)}
{body}
</main>
</body>
</html>
"""
open(dst, "w", encoding="utf-8").write(page)
