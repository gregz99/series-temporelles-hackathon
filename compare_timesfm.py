"""Comparaison à 80 % : modèles classiques contre TimesFM 3.0 (Brent).

TimesFM ne fournit que les déciles : on compare donc la couverture de
l'intervalle [q0.1, q0.9] (cible 0.80) et le score d'intervalle (Winkler,
alpha=0.2 : largeur + pénalité sur les ratés, plus bas = mieux), plus
l'erreur de la prévision ponctuelle.
"""
from pathlib import Path

import numpy as np
import pandas as pd

D = Path(__file__).parent / "data"
NOMS = {"ar1": "AR(1)", "arma11": "ARIMA(1,1,1)", "garch_n": "GARCH gaussien",
        "garch_t": "GARCH Student", "timesfm": "TimesFM 3.0"}
AL = 0.20

a = []
for k, nom in NOMS.items():
    d = pd.read_csv(D / f"rolling_{k}.csv", parse_dates=["date"])
    d["modele"] = nom
    a.append(d)
a = pd.concat(a)
a["ok"] = ((a.y >= a.lo80) & (a.y <= a.hi80)).astype(float)
a["largeur"] = a.hi80 - a.lo80
a["score"] = (a.largeur + (2 / AL) * (a.lo80 - a.y).clip(lower=0)
              + (2 / AL) * (a.y - a.hi80).clip(lower=0))
a["err2"] = (a.y - a["mean"]) ** 2
a["err_abs"] = (a.y - a["mean"]).abs()


def periode(d):
    y = d.dt.year
    return np.select([y <= 2014, y <= 2019, y == 2020, y <= 2025],
                     ["2014", "2015-19", "2020", "2021-25"], "2026")


a["periode"] = periode(a.date)
ordre = ["AR(1)", "ARIMA(1,1,1)", "GARCH gaussien", "GARCH Student", "TimesFM 3.0"]
pers = ["2014", "2015-19", "2020", "2021-25", "2026", "Total"]


def table(col, agg="mean", fmt=3):
    t = a.pivot_table(index="periode", columns="modele", values=col, aggfunc=agg)
    t.loc["Total"] = a.groupby("modele")[col].agg(agg)
    return t.reindex(pers)[ordre].round(fmt)


print("Effectifs par période :", a[a.modele == "AR(1)"].groupby("periode").size().to_dict())
print("\n== Couverture réalisée de l'IC à 80 % (cible 0.80)")
print(table("ok").to_string())
print("\n== Largeur moyenne de l'IC à 80 % (points de %)")
print(table("largeur", fmt=2).to_string())
print("\n== Score d'intervalle à 80 % (plus bas = mieux)")
print(table("score", fmt=2).to_string())
print("\n== RMSE de la prévision ponctuelle (points de %)")
t = a.groupby(["periode", "modele"]).err2.mean().pow(0.5).unstack()
t.loc["Total"] = a.groupby("modele").err2.mean().pow(0.5)
print(t.reindex(pers)[ordre].round(3).to_string())

# Prévision nulle de référence : « le rendement de demain est 0 »
z = pd.Series((a[a.modele == "AR(1)"].y ** 2).values, index=a[a.modele == "AR(1)"].periode.values)
print("\nRMSE de la prévision nulle (référence), total :",
      round(float(np.sqrt(z.mean())), 3))

# Écart des scores par rapport au GARCH Student, par h
print("\n== Couverture à 80 % par horizon (total)")
print(a.pivot_table(index="h", columns="modele", values="ok").round(3)[ordre].to_string())
a.groupby(["periode", "modele"]).agg(
    couverture80=("ok", "mean"), largeur=("largeur", "mean"),
    score=("score", "mean"), rmse=("err2", lambda s: float(np.sqrt(s.mean())))
).round(4).to_csv(D / "comparaison_timesfm_80.csv")
