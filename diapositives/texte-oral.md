# Texte de l'oral (10 minutes), par personne

Texte parlé, diapositive par diapositive. Une idée et un chiffre par diapositive ;
ne pas lire, regarder le jury. Version plus détaillée : `notes.md`. Minutage, questions
du jury : `../ORAL.md`.

## Personne A : diapositives 1 à 4 (environ 3 min 30)

**1. Titre (20 s)**
« Bonjour, nous sommes Grégoire, Rassim et Yassine. Notre question : que deviennent les modèles de séries temporelles quand quelque chose d'anormal arrive dans les données ? »

**2. Sujet et extension (1 min)**
« Le sujet demande de simuler un modèle à petite et grande taille, avec un cas où il va bien et un cas limite où il va moins bien, puis de trouver combien d'observations il faut. Nous l'avons fait. Nous avons ajouté une idée : un cas limite *dont on connaît la cause*, une anomalie. On sait ce qu'on injecte, où, et de quelle taille. C'est ce qui arrive dans la vraie vie : une crise, un changement de régime, une erreur de saisie. »

**3. Méthode (1 min)**
« Trois étapes. On fabrique une série dont on connaît la formule, donc la bonne réponse. On estime le modèle avec les logiciels habituels, en gardant les 5 derniers points pour tester. Puis on compare à la vérité. Une seule simulation ne prouve rien, donc on répète 1000 fois sans anomalie, 500 fois avec. Six modèles, quatre anomalies : une valeur aberrante, un saut de niveau durable, un changement de volatilité, et des chocs extrêmes fréquents. »

**4. Sans anomalie (1 min 15)**
« D'abord sans anomalie : combien d'observations faut-il pour que l'erreur sur un paramètre passe sous 25 % ? Une cinquantaine pour un AR(1), quelques centaines pour un AR(2), un ARIMA ou un ARCH, et de 1000 à 2000 pour estimer le paramètre alpha d'un GARCH. Un cas limite n'est pas toujours le plus difficile. Mais un ARIMA dont les deux racines se compensent presque demande 2000 points. »

## Personne B : diapositives 5 à 7 (environ 3 min 15)

**5. Chaque anomalie casse un modèle (1 min 15)**
« Voici le résultat central, avec trois mesures. À gauche, la *couverture* : un intervalle annoncé à 95 % doit contenir la vraie valeur 95 fois sur 100. C'est comme un météorologue qui annonce 70 % de pluie : il doit avoir raison 7 fois sur 10. Vert veut dire que c'est le cas, rouge que non. Au milieu, l'erreur par rapport au cas sans anomalie : 1 veut dire aucun effet. À droite, la prévision à 5 pas. Ce qu'on voit : aucune anomalie ne casse tous les modèles, et aucun modèle ne résiste à toutes les anomalies. »

**6. Deux résultats (1 min)**
« Premier résultat : un saut de niveau. Dans un AR(1), l'estimation est biaisée de plus 0,41, et l'intervalle annoncé ne contient la vraie valeur que 0 fois sur 100. Mais l'ARIMA, qui différencie la série, n'est pas touché. Deuxième résultat : des chocs extrêmes fréquents. Le GARCH se trompe presque 5 fois plus sur alpha, car il confond ces chocs avec des changements de variance. »

**7. Le Brent (1 min)**
« Passons au réel : le prix du Brent de 2010 à 2026, qui traverse trois épisodes d'anomalie : le krach de 2014 à 2016, 2020, et 2026. Le 21 avril 2020, le prix perd 64 % en une journée. Si on retire les 5 plus gros jours de 2020 d'une fenêtre de 1000 jours, l'écart-type passe de 3,98 à 2,78. Cinq jours sur mille suffisent à gonfler l'écart-type de 43 %. C'est une vraie valeur aberrante. »

## Personne C : diapositives 8 à 10 (environ 2 min 40)

**8. Variance constante contre GARCH (1 min)**
« On fait une prévision glissante : on estime sur les 1000 derniers jours, on prévoit, on regarde si la valeur réelle est dans l'intervalle, puis on avance de 5 jours. En rouge, le modèle à variance constante s'effondre à chaque épisode, jusqu'à 0,68 en 2026, puis il est trop prudent entre les crises. En bleu, le GARCH recalcule sa variance chaque jour : il reste proche de 95 %, 0,84 à 0,87 en 2026, sauf au tout début des crises. Aucun modèle n'attrape le jour à moins 64 %. »

**9. TimesFM (50 s)**
« En ouverture, TimesFM 3.0, un modèle de Google d'août 2026, que nous utilisons sans l'entraîner. Il ne donne que des déciles, donc nous comparons tout à 80 % : couverture de 0,803 pour TimesFM, 0,798 pour le GARCH Student, 0,852 pour la variance constante. Il est indiscernable du GARCH et meilleur que la variance constante. Limites : pas d'intervalle à 95 %, et son préentraînement a pu inclure des données de pétrole. »

**10. Conclusion (50 s)**
« Trois messages. Un : chaque anomalie casse un modèle précis et en épargne un autre. Deux : le logiciel affiche la même précision avec ou sans anomalie, l'intervalle d'un AR peut couvrir 0 %. Trois : sur le pétrole, une variance qui évolue, GARCH ou TimesFM, corrige l'essentiel. Nos limites : les tailles d'anomalies sont nos choix, quatre modèles sur six, un seul actif. Merci, nous sommes prêts pour vos questions. »

## Si on demande « pourquoi 95 % ? » (diapositive 11)
« C'est une convention : le logiciel calcule l'estimation plus ou moins 1,96 fois l'erreur standard. Cette formule suppose assez de données et un modèle bien spécifié. Nous mesurons ce qui se passe quand ce n'est plus vrai. »
