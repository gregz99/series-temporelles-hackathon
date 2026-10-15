"""Scénarios : un cas « sage » et un cas « limite » par modèle.

Pourquoi : la consigne demande un paramètre où le modèle se comporte bien
et un cas limite où il se comporte moins bien. Le cas limite est choisi près
de la frontière de stationnarité / d'inversibilité, là où l'estimation
devient fragile.
"""

SCENARIOS = {
    "ar1": {
        "model": "ar", "order": (1, 0, 0),
        "sage": {"phi": [0.5], "sigma": 1.0},
        "limite": {"phi": [0.98], "sigma": 1.0},
    },
    "ar2": {
        "model": "ar", "order": (2, 0, 0),
        "sage": {"phi": [0.5, 0.2], "sigma": 1.0},
        "limite": {"phi": [0.7, 0.28], "sigma": 1.0},
    },
    "ma1": {
        "model": "ma", "order": (0, 0, 1),
        "sage": {"theta": [0.5], "sigma": 1.0},
        "limite": {"theta": [0.98], "sigma": 1.0},
    },
    "arima11": {
        "model": "arima", "order": (1, 1, 1),
        "sage": {"phi": [0.5], "theta": [0.3], "d": 1, "sigma": 1.0},
        "limite": {"phi": [0.9], "theta": [-0.85], "d": 1, "sigma": 1.0},
    },
    "arch1": {
        "model": "arch", "order": None,
        "sage": {"omega": 0.2, "alpha": [0.4]},
        "limite": {"omega": 0.2, "alpha": [0.95]},
    },
    "garch11": {
        "model": "garch", "order": None,
        "sage": {"omega": 0.1, "alpha": [0.1], "beta": [0.8]},
        "limite": {"omega": 0.02, "alpha": [0.08], "beta": [0.91]},
    },
}


def get(name, cas):
    """Renvoie (model, order, params) pour un scénario et un cas."""
    s = SCENARIOS[name]
    return s["model"], s["order"], s[cas]
