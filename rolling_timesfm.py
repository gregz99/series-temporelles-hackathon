"""Prévision glissante de Brent avec TimesFM 3.0 (zéro-shot).

Même protocole que rolling_brent.py : mêmes origines (tous les 5 jours depuis
2014), même contexte (les W=1000 derniers rendements), même cible (h=1..5).
TimesFM ne sort que 9 quantiles (déciles 0.1 à 0.9) : on compare donc à
l'IC à 80 % (q0.1, q0.9) et non à 95 %.

Prérequis : pip install --user "timesfm[torch]" (testé avec torch 2.6.0 CPU :
torch 2.14 exige vcruntime140_threads.dll, absent de ce PC).
"""
from pathlib import Path

import numpy as np
import pandas as pd

from rolling_brent import FIRST, H, STEP, W, brent_returns

ROOT = Path(__file__).parent
BATCH = 16


def main():
    import timesfm

    forecaster = timesfm.TimesFM3Forecaster.from_pretrained(
        "google/timesfm-3.0-pytorch", device="cpu")

    r = brent_returns()
    y, idx = r.to_numpy().astype(np.float32), r.index
    start = int(np.searchsorted(idx, pd.Timestamp(FIRST)))
    origins = list(range(max(start, W), len(y) - H, STEP))

    rows = []
    for k in range(0, len(origins), BATCH):
        chunk = origins[k:k + BATCH]
        ctx = [y[i - W:i] for i in chunk]
        outs = list(forecaster.predict_batch(
            ctx, horizon=H, return_quantiles=True, use_symmetric_averaging=False))
        for i, o in zip(chunk, outs):
            f, q = np.asarray(o.forecast), np.asarray(o.quantiles)  # (H,), (H, 9)
            for h in range(H):
                rows.append((idx[i + h], h + 1, float(y[i + h]), f[h],
                             np.nan, np.nan, q[h, 0], q[h, 8]))
        print(f"{min(k + BATCH, len(origins))}/{len(origins)} origines", flush=True)

    out = pd.DataFrame(rows, columns=["date", "h", "y", "mean", "lo", "hi", "lo80", "hi80"])
    out.to_csv(ROOT / "data" / "rolling_timesfm.csv", index=False)
    print("timesfm", len(out), "prévisions")


if __name__ == "__main__":
    main()
