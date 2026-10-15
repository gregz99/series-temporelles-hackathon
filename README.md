# simts : validation de modèles de séries temporelles par simulation

Hackathon ENSIIE 2027 (sujet proposé par Abass Sagna).

## Question
Combien d'observations faut-il pour que l'estimation d'un modèle de séries
temporelles soit fiable, et dans quels cas (paramètres limites) un logiciel
nous donne-t-il des résultats trompeurs ?

## Démarche (celle de la consigne)
1. Choisir un modèle : AR(1/2), MA(1/2), ARIMA(1,1), ARCH(1), GARCH(1,1)
2. Simuler T observations, avec T petit puis T grand
3. Estimer sur les T-5 premières valeurs, comparer aux vrais paramètres
4. Vérifier ACF / PACF, tester les résidus
5. Prévoir les 5 valeurs suivantes, tracer trajectoire + prévisions
6. Commenter
7. Au-dessus de la consigne : répéter N fois (Monte Carlo) pour trouver le T minimal

## Structure et raison d'être
| Fichier | Rôle | Pourquoi |
|---|---|---|
| `simts/generate.py` | `simulate(modèle, params, T, seed)` | vérité connue, reproductible |
| `simts/scenarios.py` | cas « sage » et « limite » par modèle | exigé par la consigne |
| `simts/fit.py` | estimation sur T-5 valeurs | comparer estimé et vrai |
| `simts/diagnose.py` | ACF/PACF, Ljung-Box | le modèle est-il bien spécifié ? |
| `simts/forecast.py` | prévision 5 pas, RMSE | validation hors échantillon |
| `simts/experiment.py` | Monte Carlo sur une grille de T | un tirage ne prouve rien |
| `simts/plots.py` | trajectoire+prévision, convergence | livrable de la consigne |
| `run_demo.py` | un scénario de bout en bout | point d'entrée |

## Utilisation
```
pip install numpy pandas scipy statsmodels arch matplotlib
python run_demo.py ar1 sage
python run_demo.py ar1 limite
python run_demo.py garch11 sage
```
Les sorties (PNG, CSV) vont dans `outputs/`.

## Reste à faire
- Données réelles (une série par famille de modèle, à choisir)
- Mauvaise spécification : simuler A, estimer B
- Bruit non gaussien (Student), déjà prévu dans `simulate(..., dist="t")`
