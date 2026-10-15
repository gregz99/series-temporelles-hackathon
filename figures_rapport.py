"""Figures de synthèse du rapport (outputs/rapport_*.png)."""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).parent
OUT = ROOT / "outputs"
D = ROOT / "data"
SAGE, LIM = "#1f4e79", "#c0392b"
plt.rcParams.update({"font.size": 10, "axes.spines.top": False,
                     "axes.spines.right": False, "axes.grid": True,
                     "grid.alpha": 0.25})

# ---- A. couverture des IC de paramètres, sage contre limite (1000 rép.)
PANELS = [("ar1", "phi1", "AR(1) : $\\phi$"), ("ar2", "phi2", "AR(2) : $\\phi_2$"),
          ("ma1", "theta1", "MA(1) : $\\theta$"),
          ("arima11", "phi1", "ARIMA(1,1,1) : $\\phi$"),
          ("arch1", "alpha1", "ARCH(1) : $\\alpha$"),
          ("garch11", "alpha1", "GARCH(1,1) : $\\alpha$")]
se = 1.96 * np.sqrt(0.95 * 0.05 / 1000)
fig, axes = plt.subplots(2, 3, figsize=(11, 6), sharey=True)
for ax, (s, p, titre) in zip(axes.flat, PANELS):
    for cas, coul, ls in (("sage", SAGE, "-"), ("limite", LIM, "--")):
        d = pd.read_csv(OUT / f"{s}_{cas}_n1000_montecarlo.csv")
        d = d[d.param == p].sort_values("T")
        ax.plot(d["T"], d["couverture"], ls, color=coul, marker="o", ms=3,
                label=f"cas {cas}")
    ax.axhspan(0.95 - se, 0.95 + se, color="#bbbbbb", alpha=0.4)
    ax.axhline(0.95, color="black", lw=0.8, ls=":")
    ax.set_xscale("log")
    ax.set_ylim(0.55, 1.02)
    ax.set_title(titre, fontsize=10)
    ax.set_xlabel("T")
axes[0, 0].set_ylabel("couverture de l'IC à 95 %")
axes[1, 0].set_ylabel("couverture de l'IC à 95 %")
axes[0, 0].legend(loc="lower right", fontsize=8)
fig.suptitle("Couverture réalisée de l'IC à 95 % d'un paramètre (1000 répétitions)",
             y=0.995)
fig.tight_layout()
fig.savefig(OUT / "rapport_couverture_synthese.png", dpi=170)
plt.close(fig)

# ---- B. aperçu de Brent
s = pd.read_csv(ROOT / "data/raw/DCOILBRENTEU.csv", na_values=".",
                parse_dates=[0], index_col=0).iloc[:, 0].dropna().loc["2010":]
r = 100 * np.log(s).diff().dropna()
fig, ax = plt.subplots(3, 1, figsize=(10, 7.5), sharex=True)
ax[0].plot(s.index, s, color=SAGE, lw=1)
ax[0].set_ylabel("prix ($/baril)")
ax[1].plot(r.index, r, color="#555555", lw=0.6)
ax[1].set_ylabel("rendement journalier (%)")
vol = r.groupby(r.index.year).std() * np.sqrt(252)
ax[2].bar([pd.Timestamp(f"{y}-07-01") for y in vol.index], vol.values,
          width=250, color=LIM)
ax[2].set_ylabel("volatilité annualisée (%)")
for a in ax:
    a.axvspan(pd.Timestamp("2020-01-01"), pd.Timestamp("2020-12-31"),
              color="#f4d03f", alpha=0.18)
fig.suptitle("Brent (FRED, quotidien, 2010-2026) : prix, rendements, régimes de volatilité")
fig.tight_layout()
fig.savefig(OUT / "rapport_brent_apercu.png", dpi=170)
plt.close(fig)

# ---- C. couverture par période et par modèle (95 % puis 80 %)
NOMS = {"ar1": "AR(1)", "garch_n": "GARCH gaussien", "garch_t": "GARCH Student",
        "timesfm": "TimesFM 3.0"}
COUL = {"ar1": "#c0392b", "garch_n": "#7f8c8d", "garch_t": "#1f4e79",
        "timesfm": "#27ae60"}
PER = [("2014-19", 2014, 2019), ("2020", 2020, 2020),
       ("2021-25", 2021, 2025), ("2026", 2026, 2026)]


def cov(k, lo, hi, col_lo, col_hi, h=None):
    d = pd.read_csv(D / f"rolling_{k}.csv", parse_dates=["date"])
    if h is not None:
        d = d[d.h == h]
    out = []
    for _, a, b in PER:
        x = d[(d.date.dt.year >= a) & (d.date.dt.year <= b)]
        out.append(((x.y >= x[col_lo]) & (x.y <= x[col_hi])).mean())
    return out


fig, axes = plt.subplots(1, 2, figsize=(11, 4.3))
for ax, (niveau, cl, ch, cible, ks) in zip(
        axes, [("95 %", "lo", "hi", 0.95, ["ar1", "garch_n", "garch_t"]),
               ("80 %", "lo80", "hi80", 0.80, ["ar1", "garch_n", "garch_t", "timesfm"])]):
    w = 0.8 / len(ks)
    for i, k in enumerate(ks):
        vals = cov(k, None, None, cl, ch, h=1 if niveau == "95 %" else None)
        ax.bar(np.arange(len(PER)) + i * w - 0.4 + w / 2, vals, w,
               color=COUL[k], label=NOMS[k])
    ax.axhline(cible, color="black", ls="--", lw=1)
    ax.set_xticks(range(len(PER)))
    ax.set_xticklabels([p[0] for p in PER])
    ax.set_ylim(0.5, 1.13)
    ax.set_title(f"IC à {niveau} (cible {cible:.2f}), "
                 + ("horizon 1 jour" if niveau == "95 %" else "horizons 1 à 5 jours"),
                 fontsize=10)
    ax.set_ylabel("couverture réalisée")
    ax.legend(fontsize=8, loc="upper left", ncol=2)
fig.tight_layout()
fig.savefig(OUT / "rapport_brent_couverture_periodes.png", dpi=170)
plt.close(fig)
print("OK")
