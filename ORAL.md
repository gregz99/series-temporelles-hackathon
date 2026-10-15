# Oral : 5 minutes, 6 diapositives

Fil rouge : **« Un IC à 95 % dit-il vrai ? »** Chaque diapositive répond à une
question que la précédente a ouverte. Chiffres issus de `RESULTATS.md`.

| # | Temps | Titre | Message | Visuel |
|---|---|---|---|---|
| 1 | 0:30 | Un IC à 95 %, ça vaut quoi ? | Les logiciels annoncent 95 %. Combien de fois c'est vrai, selon $T$ et la volatilité ? | une phrase, un chiffre : « de 64 % à 100 % » |
| 2 | 1:00 | Méthode | On simule (vérité connue) 6 modèles, cas sage et cas limite, 1000 répétitions par taille de 20 à 2000 ; on mesure la couverture de l'IC | schéma 3 cases : simuler → estimer → compter |
| 3 | 1:00 | Ce que la simulation révèle | ARIMA limite : couverture 70-79 % jusqu'à $T=500$, alors que les résidus passent Ljung-Box. GARCH sage : 63-78 % pour $T\le150$. AR : 94-96 % partout, $T\approx50$ | `outputs/arima11_limite_n1000_couverture.png` |
| 4 | 1:00 | Le même défaut sur Brent | Prévision glissante 2014-2026 : la variance constante tombe à 0.68 en 2026 et monte à 0.996 en 2021-2025 (trop large) ; GARCH reste proche de 95 % sauf au début des crises | `outputs/brent_couverture_glissante.png` |
| 5 | 0:45 | Ouverture : TimesFM 3.0 | Modèle de fondation de Google (août 2026), zéro-shot : couverture 0.803 à 80 %, indiscernable de GARCH Student (0.798, $p=0.10$), meilleur que la variance constante ($p<0.001$) | tableau 4 lignes + « pas d'IC à 95 % » |
| 6 | 0:45 | Conclusion et limites | 4 messages (ci-dessous) ; limites : un seul actif, 51 points en 2020 et 37 en 2026, contamination possible du préentraînement | liste de 4 messages + 3 limites |

## Les 4 messages (diapositive 6)
1. Un IC à 95 % n'est pas une garantie : sa couverture réelle dépend du régime.
2. Les diagnostics de résidus ne voient pas la sur-paramétrisation.
3. Sur le pétrole, GARCH corrige l'essentiel ; un modèle de fondation sans
   réglage fait aussi bien à 80 %.
4. Les rendements ne sont pas prévisibles en moyenne : l'enjeu est l'incertitude.

## Répartition possible à plusieurs
- Diapos 1-3 : simulation et méthode (1 personne)
- Diapos 4-5 : données Brent et TimesFM (1 personne)
- Diapo 6 + questions : synthèse (1 personne)

## Questions probables du jury et réponses
- **Pourquoi Brent ?** Quotidien depuis 2010, crises marquées (2014-16, 2020,
  2026), cointégration avec WTI, volatilité en grappes (ARCH-LM $p<10^{-98}$).
- **Pourquoi ces seuils (25 %, 90 %) ?** Choisis par nous ; on montre les
  courbes complètes, le seuil ne sert qu'à résumer.
- **Pourquoi pas TimesFM à 95 % ?** Il ne sort que les déciles ; donc test à 80 %
  pour tous.
- **TimesFM a-t-il vu ces données ?** On ne peut pas l'exclure (corpus de plus
  de 1000 milliards de points réels).
- **Est-ce significatif ?** Diebold-Mariano avec variance HAC ; plusieurs
  comparaisons, donc un résultat isolé à $p\approx0.03$ est indicatif.
- **Le creux de MA(1) limite ?** Effet réel (91 %, 88 %, 90 % à $T$=750, 1000,
  2000) ; nous l'attribuons à la frontière d'inversibilité mais ne l'avons pas
  testé.

## À répéter avant
- Chronométrer : 5 minutes pile, une phrase d'accroche par diapo.
- Avoir `RESULTATS.md` sous la main pour les chiffres.

---

# Questions à poser à Abass Sagna

À envoyer par mail (je n'envoie rien sans ton accord) :

1. **Format du rendu** : rapport, notebook, diaporama, ou plusieurs ? Langue et
   longueur attendues ?
2. **Dates** : échéance de rendu, date et durée de la présentation du hackathon.
3. **Taille des équipes** : le mail est parti à 5 personnes alors que le sujet
   indique 3 ; devons-nous nous répartir en équipes de 3 ?
4. **Périmètre** : la consigne demande un modèle ; avons-nous le droit d'en
   couvrir six (AR, MA, ARIMA, ARCH, GARCH) et de comparer ?
5. **Données** : le sujet parle de simulation ; une application sur données réelles
   en complément (Brent, FRED) est-elle bienvenue ?
6. **Découpage test** : les 5 dernières valeurs sont-elles fixes, ou pouvons-nous
   faire une prévision glissante ?
7. **Outils** : Python imposé ou libre ? L'usage d'un modèle de fondation
   (TimesFM 3.0, licence non commerciale) en ouverture est-il accepté ?
8. **Critères de notation** : poids de la simulation, de l'interprétation, du
   code, de la présentation.
9. **Code** : dépôt GitHub à fournir ? Partage de code avec les autres groupes
   autorisé ?
10. **Soutenance** : démonstration en direct attendue, ou seulement les
    résultats ?
