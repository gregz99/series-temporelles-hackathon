"""Diagnostics : ACF/PACF et test sur les résidus.

Pourquoi : un modèle bien spécifié laisse des résidus sans structure, et
l'ACF/PACF de la série doit ressembler à celles du modèle (PACF qui coupe
après p pour un AR, ACF qui coupe après q pour un MA).
"""
import numpy as np
from statsmodels.stats.diagnostic import acorr_ljungbox
from statsmodels.tsa.stattools import acf, pacf


def empirical_acf_pacf(train, nlags=20):
    nlags = min(nlags, len(train) // 2 - 1)
    return acf(train, nlags=nlags, fft=True), pacf(train, nlags=nlags)


def ljung_box(residuals, lags=10, squared=False):
    """p-valeur de Ljung-Box. squared=True teste l'effet ARCH."""
    r = np.asarray(residuals)
    r = r**2 if squared else r
    out = acorr_ljungbox(r, lags=[lags], return_df=True)
    return float(out["lb_pvalue"].iloc[0])
