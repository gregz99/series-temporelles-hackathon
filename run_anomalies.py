"""Monte Carlo avec anomalie : que coûte une anomalie à l'estimation et à la
prévision ?

Usage : python run_anomalies.py <scénario> <anomalie> [n_rep]
        scénario : ar1, ma1, arima11, garch11 (cas « sage »)
        anomalie : ref, outlier, niveau, volatilite, queues

Pour chaque T de la grille et chaque répétition :
  - on simule N = T + 5 points avec l'anomalie au milieu ;
  - on estime sur les T premiers, on prévoit les 5 derniers ;
  - on relève l'erreur sur chaque paramètre, la couverture de son IC à 95 %,
    l'erreur de prévision et la part des 5 valeurs test tombant dans
    l'intervalle de prévision à 95 %.
"""
import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd

from simts import scenarios
from simts.anomalies import simulate_with_anomaly
from simts.experiment import _flat
from simts.fit import N_TEST, estimate, intervals, split
from simts.forecast import predict

GRID = (100, 250, 500, 1000)
Z = 1.959964


def main(name, kind, n_rep):
    model, order, params = scenarios.get(name, "sage")
    truth = {k: v for k, v in _flat(params).items() if k not in ("sigma", "omega")}
    rows = []
    for T in GRID:
        ests, covs, rm, pc, fails = [], [], [], [], 0
        for r in range(n_rep):
            y = simulate_with_anomaly(model, params, T + N_TEST, kind, seed=r)
            train, test = split(y)
            try:
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore")
                    est, res = estimate(train, model, order)
                    ci = intervals(res, model)
                    pr = predict(res, model, h=N_TEST)
            except Exception:
                fails += 1
                continue
            e = _flat(est)
            ests.append({k: e.get(k, np.nan) for k in truth})
            covs.append({k: (k in ci and ci[k][0] <= truth[k] <= ci[k][1]) for k in truth})
            m = np.asarray(pr["mean"])
            if "ci" in pr:
                lo, hi = pr["ci"][:, 0], pr["ci"][:, 1]
            else:
                sd = np.sqrt(np.asarray(pr["var"]))
                lo, hi = m - Z * sd, m + Z * sd
            rm.append(float(np.sqrt(np.mean((test - m) ** 2))))
            pc.append(float(np.mean((test >= lo) & (test <= hi))))
        E, C = pd.DataFrame(ests), pd.DataFrame(covs)
        for k, v in truth.items():
            err = E[k] - v
            rows.append({"modele": name, "anomalie": kind, "T": T, "param": k,
                         "vrai": v, "biais": err.mean(),
                         "rmse": float(np.sqrt((err ** 2).mean())),
                         "couverture": float(C[k].mean()),
                         "rmse_prev": float(np.mean(rm)),
                         "couv_prev": float(np.mean(pc)),
                         "echecs": fails, "n": len(E)})
    out = Path(__file__).parent / "data" / "anomalies"
    out.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_csv(out / f"{name}_{kind}.csv", index=False)
    print(name, kind, "ok")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else 500)
