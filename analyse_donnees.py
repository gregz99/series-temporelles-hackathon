"""Premier regard sur Brent et WTI (FRED, quotidien, depuis 2010).

Objectif : savoir quels modèles la série justifie *avant* de les lui imposer.
  - racine unitaire sur le niveau   -> ARIMA avec d=1 ?
  - ACF / Ljung-Box des rendements  -> AR / MA ont-ils quelque chose à saisir ?
  - ARCH-LM, Ljung-Box des carrés   -> volatilité en grappes (ARCH/GARCH) ?
  - Engle-Granger Brent / WTI       -> cointégration (VECM) ?
"""
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
from statsmodels.stats.diagnostic import acorr_ljungbox, het_arch
from statsmodels.tsa.stattools import acf, adfuller, coint, pacf

warnings.simplefilter("ignore")
RAW = Path(__file__).parent / "data" / "raw"
START = "2010-01-01"


def load(sid, name):
    s = pd.read_csv(RAW / f"{sid}.csv", na_values=".", parse_dates=[0], index_col=0)
    return s.iloc[:, 0].rename(name)


df = pd.concat([load("DCOILBRENTEU", "brent"), load("DCOILWTICO", "wti")], axis=1)
df = df.loc[START:].dropna()
print(f"Période : {df.index[0].date()} -> {df.index[-1].date()}  ({len(df)} jours communs)")
print(df.describe().round(1).loc[["min", "max", "mean"]].to_string())
print("Jours WTI <= 0 :", int((df.wti <= 0).sum()),
      "->", [str(d.date()) for d in df.index[df.wti <= 0]])

# Rendements logarithmiques, en excluant les prix <= 0 (log impossible)
pos = df[(df > 0).all(axis=1)]
ret = 100 * np.log(pos).diff().dropna()
print(f"\nRendements : {len(ret)} obs, "
      f"{len(df) - len(pos)} jours exclus pour prix <= 0")
big = ret.abs().max()
print("Plus gros rendement absolu (%) :", big.round(1).to_dict())

print("\n=== 1. Racine unitaire (ADF, H0 = racine unitaire)")
for name in ("brent", "wti"):
    lvl = np.log(pos[name])
    p_l = adfuller(lvl, regression="c", autolag="AIC")[1]
    p_r = adfuller(ret[name], regression="c", autolag="AIC")[1]
    print(f"{name:6s} log-niveau p={p_l:.3f}   rendement p={p_r:.4f}")

print("\n=== 2. Mémoire des rendements (ACF/PACF, Ljung-Box lag 10)")
for name in ("brent", "wti"):
    r = ret[name]
    a = acf(r, nlags=5, fft=True)[1:]
    pa = pacf(r, nlags=5)[1:]
    lb = acorr_ljungbox(r, lags=[10], return_df=True)["lb_pvalue"].iloc[0]
    band = 1.96 / np.sqrt(len(r))
    print(f"{name:6s} ACF1-5={np.round(a, 3)}  PACF1-2={np.round(pa[:2], 3)}  "
          f"LB p={lb:.4f}  (bande ±{band:.3f})")

print("\n=== 3. Volatilité en grappes (H0 = pas d'effet ARCH)")
for name in ("brent", "wti"):
    r = ret[name]
    lm_p = het_arch(r, nlags=10)[1]
    lb2 = acorr_ljungbox(r**2, lags=[10], return_df=True)["lb_pvalue"].iloc[0]
    kurt = float(pd.Series(r).kurt() + 3)
    print(f"{name:6s} ARCH-LM p={lm_p:.2e}   LB(carrés) p={lb2:.2e}   kurtosis={kurt:.1f} (normal = 3)")

print("\n=== 4. Cointégration Brent / WTI (Engle-Granger, H0 = pas de cointégration)")
t, p, _ = coint(np.log(pos["brent"]), np.log(pos["wti"]))
print(f"stat={t:.2f}  p={p:.4f}")
spread = pos["brent"] - pos["wti"]
print("Écart Brent - WTI ($) :", spread.describe().round(1)[["min", "mean", "max"]].to_dict())

print("\n=== 5. Régimes : volatilité annuelle des rendements Brent (%, par année)")
yearly = ret["brent"].groupby(ret.index.year).std() * np.sqrt(252)
print(yearly.round(0).astype(int).to_string())

out = Path(__file__).parent / "data"
ret.to_csv(out / "rendements_brent_wti.csv")
pos.to_csv(out / "prix_brent_wti.csv")
