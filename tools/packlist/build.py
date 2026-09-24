# -*- coding: utf-8 -*-
"""Turn 26-行李清單.md into an interactive, tickable checklist page (packlist.html).

Every "- [ ] ..." line becomes a checkbox with a stable id (hash of its text), so
ticks survive re-publishing as long as the item wording is unchanged.
Run: python3 tools/packlist/build.py
"""
import hashlib, html, re, pathlib
import markdown

ROOT = pathlib.Path(__file__).resolve().parents[2]
SRC = ROOT / "26-行李清單.md"
OUT = pathlib.Path(__file__).resolve().parent / "packlist.html"

md_text = SRC.read_text(encoding="utf-8")

# ---- split into sections on "## " headings --------------------------------
title_m = re.search(r"^# (.+)$", md_text, re.M)
page_title = title_m.group(1).strip() if title_m else "行李清單"
parts = re.split(r"^## ", md_text, flags=re.M)
intro_md = re.sub(r"^# .+$", "", parts[0], count=1, flags=re.M).strip()
sections = []
for p in parts[1:]:
    head, _, body = p.partition("\n")
    sections.append((head.strip(), body.strip()))

MD = markdown.Markdown(extensions=["tables", "sane_lists"])
def render(s):
    MD.reset()
    out = MD.convert(s)
    out = re.sub(r"<a href=\"(https?://[^\"]+)\"", r'<a target="_blank" rel="noopener" href="\1"', out)
    out = out.replace("<table>", '<div class="tw"><table>').replace("</table>", "</table></div>")
    return out

TASK = re.compile(r"^(\s*)[-*] \[( |x|X)\] (.+)$")
seen = {}
def item_id(text):
    base = hashlib.sha1(text.encode("utf-8")).hexdigest()[:10]
    n = seen.get(base, 0); seen[base] = n + 1
    return base if n == 0 else f"{base}-{n}"

def inline(s):
    return render(s).removeprefix("<p>").removesuffix("</p>")

def render_section(body):
    """Render a section body; task lines become checkbox rows, the rest is markdown."""
    out, buf, tasks = [], [], []
    def flush_md():
        if buf:
            out.append(render("\n".join(buf))); buf.clear()
    def flush_tasks():
        if tasks:
            out.append('<ul class="checks">' + "".join(tasks) + "</ul>"); tasks.clear()
    sub = None
    for line in body.splitlines():
        m = TASK.match(line)
        if m:
            flush_md()
            text = m.group(3).strip()
            iid = item_id((sub or "") + "|" + text)
            owned = "✅已有" in text
            cls = "item owned" if owned else "item"
            tasks.append(
                f'<li class="{cls}" data-id="{iid}"><label>'
                f'<input type="checkbox" id="c-{iid}" data-id="{iid}">'
                f'<span class="box" aria-hidden="true"></span>'
                f'<span class="txt">{inline(text)}</span></label></li>')
            continue
        flush_tasks()
        if line.startswith("### "):
            sub = line[4:].strip()
        buf.append(line)
    flush_md(); flush_tasks()
    return "\n".join(out)

def slug(i):
    return f"s{i+1}"

nav, blocks = [], []
for i, (head, body) in enumerate(sections):
    sid = slug(i)
    body_html = render_section(body)
    n_items = body_html.count('class="item')
    label = re.sub(r"^[^\w一-鿿]+", "", head).strip() or head
    nav.append(f'<a class="chip" href="#{sid}" data-sec="{sid}"><span class="chip-t">{html.escape(label)}</span>'
               + (f'<span class="chip-n" data-count="{sid}">0/{n_items}</span>' if n_items else "") + "</a>")
    blocks.append(
        f'<section class="sec" id="{sid}" data-sec="{sid}">'
        f'<header class="sec-h"><h2>{html.escape(head)}</h2>'
        + (f'<span class="sec-n" data-count="{sid}">0/{n_items}</span>' if n_items else "")
        + f'</header><div class="sec-b">{body_html}</div></section>')

TEMPLATE = (pathlib.Path(__file__).resolve().parent / "template.html").read_text(encoding="utf-8")
page = (TEMPLATE
        .replace("{{TITLE}}", html.escape(page_title))
        .replace("{{INTRO}}", render(intro_md))
        .replace("{{NAV}}", "\n".join(nav))
        .replace("{{SECTIONS}}", "\n".join(blocks)))
OUT.write_text(page, encoding="utf-8")
print(f"wrote {OUT} · {len(sections)} sections · {sum(seen.values())} checkboxes · {len(page):,} bytes")
