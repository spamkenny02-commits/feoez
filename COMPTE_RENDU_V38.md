# V38 — Mont de Glace, ermites et statues de Kingin

89 entrées ajoutées dans lot32_fr.json : 36 dans le bloc 67, 11 dans 68,
12 dans 73 et 30 dans 80. 88 textes modifiés et une suite de grognements
conservée. Total : 3 376 entrées. Les 3 287 entrées antérieures et les
32 occurrences de démarrage/naissance/horloge sont conservées.

Le village gelé puis libéré retrouve les dialogues de ses habitants,
l'auberge à vingt ryo, les remèdes, Hisui, Subaru et l'œuf au palais des Rêves.
L'énigme conserve les 25 pas au sud. Les quatre ermites restent placés au
cap nord-ouest, dans la caverne au nord, au cap sud-est et au village de
l'Ombre du Feu.

Les ermites du Vent, de la Vue et du Jet expliquent leurs parchemins.
Quatre types de fusion, deux exemplaires de chaque et seize combinaisons
sont conservés. Vent-Eau et Eau-Vent restent distincts. La sélection d'une
cible ou du groupe conserve les commandes haut/bas. Les noms de techniques
restent provisoires avant traduction des menus.

Kingin se cache parmi les statues d'or. Sa boisson donne à la chair
l'apparence de l'or : elle ne la transforme pas littéralement en métal. Le jeu argent/or, les déguisements,
Sherlock, Arsène, Kogorou, Miho et la résurrection annoncée sont préservés.
Le byte AA d'Arsène est conservé dans la chaîne source sous sa notation
hexadécimale ; c'est un glyphe, pas un nouvel effet pris en charge.
B080-S021 reste intact : sa commande 0A demande un traitement dédié.
Les autres messages différés restent identiques à la source.

## Vérification et limites

Le menu B073-S004 conserve ses deux colonnes à un pixel au plus de leur
position anglaise. Le cœur B067-S015 garde la séquence 09/6E/08 ; aucune
routine d'effet n'est modifiée. Les balises et répétitions sont conservées.
Les phrases longues ont été regroupées avant essais pour limiter les fins
isolées sans supprimer les indications du texte.

Les tests ciblés redirigent une demande vers la chaîne voulue avec les
routines natives. Ils vérifient rendu, pagination et terminateur exact,
pas les événements, achats, soins, effets des fusions, combats, récompenses
ou conditions d'apparition des répliques en progression naturelle.
Le fond vient du banc de test. Les captures intermédiaires de pause peuvent
répéter un texte partiel ; les sauts de ligne finaux restent présents.

Noyau Snes9x 1.63. Snes9x 1.60, matériel réel, conditions d'échec des analyses
et toutes les limites du calendrier ne sont pas testés. Les preuves détaillées
de naissance restent celles de V35. Les essais V38 utilisent final, la
référence V37 est reconstruite avec le tag reference38.

Appliquer Tengai_Makyou_Zero_FR_V38.ips à la ROM anglaise originale,
sans cumuler les patches. Les rapports sont liés à la ROM par SHA-256.

Résultats finaux : 4 191 lectures natives, 16 contrôles de police et
14 contrôles de placement réussis. 89 cas ciblés complets, 151 captures
relues. Les 85 captures fixes communes du début et les trois écrans de
navigation sont identiques à V37. 80 lectures des entrées différées
(60 messages uniques) préservent les bytes anglais. 132 blocs sur place,
34 relocalisés, 77 312 octets libres. Les 3 287 entrées antérieures
sont conservées.
