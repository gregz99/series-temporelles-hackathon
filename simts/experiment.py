"""Monte Carlo : combien d'observations faut-il ?

Pourquoi : une seule simulation ne prouve rien (un tirage chanceux ou
malchanceux). On répète N fois pour chaque T et on regarde trois choses :
  - le biais et le RMSE de l'estimateur (est-il juste ?),
  - le RMSE *relatif* à la vraie valeur (l'erreur est-elle petite par
    rapport à ce qu'on estime ?),
  - la couverture de l'IC à 95 % (l'incertitude annoncée par le logiciel
    est-elle honnête ?). Un IC qui couvre 70 % du temps est un logiciel qui
    ment sur sa propre précision.
Comment : mêmes graines pour tous les T (nombres aléatoires communs) afin
que les courbes soient comparables.
"""
import warnings

import numpy as np
import pandas as pd

from .fit import N_TEST, estimate, intervals, split
from .generate import simulate

DEFAULT_GRID = (20, 30, 50, 75, 100, 150, 200, 300, 500, 750, 1000, 2000)


def _flat(params):
    out = {}
    for k in ("phi", "theta", "alpha", "beta"):
        for i, v in enumerate(params.get(k, [])):
            out[f"{k}{i + 1}"] = v
    for k in ("sigma", "omega"):
        if k in params:
            out[k] = params[k]
    return out


def monte_carlo(model, order, params, T_grid=DEFAULT_GRID, n_rep=200, seed=0,
                dist="normal"):
    """Renvoie un DataFrame (T, param, vrai, biais, rmse, rmse_rel,
    couverture, echecs). `T` = taille d'apprentissage (les 5 valeurs test
    s'ajoutent)."""
    truth = _flat(params)
    rows = []
    for T in T_grid:
        ests, cis, fails = [], [], 0
        for r in range(n_rep):
            y = simulate(model, params, T + N_TEST, seed=seed + r, dist=dist)
            train, _ = split(y)
            try:
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore")
                    est, res = estimate(train, model, order)
                    ci = intervals(res, model)
                ests.append(_flat(est))
                cis.append(ci)
            except Exception:
                fails += 1
        df = pd.DataFrame(ests)
        for name, true_val in truth.items():
            if name not in df:
                continue
            err = df[name] - true_val
            # NaN (IC non calculable, souvent solution au bord) = non couvert
            covered = [
                (name in ci and ci[name][0] <= true_val <= ci[name][1])
                for ci in cis
            ]
            rows.append({
                "T": T, "param": name, "vrai": true_val,
                "biais": err.mean(), "rmse": np.sqrt((err**2).mean()),
                "rmse_rel": np.sqrt((err**2).mean()) / abs(true_val),
                "couverture": float(np.mean(covered)) if covered else np.nan,
                "echecs": fails,
            })
    return pd.DataFrame(rows)


def minimal_T(results, param, tol_rel=0.10, cov_min=0.90):
    """Plus petit T à partir duquel `param` est fiable *et le reste* :
    erreur relative <= tol_rel ET couverture de l'IC >= cov_min, pour ce T
    et pour tous les T plus grands de la grille.
    Renvoie None si le critère n'est jamais tenu jusqu'au bout.
    (Exiger « et tous les T plus grands » évite le faux positif d'un T qui
    passe par chance puis re-casse.)"""
    sub = results[results["param"] == param].sort_values("T")
    ok = ((sub["rmse_rel"] <= tol_rel) & (sub["couverture"] >= cov_min)).to_numpy()
    Ts = sub["T"].to_numpy()
    best = None
    for i in range(len(ok) - 1, -1, -1):
        if not ok[i]:
            break
        best = int(Ts[i])
    return best


def minimal_T_table(results, tol_rel=0.10, cov_min=0.90):
    """T minimal par paramètre + global (le plus exigeant des paramètres ;
    None si l'un d'eux n'est jamais fiable sur la grille)."""
    per = {p: minimal_T(results, p, tol_rel, cov_min)
           for p in results["param"].unique()}
    vals = list(per.values())
    overall = None if any(v is None for v in vals) else max(vals)
    return per, overall
