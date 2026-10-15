"""Graphiques de la prévision glissante Brent.

1. couverture glissante dans le temps (fenêtre de 100 jours) ;
2. IC à 95 % superposés aux rendements, autour de 2019 / 2020 / 2026.
Chaque date n'apparaît qu'une fois (origines tous les 5 jours, h=1..5), donc
les graphiques mélangent les horizons 1 à 5.
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).parent
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)
NOMS = {"ar1": "AR(1), variance constante", "garch_n": "GARCH gaussien",
        "garch_t": "GARCH Student"}
COUL = {"ar1": "#c0392b", "garch_n": "#7f8c8d", "garch_t": "#1f4e79"}
WIN = 100

d = {}
for k in NOMS:
    x = pd.read_csv(ROOT / "data" / f"rolling_{k}.csv", parse_dates=["date"])
    x = x.sort_values("date").set_index("date")
    x["ok"] = ((x.y >= x.lo) & (x.y <= x.hi)).astype(float)
    d[k] = x

# ---- 1. couverture glissante
fig, ax = plt.subplots(figsize=(11, 4.6))
se = np.sqrt(0.95 * 0.05 / WIN)
ax.axhspan(0.95 - 1.96 * se, min(1.0, 0.95 + 1.96 * se), color="#bbbbbb",
           alpha=0.35, label=f"zone de bruit attendu (n={WIN})")
ax.axhline(0.95, color="black", lw=1, ls="--")
for k, x in d.items():
    ax.plot(x.index, x.ok.rolling(WIN).mean(), color=COUL[k], lw=1.6,
            label=NOMS[k])
ax.axvspan(pd.Timestamp("2020-01-01"), pd.Timestamp("2020-12-31"),
           color="#f4d03f", alpha=0.18)
ax.text(pd.Timestamp("2020-02-01"), 0.52, "2020", fontsize=9)
ax.set_ylim(0.5, 1.02)
ax.set_ylabel(f"couverture réalisée (moy. glissante {WIN} j)")
ax.set_title("IC à 95 % : couverture réalisée dans le temps (Brent, rendements journaliers)")
ax.legend(loc="lower left", fontsize=8.5)
ax.grid(alpha=0.25)
fig.tight_layout()
fig.savefig(OUT / "brent_couverture_glissante.png", dpi=150)
plt.close(fig)

# ---- 2. IC superposés aux rendements
PANELS = [("2019-04-01", "2019-12-31", "Avant : avril-déc. 2019"),
          ("2020-01-01", "2020-12-31", "Pendant : 2020"),
          ("2026-01-01", "2026-10-31", "Après : 2026")]
fig, axes = plt.subplots(len(PANELS), 1, figsize=(11, 11))
for ax, (a, b, titre) in zip(axes, PANELS):
    g = d["garch_t"].loc[a:b]
    c = d["ar1"].loc[a:b]
    ax.fill_between(c.index, c.lo, c.hi, color=COUL["ar1"], alpha=0.14,
                    label="IC AR(1), variance constante")
    ax.plot(g.index, g.lo, color=COUL["garch_t"], lw=1)
    ax.plot(g.index, g.hi, color=COUL["garch_t"], lw=1, label="IC GARCH Student")
    miss_c = c[c.ok == 0]
    miss_g = g[g.ok == 0]
    ax.plot(g.index, g.y, ".", color="#555555", ms=3, label="rendement réalisé")
    ax.plot(miss_c.index, miss_c.y, "o", mfc="none", mec=COUL["ar1"], ms=7,
            label=f"hors IC AR(1) : {len(miss_c)}/{len(c)}")
    ax.plot(miss_g.index, miss_g.y, "x", color=COUL["garch_t"], ms=7,
            label=f"hors IC GARCH-t : {len(miss_g)}/{len(g)}")
    ax.set_title(titre, fontsize=10, loc="left")
    ax.set_ylabel("rendement (%)")
    ax.grid(alpha=0.25)
    ax.legend(fontsize=8, loc="upper center", bbox_to_anchor=(0.5, -0.1), ncol=5,
              frameon=False)
fig.suptitle("Brent : IC à 95 % prévus et rendements réalisés", y=0.995)
fig.tight_layout()
fig.savefig(OUT / "brent_ic_vs_rendements.png", dpi=150)
plt.close(fig)
print("OK")
