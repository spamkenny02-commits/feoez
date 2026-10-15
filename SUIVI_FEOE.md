# Reprise du chantier FEOE

Le README et le HEAD de main font foi. V28 intègre 2 365 entrées, dont 176
nouvelles (161 textes modifiés, douze entrées vides et trois réponses neutres).
Sources : lot23_fr.json et build_v28.py, en complément des lots antérieurs.
Les blocs 197/198/199/200 et 203/204 sont partagés. Les 2 189 entrées de V27
sont inchangées. Le constructeur conserve corrections_v20.json.

## Ressources locales

La copie de travail peut être retrouvée sous feoez_work dans l'espace de travail.
La ROM anglaise épinglée est dans ../upload/Tengai Makyou Zero.sfc ; son SHA-256
est documenté dans le README. Le matériel de test local est sous ../emulator :
snes9x_libretro_standard.so, snes9x_libretro_diagnostic.so et runs/.
Ces ressources ne sont pas publiées dans le dépôt. Vérifier leur disponibilité
avant de promettre une reconstruction ou un essai ; ne jamais inventer un résultat.

## Prochain lot

Inspecter les blocs 206 et suivants, puis les éventuels blocs antérieurs non
traités. La liste BLOCKS du dernier constructeur donne la couverture canonique ;
un numéro inférieur au dernier bloc traité n'implique pas une traduction.
Viser un lot cohérent de 100 à 200 entrées. Préserver la séquence de toutes les
balises, les variantes, les conditions, les prix et les attributions des répliques.
Conserver corrections_v20.json et tous les cas particuliers de mise en page.

## Validation et publication

- Reconstruire depuis la ROM anglaise originale avec le nouveau constructeur.
- Vérifier les routines natives 65816, les alias, l'IPS, le checksum, les largeurs,
  la police et le placement ; comparer les traductions antérieures sans les altérer.
- Rejouer le scénario standard avec la ROM exacte ; remplacer tous les chemins
  d'états par ceux de ce nouveau parcours. Initialiser A, reset, puis tester B
  jusqu'au résultat COMPLETE / ALL OK (scenario_checks_v28.json).
- Créer un état dialogue_entry avec cette même ROM. Utiliser les scripts de
  verification/reproduction et des cas propres au nouveau lot ; exiger le
  terminateur exact, relire les pages et corriger les fins de page isolées.
- Toute correction de ROM impose de produire des preuves liées à la ROM finale.
  Les essais ciblés redirigent un dialogue : ils ne prouvent pas les combats,
  les récompenses, le calendrier ou la progression naturelle.
- Publier sur main les sources, l'IPS, le glossaire et les preuves compactes,
  jamais la ROM, les états, le noyau binaire ou les milliers de captures brutes.
- Relire le HEAD distant avant d'écrire. En cas de travail concurrent, ne pas
  dupliquer ni écraser ; publier avec contrôle du parent attendu, sans force.

Les 39 messages différés et le bloc 132 restent inchangés. Consulter les rapports
pour leurs limites. Faire un compte rendu en français avec commit et tests réalisés.

V27 laisse le bloc 183 (35 invites de débogage) intact. Les nouveaux messages
différés sont B184-S008/S010 (alias 185), B186-S015 et B189-S001/S002.
La CLI git ne dispose pas d’identifiants de push. La connexion GitHub permet
de publier par blobs, arbre, commit puis update_ref avec le parent attendu.
Comparer le SHA d’arbre distant à celui du commit local testé.

V28 : B205-S048 a été raccourci après relecture (fin de page « apparais ! »).
Le test de B203-S012 utilise la valeur de substitution héritée du dialogue
de départ, pas un numéro de coffre initialisé. Ne pas prétendre valider le
compteur ou la logique du jeu des coffres par ce rendu redirigé.
