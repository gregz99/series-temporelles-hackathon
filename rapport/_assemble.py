"""Assemble le rapport restructuré autour des anomalies (script temporaire)."""
from pathlib import Path

R = Path(__file__).parent
old = (R / "rapport_v1_ic95.html").read_text(encoding="utf-8")
head = (R / "_head.html").read_text(encoding="utf-8")


def between(a, b):
    return old[old.index(a): old.index(b)]


modeles_tbl = between('<table>\n<tr><th class="l">Modèle</th><th class="l">Équation</th>',
                      "<h2>Couverture et nombre minimal d'observations</h2>")
brent_tests = between("<h2>5.1 Ce que justifient les données</h2>", "<h2>5.2 Prévision glissante")
brent_roll = between("<h2>5.2 Prévision glissante", "<h2>5.3 Ouverture")
brent_tfm = between("<h2>5.3 Ouverture", "<h1>6. Discussion et limites</h1>")
sec41 = between("<h2>4.1 Un tirage unique ne prouve rien</h2>", "<h2>4.2 Couverture des IC en fonction de T</h2>")
scen_tbl = between("<table>\n<caption>Tableau 1.", "<h2>3.2 Découpage et diagnostics</h2>")
annexe = old[old.index('<h1 class="newpage">Annexes</h1>'):]

brent_tests = brent_tests.replace("5.1 Ce que justifient les données", "6.1 Ce que justifient les données")
brent_roll = brent_roll.replace("5.2 Prévision glissante : variance constante contre GARCH",
                                "6.3 Prévision glissante : variance constante contre GARCH")
brent_tfm = brent_tfm.replace("5.3 Ouverture : TimesFM 3.0", "6.4 Ouverture : TimesFM 3.0")


def renum(txt):
    pairs = (("Figure 3.", "Figure 4."), ("Figure 4.", "Figure 5."), ("Figure 5.", "Figure 6."),
             ("Figure 6.", "Figure 7."), ("La Figure 5 est", "La Figure 6 est"),
             ("Tableau 4.", "Tableau 6."), ("Tableau 5.", "Tableau 8."), ("Tableau 6.", "Tableau 9."))
    for i, (a, b) in enumerate(pairs):
        txt = txt.replace(a, f"@@{i}@@")
    for i, (a, b) in enumerate(pairs):
        txt = txt.replace(f"@@{i}@@", b)
    return txt


brent_tests, brent_roll, brent_tfm = map(renum, (brent_tests, brent_roll, brent_tfm))
brent_tests = brent_tests.replace("18 % (2013), 123 % (2020), 72 % (2026)", "18 % (2013), 114 % (2020), 71 % (2026)")
brent_tests = brent_tests.replace("Tests préalables (4108 jours communs Brent/WTI).", "Tests préalables (4108 jours communs Brent/WTI ; volatilité : Brent seul).")
sec41 = sec41.replace("Tableau 2.", "Tableau 3.")
scen_tbl = scen_tbl.replace("Tableau 1.", "Tableau 2.")
annexe = annexe.replace(
    '<tr><td class="l"><code>python figures_rapport.py</code></td>',
    '<tr><td class="l"><code>python run_anomalies.py ar1 niveau 500</code><br>'
    '<code>python resume_anomalies.py</code></td>'
    '<td class="l">anomalies : simulation, puis synthèse et figure</td></tr>\n'
    '<tr><td class="l"><code>python figures_rapport.py</code></td>')

body = (R / "_corps.html").read_text(encoding="utf-8")
for key, val in {"@@MODELES@@": modeles_tbl, "@@SCEN@@": scen_tbl, "@@SEC41@@": sec41,
                 "@@BRENT_TESTS@@": brent_tests, "@@BRENT_ROLL@@": brent_roll,
                 "@@BRENT_TFM@@": brent_tfm, "@@ANNEXE@@": annexe}.items():
    body = body.replace(key, val)
(R / "rapport.html").write_text(head + body, encoding="utf-8")
print("assemblé :", len(head + body), "caractères")
