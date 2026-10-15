"""Génération (simulation) de séries temporelles de vérité connue.

Pourquoi : on ne peut juger une estimation que si on connaît le vrai modèle.
Comment : récurrence écrite à la main avec un burn-in, graine fixée pour la
reproductibilité. Chaque modèle renvoie un tableau numpy de longueur T.
"""
import numpy as np

MODELS = ("ar", "ma", "arma", "arima", "arch", "garch")


def _innov(rng, n, dist="normal", df=5):
    """Innovations de variance 1 (gaussiennes ou Student normalisées)."""
    if dist == "normal":
        return rng.standard_normal(n)
    if dist == "t":
        return rng.standard_t(df, n) * np.sqrt((df - 2) / df)
    raise ValueError(f"dist inconnue : {dist}")


def simulate(model, params, T, seed=None, burn=200, dist="normal"):
    """Simule T observations.

    params selon le modèle :
      ar    : {"phi": [..], "sigma": 1.0}
      ma    : {"theta": [..], "sigma": 1.0}
      arma  : {"phi": [..], "theta": [..], "sigma": 1.0}
      arima : {"phi": [..], "theta": [..], "d": 1, "sigma": 1.0}
      arch  : {"omega": .., "alpha": [..]}
      garch : {"omega": .., "alpha": [..], "beta": [..]}
    """
    if model not in MODELS:
        raise ValueError(f"modèle inconnu : {model}")
    rng = np.random.default_rng(seed)
    n = T + burn
    z = _innov(rng, n, dist)

    if model in ("arch", "garch"):
        return _simulate_garch(params, z, burn)

    sigma = params.get("sigma", 1.0)
    eps = sigma * z
    phi = np.atleast_1d(params.get("phi", []))
    theta = np.atleast_1d(params.get("theta", []))
    p, q = len(phi), len(theta)

    x = np.zeros(n)
    for t in range(n):
        ar_part = sum(phi[i] * x[t - 1 - i] for i in range(p) if t - 1 - i >= 0)
        ma_part = sum(theta[j] * eps[t - 1 - j] for j in range(q) if t - 1 - j >= 0)
        x[t] = ar_part + ma_part + eps[t]

    x = x[burn:]
    if model == "arima":
        for _ in range(params.get("d", 1)):
            x = np.cumsum(x)
    return x


def _simulate_garch(params, z, burn):
    omega = params["omega"]
    alpha = np.atleast_1d(params["alpha"])
    beta = np.atleast_1d(params.get("beta", []))
    q, p = len(alpha), len(beta)
    n = len(z)
    uncond = omega / (1 - alpha.sum() - beta.sum())
    r = np.zeros(n)
    h = np.full(n, uncond)
    for t in range(n):
        s = omega
        s += sum(alpha[i] * r[t - 1 - i] ** 2 for i in range(q) if t - 1 - i >= 0)
        s += sum(beta[j] * h[t - 1 - j] for j in range(p) if t - 1 - j >= 0)
        h[t] = s
        r[t] = np.sqrt(h[t]) * z[t]
    return r[burn:]
