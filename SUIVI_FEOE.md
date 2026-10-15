# Reprise du chantier FEOE

Le README et le HEAD de main font foi. V26 intègre 2 087 entrées, dont 102
nouvelles (97 textes modifiés et cinq réponses neutres). Sources : lot21_fr.json
et build_v26.py, en complément des lots antérieurs et corrections_v20.json.
Les six corrections de pagination concernent B177-S005/S025,
B178-S025/S031/S035 et B179-S015. Les 1 985 entrées de V25 sont inchangées.

## Ressources locales

La copie de travail peut être retrouvée sous feoez_work dans l'espace de travail.
La ROM anglaise épinglée est dans ../upload/Tengai Makyou Zero.sfc ; son SHA-256
est documenté dans le README. Le matériel de test local est sous ../emulator :
snes9x_libretro_standard.so, snes9x_libretro_diagnostic.so et runs/.
Ces ressources ne sont pas publiées dans le dépôt. Vérifier leur disponibilité
avant de promettre une reconstruction ou un essai ; ne jamais inventer un résultat.

## Prochain lot

Inspecter les blocs 183 et suivants, puis les éventuels blocs antérieurs non
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
  jusqu'au résultat COMPLETE / ALL OK (scenario_checks_v26.json).
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

Les 18 messages différés et le bloc 132 restent inchangés. Consulter les rapports
pour leurs limites. Faire un compte rendu en français avec commit et tests réalisés.
