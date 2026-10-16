"""Anomalies injectées dans une série simulée.

Pourquoi : la consigne demande des cas où le modèle « se comporte moins bien ».
Une anomalie est une cause concrète, contrôlée et réaliste de ce comportement :
on connaît sa nature, sa taille et sa date, donc on peut mesurer ce qu'elle
coûte à l'estimation et à la prévision.

Types (appliqués au milieu de l'échantillon) :
  ref        aucune anomalie (référence)
  outlier    une valeur aberrante isolée de +8 écarts-types
  niveau     décalage de niveau durable de +3 écarts-types à partir du milieu
  volatilite innovations multipliées par 3 à partir du milieu
  queues     innovations de Student à 3 degrés de liberté (queues épaisses)
"""
import numpy as np

from .generate import simulate

KINDS = ("ref", "outlier", "niveau", "volatilite", "queues")


def _scale(y, model):
    """Écart-type de référence : celui de la série, ou de sa différence
    première pour un modèle intégré."""
    base = np.diff(y) if model == "arima" else y
    return float(np.std(base))


def simulate_with_anomaly(model, params, N, kind, seed):
    """Série de N points avec une anomalie de type `kind` au milieu."""
    mid = N // 2
    if kind == "volatilite":
        vs = np.ones(N)
        vs[mid:] = 3.0
        return simulate(model, params, N, seed=seed, vol_scale=vs)
    if kind == "queues":
        return simulate(model, params, N, seed=seed, dist="t", df=3)

    y = simulate(model, params, N, seed=seed)
    s = _scale(y, model)
    if kind == "outlier":
        y = y.copy()
        y[mid] += 8.0 * s
    elif kind == "niveau":
        y = y.copy()
        y[mid:] += 3.0 * s
    elif kind != "ref":
        raise ValueError(f"anomalie inconnue : {kind}")
    return y
