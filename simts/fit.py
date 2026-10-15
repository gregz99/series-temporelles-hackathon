"""Estimation des paramètres sur les T-5 premières valeurs.

Pourquoi : séparer l'estimation de la simulation permet de comparer plusieurs
logiciels sur la même série et de mesurer l'écart au vrai paramètre.
Comment : statsmodels pour ARMA/ARIMA, arch pour ARCH/GARCH. Les paramètres
estimés sont renvoyés sous les mêmes noms que ceux de simulate().
"""
import warnings

import numpy as np

N_TEST = 5  # consigne : les 5 dernières valeurs servent de test


def split(y, n_test=N_TEST):
    """(apprentissage = T-5 premières valeurs, test = 5 dernières)."""
    return y[:-n_test], y[-n_test:]


def estimate(train, model, order=None):
    """Ajuste le modèle. Renvoie (params_estimés, objet_résultat)."""
    if model in ("arch", "garch"):
        return _fit_garch(train, model)
    return _fit_arima(train, model, order)


def intervals(res, model):
    """IC à 95 % des paramètres, avec les mêmes noms « aplatis » que
    experiment._flat : phi1, theta1, alpha1, beta1, sigma, omega."""
    if model in ("arch", "garch"):
        df = res.conf_int()
        out = {}
        for key, name in (("omega", "omega"), ("alpha1", "alpha[1]"), ("beta1", "beta[1]")):
            if name in df.index:
                out[key] = (float(df.loc[name].iloc[0]), float(df.loc[name].iloc[1]))
        return out

    d = dict(zip(res.param_names, np.asarray(res.conf_int())))
    out = {}
    for k, v in d.items():
        if k.startswith("ar.L"):
            out[f"phi{k[4:]}"] = (float(v[0]), float(v[1]))
        elif k.startswith("ma.L"):
            out[f"theta{k[4:]}"] = (float(v[0]), float(v[1]))
        elif k == "sigma2":
            lo, hi = max(v[0], 0.0), max(v[1], 0.0)
            out["sigma"] = (float(np.sqrt(lo)), float(np.sqrt(hi)))
    return out


def _fit_arima(train, model, order):
    from statsmodels.tsa.arima.model import ARIMA

    # Pas de constante pour ar/ma/arma (processus centré), comme simulé.
    # Pour ARIMA avec d>0, statsmodels n'en ajoute pas non plus.
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        res = ARIMA(train, order=order, trend="n").fit()

    p, d, q = order
    names = res.param_names
    vals = dict(zip(names, np.asarray(res.params)))
    out = {
        "phi": [vals[f"ar.L{i}"] for i in range(1, p + 1)],
        "theta": [vals[f"ma.L{i}"] for i in range(1, q + 1)],
        "sigma": float(np.sqrt(vals["sigma2"])),
    }
    return out, res


def _fit_garch(train, model):
    try:
        from arch import arch_model
    except ImportError as e:  # pragma: no cover
        raise ImportError("pip install arch") from e

    p = 0 if model == "arch" else 1
    am = arch_model(train, mean="Zero", vol="GARCH", p=1, q=p)
    res = am.fit(disp="off")
    v = res.params
    out = {
        "omega": float(v["omega"]),
        "alpha": [float(v["alpha[1]"])],
        "beta": [float(v["beta[1]"])] if p else [],
    }
    return out, res
