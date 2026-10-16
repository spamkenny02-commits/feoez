# Reprise du chantier FEOE

Le README et le HEAD de main font foi. V30 intègre 2 601 entrées, dont 38
nouvelles. Sources : lot25_fr.json et build_v30.py, en complément des lots
antérieurs. Les 2 563 entrées de V29 sont inchangées. Le constructeur
conserve corrections_v20.json.

## Ressources locales

La copie de travail peut être retrouvée sous feoez_work dans l'espace de travail.
La ROM anglaise épinglée est dans ../upload/Tengai Makyou Zero.sfc ; son SHA-256
est documenté dans le README. Le matériel de test local est sous ../emulator :
snes9x_libretro_standard.so, snes9x_libretro_diagnostic.so et runs/.
Ces ressources ne sont pas publiées dans le dépôt. Vérifier leur disponibilité
avant de promettre une reconstruction ou un essai ; ne jamais inventer un résultat.

## Prochain lot

Inspecter les blocs 217 et suivants, et reprendre le journal du bloc 210, puis les éventuels blocs antérieurs non
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
  jusqu'aux résultats attendus (A : COMPLETE / ALL OK ; B : les deux BACKUP OK,
  scenario_checks_v30.json).
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

Les 40 messages différés et le bloc 132 restent inchangés. Consulter les rapports
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

V29 ajoute B212-S018 aux messages différés. Les énigmes DOG/GOD utilisent
les mots anglais et leurs sens français, sans changer les portes T/F.
collect_evidence.py regroupe les preuves et produit des planches, mais laisse
la relecture visuelle en attente : les images doivent être inspectées.

Pagination V29 : B206-S001, B208-S013, B209-S025, B211-S005/S010 raccourcis
après relecture ; reconstruire et tester uniquement la ROM finale corrigée.

V30 : petit lot cohérent de 38 entrées, blocs 214-216, tous rendus à l'écran.
B215-S006/S012 et B216-S005 raccourcis après relecture. Les preuves finales
doivent utiliser les parcours corrected, liés à la ROM finale. Le contrôle
A affiche COMPLETE / ALL OK ; B affiche OK pour RTC BACKUP et S-RAM BACKUP.
Ne pas prétendre que B affiche aussi un écran COMPLETE / ALL OK.
