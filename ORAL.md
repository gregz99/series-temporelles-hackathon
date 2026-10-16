# Oral de 10 minutes : fiche de préparation

Diapositives : deck « Soutenance : anomalies et modèles de séries temporelles »
(10 diapositives + 1 annexe de secours, notes d'orateur dans chaque diapositive).
Fil rouge : **« Que deviennent les modèles de séries temporelles quand une
anomalie survient ? »** Chiffres issus de `rapport/rapport.pdf`.

## Minutage (9 min 30, 30 s de marge)

| # | Temps | Diapositive | Message en une phrase |
|---|---|---|---|
| 1 | 0:00-0:20 | Titre | Notre question : que deviennent les modèles quand une anomalie survient ? |
| 2 | 0:20-1:20 | Ce que demande le sujet, ce que nous ajoutons | Une anomalie est un cas limite dont on connaît la cause. |
| 3 | 1:20-2:20 | Méthode | Simuler, estimer, comparer à la vérité ; 6 modèles, 4 anomalies. |
| 4 | 2:20-3:35 | Sans anomalie | De 50 points (AR(1)) à 2000 (α du GARCH). |
| 5 | 3:35-4:50 | Chaque anomalie casse un modèle | Cartes de chaleur : aucun modèle n'est robuste à tout. |
| 6 | 4:50-5:50 | Deux résultats | Décalage de niveau : AR détruit, ARIMA intact. Queues épaisses : GARCH ×5. |
| 7 | 5:50-6:50 | Le Brent | Trois épisodes réels ; 5 jours gonflent l'écart-type de 43 %. |
| 8 | 6:50-7:50 | Variance constante contre GARCH | Elle échoue à chaque épisode (0,68 en 2026 contre 0,84-0,87). |
| 9 | 7:50-8:40 | TimesFM 3.0 | Sans réglage, indiscernable de GARCH à 80 %. |
| 10 | 8:40-9:30 | Ce qu'on retient | 3 messages et 4 limites. |
| 11 | secours | Annexe : d'où vient le 95 % | À montrer seulement si on pose la question. |

## Répartition à trois

- **Personne A (Grégoire)** : diapositives **1, 2, 3 puis 10** (3 min 10) : ouvre avec la question, le sujet et la méthode, et **referme** avec la conclusion.
- **Personne B (Rassim ou Yassine, à choisir)** : diapositives **4, 5, 6** (3 min 30) : le cœur, simulation sans anomalie, cartes de chaleur, deux résultats.
- **Personne C (l'autre)** : diapositives **7, 8, 9** (2 min 50) : le réel, Brent, variance constante contre GARCH, TimesFM.

Relais : A → B « voyons d'abord ce que ça donne sans anomalie » ; B → C « voyons si on
le retrouve dans le réel » ; C → A « je laisse conclure ».

Qui répond aux questions : méthode et sujet → A ; simulation → B ; Brent et TimesFM → C.
Chacun doit pouvoir expliquer **toutes** les diapositives : le jury peut interroger n'importe qui.

## Les 5 phrases à savoir par cœur

1. « Une anomalie est un cas limite dont on connaît la cause. »
2. « Aucun modèle n'est robuste à tout : chaque anomalie en casse un et en épargne un autre. »
3. « Un décalage de niveau détruit un AR (couverture 0 %) mais laisse un ARIMA intact. »
4. « Le logiciel affiche la même précision avec ou sans anomalie. »
5. « Sur le pétrole, une variance qui évolue, GARCH ou TimesFM, corrige l'essentiel. »

## Questions probables et réponses courtes

- **Que veut dire « couverture » ?** La fréquence avec laquelle l'intervalle annoncé contient la vraie valeur ; pour un intervalle à 95 %, on attend 95 fois sur 100. (Diapositive d'annexe.)
- **D'où vient le 95 % ?** C'est une convention ; le logiciel calcule estimation ± 1,96 × erreur standard (loi normale). Cela suppose un T assez grand, un paramètre loin des frontières et un modèle bien spécifié.
- **Pourquoi ces anomalies et ces tailles ?** Ce sont nos choix (+8 σ, +3 σ, ×3, Student à 3 degrés), faits pour provoquer un effet net ; nous n'avons pas fait varier l'amplitude. C'est une limite.
- **Pourquoi le décalage de niveau détruit-il l'AR ?** Le saut rend la série très persistante, donc φ estimé monte vers 0,9 (biais +0,41). L'ARIMA différencie la série : le saut devient un point isolé.
- **Pourquoi le GARCH souffre-t-il des queues épaisses ?** Il confond des valeurs extrêmes fréquentes avec des changements de variance : α est estimé près de 5 fois moins bien.
- **Pourquoi le Brent ?** Quotidien depuis 2010, crises marquées (2014-2016, 2020, 2026), volatilité en grappes (test ARCH, p < 10⁻⁹⁸).
- **Pourquoi 25 % comme seuil ?** C'est notre choix. Avec 10 %, l'ARIMA et le GARCH n'atteignent presque jamais le critère jusqu'à T = 2000. Les courbes complètes sont dans le rapport.
- **Pourquoi seulement 4 modèles avec anomalies ?** Un choix de temps : AR(1), MA(1), ARIMA et GARCH couvrent les familles ; AR(2) et ARCH(1) ne sont pas testés avec anomalies.
- **TimesFM est-il meilleur que GARCH ?** Non : indiscernable à 80 % (p = 0,10). Il est meilleur que la variance constante.
- **TimesFM a-t-il « vu » ces données ?** On ne peut pas l'exclure : préentraînement sur plus de 1000 milliards de points réels.
- **Pourquoi 80 % pour TimesFM ?** Il ne donne que les déciles, pas d'intervalle à 95 %.
- **La simulation prouve-t-elle ce qu'on voit sur le Brent ?** Non : en simulation on mesure l'intervalle d'un paramètre, sur le Brent celui d'une observation. Les deux montrent un défaut, mais l'un ne confirme pas l'autre.
- **Qu'auriez-vous fait avec plus de temps ?** Varier l'amplitude des anomalies, tester AR(2) et ARCH(1), essayer des méthodes robustes (indicatrices, innovations de Student), d'autres actifs.

## Ce qu'il ne faut pas dire

- « TimesFM est meilleur que GARCH » (non démontré).
- « Les intervalles de confiance sont faux » (nous disons : le chiffre affiché ne suffit pas).
- « Les remèdes marchent » : nous n'avons testé que la différenciation et la variance dépendante du temps.
- « Les anomalies sont réalistes en taille » : ce sont des tailles choisies.

## À répéter

- Chronométrer à voix haute, deux fois, avec les diapositives.
- Une seule phrase d'accroche par diapositive ; ne pas lire les notes mot à mot.
- Avoir `rapport/rapport.pdf` ouvert pour vérifier un chiffre.
