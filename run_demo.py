"""Démo de bout en bout, un scénario : simulation -> estimation -> ACF/PACF
-> prévision 5 pas -> graphique -> convergence Monte Carlo.

Usage : python run_demo.py [scénario] [sage|limite] [n_rep]
        (défaut : ar1 sage 200 ; n_rep != 200 suffixe les fichiers par _n<n_rep>)
"""
import sys
from pathlib import Path

import numpy as np

from simts import scenarios
from simts.diagnose import empirical_acf_pacf, ljung_box
from simts.experiment import DEFAULT_GRID, minimal_T_table, monte_carlo
from simts.fit import estimate, split
from simts.forecast import predict, rmse
from simts.generate import simulate
from simts.plots import plot_convergence, plot_coverage, plot_trajectory_forecast

OUT = Path(__file__).parent / "outputs"
OUT.mkdir(exist_ok=True)

name = sys.argv[1] if len(sys.argv) > 1 else "ar1"
cas = sys.argv[2] if len(sys.argv) > 2 else "sage"
model, order, params = scenarios.get(name, cas)
N_REP = int(sys.argv[3]) if len(sys.argv) > 3 else 200
tag = f"{name}_{cas}" + ("" if N_REP == 200 else f"_n{N_REP}")

print(f"=== {tag} : vrais paramètres = {params}")

# 1. Deux tailles : petit T et grand T
for T in (50, 1000):
    y = simulate(model, params, T, seed=42)
    train, test = split(y)
    est, res = estimate(train, model, order)
    print(f"\n--- T={T} (apprentissage {len(train)}, test 5)")
    print("estimés :", {k: np.round(v, 3).tolist() for k, v in est.items()})

    acf, pacf = empirical_acf_pacf(train, nlags=5)
    print("ACF  1..3 :", np.round(acf[1:4], 3))
    print("PACF 1..3 :", np.round(pacf[1:4], 3))

    resid = np.asarray(res.resid if model not in ("arch", "garch") else res.std_resid)
    print("Ljung-Box p (résidus)   :", round(ljung_box(resid), 3))
    print("Ljung-Box p (résidus^2) :", round(ljung_box(resid, squared=True), 3))

    pr = predict(res, model, h=5)
    if "ci" in pr:
        print("RMSE prévision (5 pas)  :", round(rmse(test, pr["mean"]), 3))
        plot_trajectory_forecast(
            y, pr["mean"], pr["ci"],
            title=f"{tag}, T={T} : trajectoire et prévisions",
            path=OUT / f"{tag}_T{T}_prevision.png",
        )
    else:
        print("variance prévue (5 pas) :", np.round(pr["var"], 3))
        print("variance empirique test :", np.round(test**2, 3))
        band = 1.96 * np.sqrt(pr["var"])
        plot_trajectory_forecast(
            y, np.zeros(5), np.column_stack([-band, band]),
            title=f"{tag}, T={T} : trajectoire et bande ±1.96σ prévue",
            path=OUT / f"{tag}_T{T}_prevision.png",
        )

# 2. Monte Carlo : combien d'observations ?
COV_MIN = 0.90
print(f"\n--- Monte Carlo ({N_REP} répétitions par T, grille {DEFAULT_GRID})")
mc = monte_carlo(model, order, params, DEFAULT_GRID, n_rep=N_REP, seed=0)
mc.to_csv(OUT / f"{tag}_montecarlo.csv", index=False)
print("RMSE relatif (erreur / vraie valeur) :")
print(mc.pivot(index="T", columns="param", values="rmse_rel").round(3))
print("Couverture de l'IC à 95 % (cible 0.95) :")
print(mc.pivot(index="T", columns="param", values="couverture").round(2))
plot_convergence(mc, title=f"{tag} : RMSE de l'estimateur selon T",
                 path=OUT / f"{tag}_convergence.png")
plot_coverage(mc, title=f"{tag} : couverture de l'IC à 95 %",
              path=OUT / f"{tag}_couverture.png")
for tol in (0.25, 0.10):
    per, overall = minimal_T_table(mc, tol, COV_MIN)
    print(f"T minimal (erreur relative <= {tol:.0%} ET couverture >= {COV_MIN:.0%},"
          " pour ce T et tous les plus grands) :")
    for p, t in per.items():
        print(f"  {p:8s} : {t if t is not None else 'jamais (grille jusqu a 2000)'}")
    print("  GLOBAL   :", overall if overall is not None else "jamais sur la grille")
