"""Couverture réalisée des IC à 95 % et largeur moyenne, par période.

Lecture : couverture annoncée = 95 %. Le test binomial teste H0 « la vraie
couverture est 95 % » (les prévisions successives sont corrélées, donc la
p-valeur est indicative, pas exacte).
"""
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

D = Path(__file__).parent / "data"
NOMS = {"ar1": "AR(1)", "arma11": "ARIMA(1,1,1)",
        "garch_n": "GARCH gaussien", "garch_t": "GARCH Student"}
PERIODES = [
    ("2014-2019 (avant)", "2014-01-01", "2019-12-31"),
    ("2020 (crise)", "2020-01-01", "2020-12-31"),
    ("2021-2026 (après)", "2021-01-01", "2026-12-31"),
    ("Total", "2014-01-01", "2026-12-31"),
]

frames = []
for key, nom in NOMS.items():
    d = pd.read_csv(D / f"rolling_{key}.csv", parse_dates=["date"])
    d["modele"] = nom
    d["ok"] = (d.y >= d.lo) & (d.y <= d.hi)
    d["largeur"] = d.hi - d.lo
    frames.append(d)
a = pd.concat(frames)

lignes = []
for h in (1, 5):
    for nom_p, d0, d1 in PERIODES:
        sub = a[(a.h == h) & (a.date >= d0) & (a.date <= d1)]
        for nom in NOMS.values():
            s = sub[sub.modele == nom]
            n, k = len(s), int(s.ok.sum())
            p = stats.binomtest(k, n, 0.95).pvalue if n else np.nan
            lignes.append({"h": h, "periode": nom_p, "modele": nom, "n": n,
                           "couverture": k / n if n else np.nan,
                           "largeur_moy": s.largeur.mean(), "p_binom": p})
res = pd.DataFrame(lignes)
res.to_csv(D / "couverture_rolling.csv", index=False)

for h in (1, 5):
    print(f"\n===== Horizon h={h} jour(s) : couverture réalisée (cible 0.95)")
    t = res[res.h == h].pivot(index="periode", columns="modele", values="couverture")
    print(t.reindex([p[0] for p in PERIODES])[list(NOMS.values())].round(3).to_string())
    print("largeur moyenne de l'IC (points de %) :")
    t = res[res.h == h].pivot(index="periode", columns="modele", values="largeur_moy")
    print(t.reindex([p[0] for p in PERIODES])[list(NOMS.values())].round(2).to_string())

print("\nEffectifs (n par cellule, h=1) :",
      res[(res.h == 1) & (res.modele == "AR(1)")].set_index("periode").n.to_dict())

# Où sont les ratés ? jours les plus extrêmes non couverts par GARCH Student
g = a[(a.h == 1) & (a.modele == "GARCH Student") & (~a.ok)]
print("\nRatés du GARCH Student (h=1) par année :")
print(g.groupby(g.date.dt.year).size().to_string())
