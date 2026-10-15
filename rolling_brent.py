"""Prévision glissante sur les rendements journaliers de Brent.

Pourquoi : mesurer si l'IC à 95 % annoncé par chaque modèle tient dans la
réalité, avant et après 2020. Les paramètres sont inconnus, donc le seul
juge est la valeur réalisée.
Comment : fenêtre glissante de W jours, ré-estimation tous les STEP jours,
prévision des 5 jours suivants (h=1..5). On enregistre la moyenne et l'IC
prévus pour chaque jour cible.

Usage : python rolling_brent.py {ar1|arma11|garch_n|garch_t}
  ar1     : AR(1) avec constante, variance constante
  arma11  : ARMA(1,1) avec constante sur les rendements = ARIMA(1,1,1) avec
            dérive sur le log-prix, variance constante
  garch_n : constante + GARCH(1,1), innovations gaussiennes
  garch_t : constante + GARCH(1,1), innovations Student
"""
import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

warnings.simplefilter("ignore")
ROOT = Path(__file__).parent
W, STEP, H, FIRST = 1000, 5, 5, "2014-01-01"
Z = stats.norm.ppf(0.975)
Z80 = stats.norm.ppf(0.90)  # IC à 80 % : comparable aux déciles de TimesFM


def brent_returns():
    s = pd.read_csv(ROOT / "data/raw/DCOILBRENTEU.csv", na_values=".",
                    parse_dates=[0], index_col=0).iloc[:, 0]
    s = s.loc["2010-01-01":].dropna()
    s = s[s > 0]
    return 100 * np.log(s).diff().dropna()


def forecast_arma(train, order):
    from statsmodels.tsa.arima.model import ARIMA
    res = ARIMA(train, order=order, trend="c").fit()
    fc = res.get_forecast(H)
    m, se = np.asarray(fc.predicted_mean), np.asarray(fc.se_mean)
    return m, m - Z * se, m + Z * se, m - Z80 * se, m + Z80 * se


def forecast_garch(train, dist):
    from arch import arch_model
    res = arch_model(train, mean="Constant", vol="GARCH", p=1, q=1,
                     dist=dist).fit(disp="off")
    f = res.forecast(horizon=H, reindex=False)
    m = np.asarray(f.mean.iloc[-1])
    sd = np.sqrt(np.asarray(f.variance.iloc[-1]))
    if dist == "t":
        nu = [res.params["nu"]]
        q = res.model.distribution.ppf([0.025, 0.975], nu)
        q8 = res.model.distribution.ppf([0.10, 0.90], nu)
        return m, m + q[0] * sd, m + q[1] * sd, m + q8[0] * sd, m + q8[1] * sd
    return m, m - Z * sd, m + Z * sd, m - Z80 * sd, m + Z80 * sd


def main(name):
    r = brent_returns()
    y, idx = r.to_numpy(), r.index
    start = int(np.searchsorted(idx, pd.Timestamp(FIRST)))
    rows = []
    for i in range(max(start, W), len(y) - H, STEP):
        train = y[i - W:i]
        try:
            if name == "ar1":
                m, lo, hi, lo8, hi8 = forecast_arma(train, (1, 0, 0))
            elif name == "arma11":
                m, lo, hi, lo8, hi8 = forecast_arma(train, (1, 0, 1))
            elif name == "garch_n":
                m, lo, hi, lo8, hi8 = forecast_garch(train, "normal")
            else:
                m, lo, hi, lo8, hi8 = forecast_garch(train, "t")
        except Exception:
            continue
        for h in range(H):
            rows.append((idx[i + h], h + 1, y[i + h], m[h], lo[h], hi[h], lo8[h], hi8[h]))
    out = pd.DataFrame(rows, columns=["date", "h", "y", "mean", "lo", "hi", "lo80", "hi80"])
    out.to_csv(ROOT / "data" / f"rolling_{name}.csv", index=False)
    print(name, len(out), "prévisions")


if __name__ == "__main__":
    main(sys.argv[1])
