"""Construit diapositives.html (puis le PDF) et notes.md à partir des sources.

Les sources (source/*.html + deck.json) sont celles du deck publié dans l'outil
de présentation ; ce script en fait un document autonome, une page 1920×1080
par diapositive, avec les images locales du dossier outputs/.
"""
import json
import re
from pathlib import Path

R = Path(__file__).parent
SRC = R / "source"
IMAGES = {  # identifiant d'actif du deck -> fichier local
    "bf9a2d9c19d86d7fb21a1f9057e96667": "rapport_anomalies.png",
    "2c689cdfd910dc9c1af67af8f96ecff7": "rapport_brent_apercu.png",
    "3cc4b93035d49ed59305ba82be544c3c": "brent_couverture_glissante.png",
    "4a1b3cd6f59db11c9f1a5ed3599fa14c": "rapport_brent_couverture_periodes.png",
    "7470b224d4061226ea9347510e8df7ed": "brent_ic_vs_rendements.png",
}

deck = json.loads((SRC / "deck.json").read_text(encoding="utf-8"))
sections, notes = [], []
for n, sid in enumerate(deck["order"], 1):
    html = (SRC / f"{sid}.html").read_text(encoding="utf-8")
    m = re.search(r"<aside>(.*?)</aside>", html, re.S)
    if m:
        notes.append(f"## Diapositive {n} ({sid})\n\n{m.group(1).strip()}\n")
    html = re.sub(r"<aside>.*?</aside>", "", html, flags=re.S)
    for aid, name in IMAGES.items():
        html = html.replace(f"/_blob/{aid}", f"../outputs/{name}")
    sections.append(html)

css = """
@page { size: 1920px 1080px; margin: 0; }
html, body { margin: 0; padding: 0; }
section { width: 1920px; height: 1080px; position: relative; box-sizing: border-box;
          overflow: hidden; page-break-after: always; break-after: page; }
h1, h2, h3, p, ul, ol { margin: 0; }
ul, ol { padding-left: 44px; }
li { margin-bottom: 10px; }
hr { border: 0; margin: 0; }
img { display: block; }
table { border-collapse: collapse; }
th { background: #13263F; color: #F7F5EF; font-weight: 600; padding: 12px 20px; text-align: center; border: 1px solid #13263F; }
td { padding: 12px 20px; text-align: center; border: 1px solid #E1DCCF; background: #FFFFFF; }
tr:nth-child(even) td { background: #F1EEE5; }
"""
fonts = ('<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=EB+Garamond:wght@400..700'
         '&family=IBM+Plex+Sans:wght@400;500;600&display=swap">')
doc = (f'<!doctype html><html lang="fr"><head><meta charset="utf-8"><title>{deck["title"]}</title>'
       f'{fonts}<style>{css}</style></head><body>' + "\n".join(sections) + "</body></html>")
(R / "diapositives.html").write_text(doc, encoding="utf-8")
(R / "notes.md").write_text("# Notes d'orateur\n\n" + "\n".join(notes), encoding="utf-8")
print(len(deck["order"]), "diapositives")
