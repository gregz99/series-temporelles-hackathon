"""Synthèse des Monte Carlo avec anomalies : tableaux et figure."""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).parent
D = ROOT / "data" / "anomalies"
MODELES = ["ar1", "ma1", "arima11", "garch11"]
NOMS = {"ar1": "AR(1)", "ma1": "MA(1)", "arima11": "ARIMA(1,1,1)", "garch11": "GARCH(1,1)"}
KINDS = ["ref", "outlier", "niveau", "volatilite", "queues"]
KNOMS = {"ref": "aucune (référence)", "outlier": "valeur aberrante (+8 σ)",
         "niveau": "décalage de niveau (+3 σ)", "volatilite": "volatilité ×3",
         "queues": "queues épaisses (Student 3)"}
MAIN = {"ar1": "phi1", "ma1": "theta1", "arima11": "phi1", "garch11": "alpha1"}

a = pd.concat([pd.read_csv(f) for f in D.glob("*.csv")])
pd.options.display.float_format = "{:.2f}".format


def pick(m, k, T, col, param=None):
    d = a[(a.modele == m) & (a.anomalie == k) & (a["T"] == T)]
    d = d[d.param == (param or MAIN[m])]
    return float(d[col].iloc[0])


for T in (250, 1000):
    print(f"\n########## T = {T}")
    rows = []
    for m in MODELES:
        for k in KINDS:
            rows.append({
                "modèle": NOMS[m], "anomalie": KNOMS[k], "param": MAIN[m],
                "biais": pick(m, k, T, "biais"),
                "RMSE": pick(m, k, T, "rmse"),
                "RMSE/réf": pick(m, k, T, "rmse") / pick(m, "ref", T, "rmse"),
                "couv IC": pick(m, k, T, "couverture"),
                "RMSE prév/réf": pick(m, k, T, "rmse_prev") / pick(m, "ref", T, "rmse_prev"),
                "couv prév": pick(m, k, T, "couv_prev"),
            })
    print(pd.DataFrame(rows).to_string(index=False))

# ---- figure : couverture de l'IC du paramètre principal et inflation du RMSE
T0 = 500
fig, axes = plt.subplots(1, 3, figsize=(13, 4.3))
labels_k = [KNOMS[k].replace(" (", "\n(") for k in KINDS]
for ax, (col, titre, cmap, vmin, vmax, fmt) in zip(axes, [
        ("couverture", f"Couverture de l'IC à 95 % du paramètre\n(T = {T0}, cible 0,95)", "RdYlGn", 0.3, 1.0, "{:.2f}"),
        ("rmse_ratio", f"Erreur d'estimation relative à la référence\n(T = {T0}, 1 = sans anomalie)", "YlOrRd", 1.0, 3.0, "{:.1f}"),
        ("couv_prev", f"Prévision à 5 pas : valeurs test dans l'IC à 95 %\n(T = {T0}, cible 0,95)", "RdYlGn", 0.3, 1.0, "{:.2f}")]):
    M = np.zeros((len(KINDS), len(MODELES)))
    for j, m in enumerate(MODELES):
        for i, k in enumerate(KINDS):
            if col == "rmse_ratio":
                M[i, j] = pick(m, k, T0, "rmse") / pick(m, "ref", T0, "rmse")
            else:
                M[i, j] = pick(m, k, T0, col)
    im = ax.imshow(M, cmap=cmap, vmin=vmin, vmax=vmax, aspect="auto")
    ax.set_xticks(range(len(MODELES)))
    ax.set_xticklabels([NOMS[m] for m in MODELES], rotation=20, fontsize=8)
    ax.set_yticks(range(len(KINDS)))
    ax.set_yticklabels(labels_k if ax is axes[0] else [""] * len(KINDS), fontsize=8)
    for i in range(len(KINDS)):
        for j in range(len(MODELES)):
            ax.text(j, i, fmt.format(M[i, j]), ha="center", va="center", fontsize=9)
    ax.set_title(titre, fontsize=9.5)
fig.tight_layout()
fig.savefig(ROOT / "outputs" / "rapport_anomalies.png", dpi=170)
print("\nfigure OK")
