# Validation de modèles de séries temporelles par simulation : synthèse des résultats

Hackathon ENSIIE 2027 (sujet d'Abass Sagna). État au 15/10/2026. Les chiffres
viennent des fichiers de `outputs/` et `data/` ; chaque affirmation indique sa
source et ses limites.

## 1. Question
> Un logiciel d'estimation annonce un intervalle à 95 %. Combien de fois dit-il
> vrai, selon la taille de l'échantillon et le régime de volatilité ?

## 2. Démarche
1. **Simulation** (vérité connue) : AR(1), AR(2), MA(1), ARIMA(1,1,1), ARCH(1),
   GARCH(1,1), chacun avec un cas « sage » et un cas « limite ».
2. **Monte Carlo** : 200 répétitions par taille $T \in \{20, \dots, 2000\}$ ;
   biais, RMSE relatif et couverture de l'IC à 95 % des paramètres.
3. **Données réelles** : Brent et WTI quotidiens (FRED, 2010 → oct. 2026).
4. **Prévision glissante** sur Brent (fenêtre de 1000 jours, ré-estimation tous
   les 5 jours, prévisions à 1-5 jours) : AR(1), ARIMA(1,1,1), GARCH(1,1)
   gaussien et Student, TimesFM 3.0 (zéro-shot).

## 3. Simulation : T minimal
Critère : erreur relative ≤ 25 % **et** couverture de l'IC ≥ 90 %, pour ce $T$
et tous les $T$ plus grands de la grille (jusqu'à 2000).

| Modèle | Sage | Limite |
|---|---|---|
| AR(1) | 75 | 20 (ne casse pas) |
| AR(2) | 500 | 300 |
| MA(1) | 300 | 2000 (voir limite 1) |
| ARIMA(1,1,1) | 500 | 2000 |
| ARCH(1) | 500 | 200 |
| GARCH(1,1) | $\beta$ : 750, $\alpha$ : 2000, $\omega$ : jamais | $\beta$ : 500, $\alpha$ : 750, $\omega$ : jamais |

Constats :
- **ARIMA(1,1,1) limite** ($\phi=0.9$, $\theta=-0.85$, racines AR et MA quasi
  identiques) est le pire cas : erreur relative de $\phi$ de 110 % à $T=20$,
  43 % à $T=1000$ ; couverture de 66 à 78 % jusqu'à $T=500$. Les résidus passent
  pourtant Ljung-Box (p = 0.96 sur un tirage à $T=1000$) : le diagnostic
  rassure alors que les paramètres sont faux.
- **GARCH(1,1)** : couverture de $\alpha$ de 66-75 % pour $T$ entre 20 et 150 ;
  solutions au bord ($\hat\alpha=0$, $\hat\beta=1$) à $T=50$.
- **AR** : couverture de 92 à 98 % à toutes les tailles, $T \approx 75$ suffit
  pour AR(1). Le cas limite $\phi=0.98$ n'est pas pire (convergence plus rapide
  près de la racine unité) ; son risque est ailleurs (prévision longue, confusion
  avec une marche aléatoire).

## 4. Données : ce que Brent justifie
Source : FRED `DCOILBRENTEU` et `DCOILWTICO`, 4108 jours communs.

| Question | Résultat | Verdict |
|---|---|---|
| Racine unitaire (ADF, log-niveau) | Brent $p=0.063$, WTI $p=0.032$ | ambigu |
| Mémoire des rendements | ACF(1) = −0.064 (Brent), −0.089 (WTI) | quasi vide |
| Effet ARCH | ARCH-LM $p<10^{-98}$ | écrasant |
| Cointégration Brent/WTI | Engle-Granger $p=0.0007$ | plausible |
| Volatilité annuelle | 18 % (2013), 123 % (2020), 72 % (2026) | régimes |

- Kurtosis de Brent seul : **95** ; **12,8** en retirant les 5 plus gros jours
  (tous entre mars et mai 2020). Le WTI vaut −37 $ le 20/04/2020 et Brent passe de
  17,36 à 9,12 $ le 21/04/2020 (−64 %).

## 5. Prévision glissante sur Brent : IC à 95 % (h = 1)
Couverture réalisée (cible 0.95) :

| Période | $n$ | AR(1) | GARCH gaussien | GARCH Student |
|---|---|---|---|---|
| 2014-2019 | 306 | 0.899 | 0.931 | 0.948 |
| 2020 | 51 | 0.824 | 0.882 | 0.882 |
| 2021-2025 | 253 | 0.996 | 0.964 | 0.968 |
| 2026 | 37 | 0.676 | 0.865 | 0.838 |

Score d'intervalle à 95 % (plus bas = mieux) : 2020, AR(1) 96,4 contre 38,1
(GARCH gaussien) ; 2026, 38,4 contre 28,0.

- La variance constante échoue en **trois épisodes** : 2015-2016, 2020, 2026
  (couverture glissante de 100 jours jusqu'à ≈ 0.64-0.70).
- Entre les crises, elle est **trop large** (couverture ≈ 1.00 en 2021-2025) :
  la fenêtre de 1000 jours « se souvient » du choc.
- GARCH reste dans la zone de bruit sauf aux débuts de crise, où il élargit son
  IC avec un retard de quelques jours.
- Le Student n'améliore pas nettement la couverture par rapport au gaussien.
- Aucun modèle n'attrape le jour du −64 %.

## 6. Ouverture : TimesFM 3.0 (Google Research, août 2026)
Modèle de fondation de 330 M de paramètres, utilisé **sans réglage** (zéro-shot),
mêmes contextes et mêmes cibles. Il ne sort que les déciles : comparaison à 80 %.

| | AR(1) | GARCH gaussien | GARCH Student | TimesFM 3.0 |
|---|---|---|---|---|
| Couverture (cible 0.80) | 0.852 | 0.828 | 0.798 | **0.803** |
| Score d'intervalle | 10.48 | 9.04 | **8.97** | 9.07 |
| Test de Kupiec (p) | < 0.001 | < 0.001 | 0.79 | 0.71 |

Test de Diebold-Mariano sur le score d'intervalle (variance HAC, 5 retards) :
- TimesFM **meilleur que la variance constante**, écart −1,41, $p<0.001$ ;
- TimesFM **indiscernable des GARCH** : écart +0,11 contre GARCH Student,
  $p=0.099$ ; +0,03 contre GARCH gaussien, $p=0.62$ ; robuste en h = 1 seul.
- Prévision ponctuelle : personne ne bat la prévision nulle (RMSE 3,03 ; TimesFM
  3,10). En 2026, l'erreur quadratique de TimesFM est plus grande que celle des
  autres modèles ($p\approx 0.02$-$0.03$, 3 comparaisons corrélées).

## 7. Message du rapport
1. Un IC à 95 % n'est pas une garantie : sa couverture réelle varie de 64 % à
   100 % selon le régime de volatilité et la taille de l'échantillon.
2. Les diagnostics de résidus ne détectent pas la sur-paramétrisation
   (ARIMA limite).
3. Sur le pétrole, une variance dépendante du temps (GARCH) corrige l'essentiel
   du défaut ; un modèle de fondation sans réglage obtient le même résultat à 80 %.
4. Les rendements ne sont pas prévisibles en moyenne : l'enjeu est
   l'incertitude, pas le point central.

## 8. Limites (à dire à l'oral)
1. **Bruit de simulation** : 200 répétitions → couverture à ±0.02 près. Les cas
   proches du seuil (ex. MA(1) limite, 0.87 à $T=1000$ puis 0.90 à $T=2000$)
   basculent par hasard. À passer à 1000 répétitions pour les chiffres cités.
2. **Seuils choisis** (25 %/10 %, couverture 90 %) : arbitraires, à afficher.
3. **Objets différents** : en simulation, l'IC d'un *paramètre* ; en prévision
   glissante, l'IC d'une *observation*. Les deux montrent un IC mal calibré,
   mais l'un ne confirme pas l'autre.
4. **Petits effectifs** : 51 points en 2020, 37 en 2026 (± 3 à 5 points).
5. **Un seul actif**, une fenêtre (1000 j), un pas de ré-estimation (5 j).
6. **TimesFM** : pas d'IC à 95 % (donc pas de test des queues) ; poids
   préentraînés sur un corpus d'un millier de milliards de points réels, la
   contamination par des prix du pétrole ne peut pas être exclue ; licence non
   commerciale.
7. **Tests multiples** : une vingtaine de comparaisons Diebold-Mariano ; un
   résultat isolé à p ≈ 0.03 est indicatif, pas concluant.
8. **Prix 2026** pris tels quels sur FRED, non recoupés avec une autre source.

## 9. Reproduction
```
pip install numpy pandas scipy statsmodels arch matplotlib pefile
pip install "torch==2.6.0" "timesfm[torch]"        # TimesFM : voir note PC
python run_demo.py ar1 limite                       # un scénario (simulation)
python analyse_donnees.py                           # tests sur Brent/WTI
python rolling_brent.py garch_t                     # prévision glissante
python rolling_timesfm.py                           # TimesFM (1,3 Go de poids)
python resume_rolling.py && python compare_timesfm.py && python test_dm.py
python graphiques_rolling.py
```
Note : sur le PC de développement, torch ≥ 2.14 ne charge pas (DLL
`vcruntime140_threads.dll` absente) ; torch 2.6.0 CPU fonctionne.

## 10. Fichiers
- Graphiques : `outputs/brent_couverture_glissante.png`,
  `outputs/brent_ic_vs_rendements.png`, `outputs/*_couverture.png`,
  `outputs/*_convergence.png`
- Tableaux : `data/couverture_rolling.csv`, `data/comparaison_timesfm_80.csv`,
  `data/dm_tests.csv`, `outputs/*_montecarlo.csv`
