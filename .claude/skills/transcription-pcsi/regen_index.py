#!/usr/bin/env python3
"""Regenerate Prepa_barthou/1ere_annee/index.html by scanning the 4 subject folders.
Usage: python3 regen_index.py <repo_root>
"""
import sys
import os
import html

SUBJECTS = [
    ("01_MATHS", "🔢", "Maths"),
    ("02_PHYSIQUE", "⚛️", "Physique"),
    ("03_CHIMIE", "🧪", "Chimie"),
    ("04_SI", "⚙️", "SI"),
]

BASE_URL = "https://plouf34.github.io/prepabarthou/Prepa_barthou/1ere_annee"

def display_name(filename):
    name = filename[:-5] if filename.endswith(".html") else filename
    return name.replace("_", " ")

def build_subject_block(repo_root, folder, emoji, label):
    dir_path = os.path.join(repo_root, "Prepa_barthou", "1ere_annee", folder)
    files = []
    if os.path.isdir(dir_path):
        files = sorted(f for f in os.listdir(dir_path) if f.endswith(".html"))
    if not files:
        return (
            f'<div class="subject"><h2 class="subject-title">{emoji} {html.escape(label)}</h2>'
            f'<div class="empty">Aucun fichier pour l\'instant.</div></div>'
        )
    items = []
    for f in files:
        url = f"{BASE_URL}/{folder}/{f}"
        name = html.escape(display_name(f))
        items.append(f'<li><a href="{url}" target="_blank" rel="noopener">📄 {name}</a></li>')
    return (
        f'<div class="subject"><h2 class="subject-title">{emoji} {html.escape(label)}</h2>'
        f'<ul class="file-list">{"".join(items)}</ul></div>'
    )

def main():
    repo_root = sys.argv[1] if len(sys.argv) > 1 else "."
    blocks = "".join(build_subject_block(repo_root, folder, emoji, label) for folder, emoji, label in SUBJECTS)

    out = f"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<title>Prépa Barthou — 1ère année</title>
<link rel="icon" type="image/svg+xml" href="../../favicon.svg">
<link rel="icon" type="image/png" sizes="32x32" href="../../favicon-32.png">
<link rel="apple-touch-icon" href="../../apple-touch-icon.png">
<style>
  :root {{
    --bg: #f2f2f7; --card-bg: #ffffff; --text: #1c1c1e; --sub: #6e6e73;
    --accent: #0a63d3; --border: #e2e2e7;
  }}
  @media (prefers-color-scheme: dark) {{
    :root {{ --bg:#000; --card-bg:#1c1c1e; --text:#f5f5f7; --sub:#9a9a9e; --accent:#4da3ff; --border:#2c2c2e; }}
  }}
  * {{ box-sizing: border-box; }}
  body {{ margin:0; background:var(--bg); color:var(--text);
    font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "Segoe UI", Roboto, sans-serif; }}
  header {{ padding: 20px 16px 10px; text-align:center; }}
  .crosslinks {{ display:flex; justify-content:center; gap:14px; margin-bottom:8px; }}
  .crosslinks a {{ font-size:12px; font-weight:600; color:var(--accent); text-decoration:none; }}
  header h1 {{ font-size:20px; margin:0; }}
  header p {{ color:var(--sub); font-size:12px; margin:4px 0 0; }}
  main {{ padding: 10px 14px 40px; max-width: 720px; margin:0 auto; }}
  .subject {{ margin: 18px 0; background:var(--card-bg); border:1px solid var(--border);
    border-radius: 14px; padding: 12px 16px; }}
  .subject-title {{ font-size:16px; margin:0 0 8px; }}
  .file-list {{ list-style:none; margin:0; padding:0; }}
  .file-list li {{ padding: 8px 0; border-top: 1px solid var(--border); }}
  .file-list li:first-child {{ border-top:none; }}
  .file-list a {{ color:var(--accent); text-decoration:none; font-weight:600; font-size:14px; }}
  .empty {{ color:var(--sub); font-size:13px; font-style:italic; }}
  footer {{ text-align:center; color:var(--sub); font-size:11px; padding:20px; }}
</style>
</head>
<body>
<header>
  <div class="crosslinks"><a href="../../index.html">🏠 Accueil</a><a href="../../Kit_Revision_PCSI.html">🎯 Kit de révision PCSI</a></div>
  <h1>📚 Prépa Barthou — 1ère année</h1>
  <p>Cours, TD et exercices — mis à jour au fil de l'année</p>
</header>
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
