#!/usr/bin/env python3
"""Regenerate Prepa_barthou/1ere_annee/index.html by scanning the 4 subject folders.
Usage: python3 regen_index.py <repo_root>

Rendu aligné sur celui de Kit_Revision_PCSI.html : onglets sticky, bandeau
"Sources" par matière, tableau N° / Intitulé / Lien avec lignes de section
("1. Cours Clarisse" / "2. Cours Profs").
"""
import sys
import os
import re
import html

SUBJECTS = [
    ("01_MATHS", "🔢", "Maths", "maths"),
    ("02_PHYSIQUE", "⚛️", "Physique", "physique"),
    ("03_CHIMIE", "🧪", "Chimie", "chimie"),
    ("04_SI", "⚙️", "SI", "si"),
]

BASE_URL = "https://plouf34.github.io/prepabarthou/Prepa_barthou/1ere_annee"

# Établissement(s) source des documents "Cours Profs" pour chaque matière
# (ville affichée à titre indicatif, sans classement — ce n'est pas le Kit de révision).
# 5e élément = (num_min, num_max) des fichiers "Cours Profs" attribués à cette source
# (None = source unique, capte tous les fichiers profs de la matière).
SUBJECT_SOURCES = {
    "01_MATHS": [("Lycée Louis Barthou", "Pau", "https://www.prepabarthou.fr/cours/my/courses.php", "../../logo-barthou.png", None, None)],
    "02_PHYSIQUE": [("Lycée Louis Barthou", "Pau", "https://www.prepabarthou.fr/cours/my/courses.php", "../../logo-barthou.png", None, None)],
    "03_CHIMIE": [
        ("Sainte-Geneviève — S. Falcou", "Versailles", "http://www.pcsi1.bginette.com/Chim/Polys.php", None, (1, 7), None),
        ("Janson de Sailly", "Paris", "http://chimie-pcsi-jds.net", None, (8, 11), None),
    ],
    "04_SI": [
        ("Jean Perrin — N. Mesnier", "Lyon", "http://nmesnier.free.fr/SII-PCSI.html", None, (0, 8), None),
        ("Gustave Eiffel — A. Roux", "Bordeaux", "https://aroux-sii.fr/", None, (9, 13), "psi*2627"),
    ],
}


def esc(s):
    return html.escape(s or "")


def is_clarisse(filename):
    return "_Clarisse_" in filename or "_Clarisse." in filename


def parse_number_and_title(filename):
    """Extrait le numéro de séquence et un intitulé lisible depuis le nom de fichier."""
    name = filename[:-5] if filename.endswith(".html") else filename
    display = name.replace("_", " ")
    m = re.match(r'^(\d+)[\s-]+(.*)$', display)
    num, rest = (m.group(1), m.group(2)) if m else ("", display)
    rest = re.sub(r'^\d{4}-\d{2}-\d{2}\s+', '', rest)
    rest = re.sub(r'\s+\d{4}-\d{2}-\d{2}\s*$', '', rest)
    return num, rest.strip()


def sources_bar(folder):
    items = SUBJECT_SOURCES.get(folder, [])
    if not items:
        return ""
    chips = ""
    for name, ville, url, icon, _num_range, password in items:
        icon_html = f'<img src="{esc(icon)}" class="source-icon" alt="">' if icon else "🏫"
        pin = f'<span class="source-pin">📍 {esc(ville)}</span>'
        if password:
            pin += f'<span class="source-pin">🔑 {esc(password)}</span>'
        if url:
            chips += (f'<div class="source-block">'
                      f'<a class="source-chip" href="{esc(url)}" target="_blank" rel="noopener">{icon_html} {esc(name)} {pin} <span class="arrow">↗</span></a>'
                      f'</div>')
        else:
            chips += (f'<div class="source-block">'
                      f'<span class="source-chip source-chip-static">{icon_html} {esc(name)} {pin}</span>'
                      f'</div>')
    label = "Source" if len(items) == 1 else "Sources"
    return f'<div class="sources-bar"><span class="sources-label">{label} :</span>{chips}</div>'


def table_row(num, titre, url):
    n_html = esc(num) if num else "—"
    if url:
        link_html = f'<a class="pill pill-sujet" href="{esc(url)}" target="_blank" rel="noopener">📄 Ouvrir</a>'
    else:
        link_html = '<span class="pill pill-off">—</span>'
    return (f'<tr><td class="col-n">{n_html}</td><td class="col-titre">{esc(titre)}</td>'
            f'<td class="col-link">{link_html}</td></tr>')


def section_row(title):
    return f'<tr class="section-row"><td colspan="3">{esc(title)}</td></tr>'


def empty_row():
    return '<tr><td colspan="3" class="empty-cell">Aucun fichier pour l\'instant.</td></tr>'


def table_open():
    return ('<table><thead><tr>'
            '<th class="col-n">N°</th><th class="col-titre">Intitulé</th>'
            '<th class="col-link">Lien</th></tr></thead><tbody>')


def table_close():
    return '</tbody></table>'


def build_subject_block(repo_root, folder, emoji, label, anchor):
    dir_path = os.path.join(repo_root, "Prepa_barthou", "1ere_annee", folder)
    files = []
    if os.path.isdir(dir_path):
        files = sorted(f for f in os.listdir(dir_path) if f.endswith(".html"))

    clarisse_files = [f for f in files if is_clarisse(f)]
    profs_files = [f for f in files if not is_clarisse(f)]

    body = table_open()
    body += section_row("1. Cours Clarisse")
    if clarisse_files:
        for f in clarisse_files:
            num, titre = parse_number_and_title(f)
            url = f"{BASE_URL}/{folder}/{f}"
            body += table_row(num, titre, url)
    else:
        body += empty_row()

    sources = SUBJECT_SOURCES.get(folder, [])
    if len(sources) <= 1:
        # Source unique (ou aucune) : un seul pavé "Cours Profs", comme avant.
        body += section_row("2. Cours Profs")
        if profs_files:
            for f in profs_files:
                num, titre = parse_number_and_title(f)
                url = f"{BASE_URL}/{folder}/{f}"
                body += table_row(num, titre, url)
        else:
            body += empty_row()
    else:
        # Plusieurs sources : un pavé "Cours Profs — <source>" par source,
        # les fichiers étant attribués selon leur numéro (num_range).
        assigned = set()
        section_idx = 2
        for name, ville, _url, _icon, num_range, _password in sources:
            short_name = name.split(" — ")[0]
            body += section_row(f"{section_idx}. Cours Profs — {short_name} ({ville})")
            section_idx += 1
            matched = []
            for f in profs_files:
                num, _titre = parse_number_and_title(f)
                if num_range and num.isdigit() and num_range[0] <= int(num) <= num_range[1]:
                    matched.append(f)
                    assigned.add(f)
            if matched:
                for f in matched:
                    num, titre = parse_number_and_title(f)
                    url = f"{BASE_URL}/{folder}/{f}"
                    body += table_row(num, titre, url)
            else:
                body += empty_row()
        leftover = [f for f in profs_files if f not in assigned]
        if leftover:
            body += section_row(f"{section_idx}. Cours Profs — autres")
            for f in leftover:
                num, titre = parse_number_and_title(f)
                url = f"{BASE_URL}/{folder}/{f}"
                body += table_row(num, titre, url)
    body += table_close()

    return (f'<section id="{anchor}" class="subject">'
            f'<h2 class="subject-title">{emoji} {esc(label)}</h2>'
            f'{sources_bar(folder)}{body}</section>')


def main():
    repo_root = sys.argv[1] if len(sys.argv) > 1 else "."
    blocks = "".join(build_subject_block(repo_root, folder, emoji, label, anchor)
                      for folder, emoji, label, anchor in SUBJECTS)
    nav_links = "".join(f'<a href="#{anchor}">{emoji} {esc(label)}</a>'
                         for _, emoji, label, anchor in SUBJECTS)

    out = f"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<title>Prépa Barthou — 1ère année</title>
<link rel="icon" type="image/png" sizes="32x32" href="../../favicon-32.png">
<link rel="apple-touch-icon" href="../../apple-touch-icon.png">
<style>
  :root {{
    --bg: #f2f2f7;
    --card-bg: #ffffff;
    --text: #1c1c1e;
    --sub: #6e6e73;
    --accent: #0a63d3;
    --accent-2: #0a8a4a;
    --border: #e2e2e7;
    --nav-bg: rgba(255,255,255,0.92);
    --section-bg: #dfe8f7;
    --section-text: #1F4E78;
    --row-alt: #fafafc;
  }}
  @media (prefers-color-scheme: dark) {{
    :root {{
      --bg: #000000;
      --card-bg: #1c1c1e;
      --text: #f5f5f7;
      --sub: #9a9a9e;
      --accent: #4da3ff;
      --accent-2: #4fd97a;
      --border: #2c2c2e;
      --nav-bg: rgba(28,28,30,0.92);
      --section-bg: #16344f;
      --section-text: #bcd6f2;
      --row-alt: #232325;
    }}
  }}
  * {{ box-sizing: border-box; -webkit-tap-highlight-color: transparent; }}
  html, body {{
    margin: 0; padding: 0;
    background: var(--bg);
    color: var(--text);
    font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "Segoe UI", Roboto, sans-serif;
    -webkit-font-smoothing: antialiased;
  }}
  header {{ padding: max(env(safe-area-inset-top, 14px), 14px) 16px 8px 16px; text-align: center; }}
  .crosslinks {{ display:flex; justify-content:center; align-items:center; gap:14px; margin-bottom:8px; flex-wrap:wrap; }}
  .crosslinks a {{ display:inline-flex; align-items:center; gap:4px; font-size:12px; font-weight:600; color:var(--accent); text-decoration:none; }}
  .crosslinks img {{ height:16px; width:auto; border-radius:3px; vertical-align:middle; }}
  header h1 {{ font-size: 19px; margin: 4px 0 2px 0; font-weight: 700; }}
  header h1 a {{ display:flex; align-items:center; justify-content:center; gap:8px; color:var(--text); text-decoration:none; }}
  header h1 img {{ height:26px; width:auto; vertical-align:middle; }}
  header p {{ margin: 0; color: var(--sub); font-size: 12px; }}
  html {{ scroll-behavior: smooth; }}
  nav#tabs {{
    position: sticky; top: 0; z-index: 20;
    display: flex; gap: 4px; overflow-x: auto;
    max-width: 760px; margin: 0 auto;
    padding: 6px 8px;
    -webkit-overflow-scrolling: touch;
  }}
  nav#tabs a {{
    flex: 1 1 0; border-radius: 16px;
    padding: 6px 4px; font-size: 12px; font-weight: 600;
    background: var(--card-bg); color: var(--text);
    text-decoration: none; white-space: nowrap;
    border: 1px solid var(--border);
    text-align: center;
  }}
  nav#tabs a.tab-home {{ flex: 0 0 auto; padding: 6px 10px; }}
  main {{ padding: 10px 8px 40px 8px; max-width: 760px; margin: 0 auto; }}
  .subject {{ scroll-margin-top: 56px; padding-top: 4px; }}
  .subject-title {{
    font-size: 18px; font-weight: 700; margin: 22px 4px 6px 4px;
    padding-top: 10px; border-top: 1px solid var(--border);
  }}
  .subject:first-of-type .subject-title {{ border-top: none; margin-top: 4px; }}

  .sources-bar {{ display: flex; flex-wrap: wrap; align-items: center; gap: 6px; padding: 8px 6px 10px 6px; font-size: 12px; }}
  .sources-label {{ color: var(--sub); font-weight: 600; }}
  .source-chip {{
    display: inline-flex; align-items: center; gap: 4px;
    background: var(--card-bg); border: 1px solid var(--border);
    padding: 5px 10px; border-radius: 14px;
    color: var(--accent); font-weight: 600; text-decoration: none; font-size: 12px;
  }}
  .source-chip-static {{ color: var(--text); }}
  .source-chip .arrow {{ opacity: .6; }}
  .source-icon {{ height:14px; width:auto; border-radius:2px; vertical-align:middle; }}
  .source-block {{ display: flex; }}
  .source-pin {{ opacity: .65; font-weight: 500; font-size: 11px; }}

  table {{
    width: 100%; border-collapse: collapse;
    background: var(--card-bg); border-radius: 12px;
    overflow: hidden; font-size: 12.5px;
    border: 1px solid var(--border);
  }}
  thead th {{
    background: #1F4E78; color: #fff;
    font-size: 11px; text-transform: uppercase; letter-spacing: .03em;
    padding: 8px 6px; text-align: left; font-weight: 700;
  }}
  tbody tr:nth-child(even):not(.section-row) {{ background: var(--row-alt); }}
  tbody tr:not(.section-row) {{ border-top: 1px solid var(--border); }}
  td {{ padding: 7px 6px; vertical-align: middle; }}
  .section-row td {{
    background: var(--section-bg); color: var(--section-text);
    font-weight: 700; font-size: 11.5px; text-transform: uppercase;
    letter-spacing: .02em; padding: 7px 8px;
  }}
  .col-n {{ width: 40px; color: var(--sub); font-size: 11.5px; white-space: nowrap; }}
  .col-titre {{ min-width: 140px; }}
  .col-link {{ width: 1%; white-space: nowrap; text-align: center; }}
  .empty-cell {{ color: var(--sub); font-size: 12.5px; font-style: italic; text-align: center; }}

  .pill {{ display: inline-block; font-size: 11px; font-weight: 700; text-decoration: none; padding: 4px 8px; border-radius: 8px; white-space: nowrap; }}
  .pill-sujet {{ background: rgba(10,99,211,0.12); color: var(--accent); }}
  .pill-off {{ color: var(--sub); font-size: 12px; }}

  footer {{ text-align: center; padding: 16px; color: var(--sub); font-size: 10.5px; }}

  @media (max-width: 420px) {{ table {{ font-size: 11.5px; }} nav#tabs a {{ font-size: 11px; padding: 6px 2px; }} }}
</style>
</head>
<body>

<header>
  <div class="crosslinks">
    <a href="../../index.html">🏠 Accueil</a>
    <a href="../../Kit_Revision_PCSI.html">🎯 Kit de révision PCSI</a>
  </div>
  <h1><a href="https://www.prepabarthou.fr/cours/my/courses.php" target="_blank" rel="noopener"><img src="../../logo-barthou.png" alt="">Prépa Barthou — 1ère année</a></h1>
  <p>Cours, TD et exercices — mis à jour au fil de l'année</p>
</header>

<nav id="tabs">
  <a href="../../index.html" class="tab-home" title="Accueil">🏠</a>
{nav_links}
</nav>

<main>
{blocks}
</main>

<footer>Lien fixe — recharge la page pour voir les derniers fichiers ajoutés.</footer>

</body>
</html>
"""
    index_path = os.path.join(repo_root, "Prepa_barthou", "1ere_annee", "index.html")
    with open(index_path, "w", encoding="utf-8") as fh:
        fh.write(out)
    print(f"Wrote {index_path}")


if __name__ == "__main__":
    main()
