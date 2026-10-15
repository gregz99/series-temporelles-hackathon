"""Tests de significativité sur la prévision glissante Brent (IC à 80 %).

1. Diebold-Mariano : le score d'intervalle de TimesFM diffère-t-il de celui
   des autres modèles ? Différentielle de perte d_t = S_TimesFM - S_autre,
   régression sur une constante avec variance HAC (Newey-West, 5 retards :
   les 5 jours d'une même origine partagent les mêmes paramètres).
   d_t < 0 : TimesFM meilleur.
2. Robustesse : même test sur h=1 seul (une observation par origine).
3. Kupiec : la couverture réalisée est-elle compatible avec 80 % ?
   (test binomial, indicatif : prévisions corrélées).
"""
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy import stats

D = Path(__file__).parent / "data"
AL = 0.20
NOMS = {"ar1": "AR(1)", "arma11": "ARIMA(1,1,1)", "garch_n": "GARCH gaussien",
        "garch_t": "GARCH Student", "timesfm": "TimesFM 3.0"}


def charge(k):
    d = pd.read_csv(D / f"rolling_{k}.csv", parse_dates=["date"]).sort_values("date")
    d["score"] = ((d.hi80 - d.lo80) + (2 / AL) * (d.lo80 - d.y).clip(lower=0)
                  + (2 / AL) * (d.y - d.hi80).clip(lower=0))
    d["err2"] = (d.y - d["mean"]) ** 2
    d["ok"] = ((d.y >= d.lo80) & (d.y <= d.hi80)).astype(float)
    return d.set_index(["date", "h"])


M = {k: charge(k) for k in NOMS}


def dm(a, b, col, mask=None, lags=5):
    d = (M[a][col] - M[b][col]).dropna()
    if mask is not None:
        d = d[mask(d.index)]
    d = d.sort_index(level="date")
    res = sm.OLS(d.to_numpy(), np.ones(len(d))).fit(cov_type="HAC", cov_kwds={"maxlags": lags})
    return float(res.params[0]), float(res.tvalues[0]), float(res.pvalues[0]), len(d)


PER = {
    "Total": None,
    "2015-2019": lambda i: (i.get_level_values("date").year >= 2015) & (i.get_level_values("date").year <= 2019),
    "2020": lambda i: i.get_level_values("date").year == 2020,
    "2021-2025": lambda i: (i.get_level_values("date").year >= 2021) & (i.get_level_values("date").year <= 2025),
    "2026": lambda i: i.get_level_values("date").year == 2026,
    "h=1 seul": lambda i: i.get_level_values("h") == 1,
}

rows = []
for autre in ("ar1", "arma11", "garch_n", "garch_t"):
    for col, nom_col in (("score", "score d'intervalle"), ("err2", "erreur quadratique")):
        for per, f in PER.items():
            moy, t, p, n = dm("timesfm", autre, col, f, lags=1 if per == "h=1 seul" else 5)
            rows.append({"TimesFM contre": NOMS[autre], "perte": nom_col, "période": per,
                         "écart moyen": moy, "t (HAC)": t, "p": p, "n": n})
res = pd.DataFrame(rows)
res.to_csv(D / "dm_tests.csv", index=False)

pd.options.display.float_format = "{:.3f}".format
for nom_col in ("score d'intervalle", "erreur quadratique"):
    print(f"\n===== Diebold-Mariano, perte = {nom_col} (écart < 0 : TimesFM meilleur)")
    t = res[res.perte == nom_col]
    print(t.pivot(index="période", columns="TimesFM contre", values="écart moyen")
          .reindex(list(PER))[[NOMS[k] for k in ("ar1", "arma11", "garch_n", "garch_t")]].to_string())
    print("p-valeurs :")
    print(t.pivot(index="période", columns="TimesFM contre", values="p")
          .reindex(list(PER))[[NOMS[k] for k in ("ar1", "arma11", "garch_n", "garch_t")]].to_string())

print("\n===== Kupiec : couverture à 80 % (p du test binomial contre 0.80)")
for k, nom in NOMS.items():
    x = M[k].ok.dropna()
    n, s = len(x), int(x.sum())
    p = stats.binomtest(s, n, 0.80).pvalue
    print(f"{nom:16s} couverture={s / n:.3f}  n={n}  p={p:.3f}")
