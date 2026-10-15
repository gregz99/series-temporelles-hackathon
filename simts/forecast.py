"""Prévision des 5 périodes suivantes et comparaison aux vraies valeurs.

Pourquoi : la consigne demande de prédire les 5 dernières valeurs mises de
côté et de les tracer avec la trajectoire. Pour un (G)ARCH la moyenne est
nulle : ce qui se prévoit, c'est la variance.
"""
import numpy as np


def predict(res, model, h=5):
    """Renvoie un dict : mean (h,), et var (h,) pour les modèles ARCH/GARCH."""
    if model in ("arch", "garch"):
        f = res.forecast(horizon=h, reindex=False)
        return {
            "mean": np.asarray(f.mean.iloc[-1]),
            "var": np.asarray(f.variance.iloc[-1]),
        }
    fc = res.get_forecast(steps=h)
    ci = np.asarray(fc.conf_int(alpha=0.05))
    return {"mean": np.asarray(fc.predicted_mean), "ci": ci}


def rmse(y_true, y_pred):
    return float(np.sqrt(np.mean((np.asarray(y_true) - np.asarray(y_pred)) ** 2)))
