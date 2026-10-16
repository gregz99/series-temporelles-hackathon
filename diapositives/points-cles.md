# Points clés par diapositive (à dérouler avec ses propres mots)

**Fil conducteur** : une question → une méthode → la preuve en laboratoire → la preuve dans le réel → la leçon.
Chaque diapositive : **une idée, un chiffre**. Texte rédigé facultatif : `texte-oral.md`.

**La phrase à avoir en tête :** un modèle donne un résultat propre même quand les données contiennent un accident, et il ne prévient pas ; il faut savoir quel accident casse quel modèle.

## 1. Titre
- La question : que deviennent les modèles quand une anomalie survient ?
- Plan en trois temps : méthode, laboratoire (simulation), réel (Brent)

## 2. Sujet et extension
- Ce que demande le sujet : simuler, cas sage et cas limite, nombre minimal d'observations
- Notre ajout : un cas limite **dont on connaît la cause**
- Pourquoi réaliste : crise, changement de régime, erreur de saisie

## 3. Méthode
- Simuler (on connaît la bonne réponse), estimer, comparer
- 6 modèles, 4 anomalies
- Répéter : un tirage ne prouve rien. **1000 et 500 répétitions**

## 4. Sans anomalie
- Critère : erreur sur le paramètre sous 25 %
- Échelle : **de 50 observations à 2000**
- Surprise : un cas limite n'est pas toujours le plus dur ; le pire = racines qui se compensent (ARIMA)

## 5. Cartes de chaleur
- Lecture : 3 panneaux, vert = tient, rouge = casse, 1 = rien ne change
- Couverture, avec la météo : « 70 % de pluie » doit être juste 7 fois sur 10
- Conclusion : **aucun modèle ne résiste à tout**

## 6. Deux résultats
- Saut de niveau : AR **+0,41 de biais, couverture 0 %** ; ARIMA ×1,01 → différencier
- Chocs extrêmes : GARCH **×4,95** sur α → il confond chocs et changement de variance

## 7. Le Brent
- Trois épisodes réels : 2014-2016, 2020, 2026
- 21 avril 2020 : **−64 % en un jour**
- 5 jours gonflent l'écart-type de **43 %** : vraie valeur aberrante

## 8. Variance constante contre GARCH
- Principe : estimer, prévoir, vérifier, avancer de 5 jours
- Rouge (variance constante) : s'effondre à chaque crise, **0,68 en 2026**, puis trop prudent
- Bleu (GARCH) : proche de 95 %, **0,84 à 0,87 en 2026**, retard au début des crises
- Personne n'attrape le jour à −64 %

## 9. TimesFM
- Modèle de Google, août 2026, **sans entraînement**
- 80 % car il ne donne que des déciles
- **0,803 contre 0,798** (GARCH) : équivalent ; meilleur que la variance constante
- Limites : pas d'IC à 95 %, a pu voir du pétrole

## 10. Conclusion
- Chaque anomalie casse un modèle précis
- Le logiciel affiche la même précision avec ou sans anomalie
- Sur le pétrole : une variance qui évolue
- Limites : tailles choisies par nous, 4 modèles sur 6, un seul actif

## 11. Annexe (si question sur le 95 %)
- Convention ; formule estimation ± 1,96 × erreur standard
- Suppose T grand, modèle bien spécifié, variance constante

## Gérer le temps
- Raccourcir : 1, 2, 3. Ne pas sacrifier : 4 à 6 (le cœur du sujet).
