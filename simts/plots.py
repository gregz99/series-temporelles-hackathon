"""Graphiques : le tracé demandé (trajectoire + 5 prévisions) et la
convergence de l'erreur d'estimation en fonction de T."""
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


def plot_trajectory_forecast(y_full, pred_mean, ci=None, title="", path=None):
    """y_full = les T valeurs ; les 5 dernières sont les valeurs test."""
    T, h = len(y_full), len(pred_mean)
    fig, ax = plt.subplots(figsize=(9, 4))
    ax.plot(range(T), y_full, color="#1f4e79", lw=1.2, label="série simulée")
    xs = range(T - h, T)
    ax.plot(xs, pred_mean, "o--", color="#c0392b", label="prévisions (5 pas)")
    if ci is not None:
        ax.fill_between(xs, ci[:, 0], ci[:, 1], color="#c0392b", alpha=0.15,
                        label="IC 95 %")
    ax.axvline(T - h - 0.5, color="grey", ls=":", lw=1)
    ax.set_title(title)
    ax.set_xlabel("t")
    ax.legend()
    fig.tight_layout()
    if path:
        fig.savefig(path, dpi=140)
    plt.close(fig)


def plot_coverage(results, title="", path=None):
    """Couverture empirique de l'IC à 95 % selon T (cible : 0.95)."""
    fig, ax = plt.subplots(figsize=(7, 4))
    for name, g in results.groupby("param"):
        g = g.sort_values("T")
        ax.plot(g["T"], g["couverture"], "o-", label=name)
    ax.axhline(0.95, color="grey", ls="--", lw=1, label="cible 95 %")
    ax.set_xscale("log")
    ax.set_ylim(0, 1.02)
    ax.set_xlabel("T (taille d'apprentissage)")
    ax.set_ylabel("couverture de l'IC à 95 %")
    ax.set_title(title)
    ax.legend()
    fig.tight_layout()
    if path:
        fig.savefig(path, dpi=140)
    plt.close(fig)


def plot_convergence(results, title="", path=None):
    """RMSE de chaque paramètre en fonction de T (échelle log)."""
    fig, ax = plt.subplots(figsize=(7, 4))
    for name, g in results.groupby("param"):
        g = g.sort_values("T")
        ax.plot(g["T"], g["rmse"], "o-", label=name)
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("T (taille d'apprentissage)")
    ax.set_ylabel("RMSE de l'estimateur")
    ax.set_title(title)
    ax.legend()
    fig.tight_layout()
    if path:
        fig.savefig(path, dpi=140)
    plt.close(fig)
