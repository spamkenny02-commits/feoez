# Reprise du chantier FEOE

Le README et le HEAD de main font foi. V34 intègre 3 160 entrées, dont 123
nouvelles. Sources : lot29_fr.json et build_v34.py en complément des lots
antérieurs. Les 3 037 entrées de V33 sont inchangées. Le constructeur
conserve corrections_v20.json et les mises en page particulières héritées.

## Ressources locales

La copie de travail peut être retrouvée sous feoez_work dans l'espace de travail.
La ROM anglaise épinglée est dans ../upload/Tengai Makyou Zero.sfc ; son SHA-256
est documenté dans le README. Le matériel de test local est sous ../emulator :
snes9x_libretro_standard.so, snes9x_libretro_diagnostic.so et runs/.
Ces ressources ne sont pas publiées dans le dépôt. Vérifier leur disponibilité
avant de promettre une reconstruction ou un essai ; ne jamais inventer un résultat.

## Prochain lot

Reprendre le journal du bloc 210, les blocs 235/236, le menu 244/245 et
le bloc 253, puis les éventuels blocs antérieurs non traités. La liste BLOCKS du dernier constructeur donne la couverture canonique ;
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
  scenario_checks_v33.json).
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

Les messages différés et le bloc 132 restent inchangés. Consulter les rapports
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

V31 : B221-S022 reste différé à cause du fragment littéral x5. Le choix
B217-S013 conserve les colonnes ; le rendu ne prouve pas la sélection
effective des fins. L'ermite du Tonnerre, Foudre et Éclair sont distincts.

La sélection du banc CPU accepte maintenant jusqu'à 500 000 instructions,
car B221-S011 demande 118 082 instructions sur la source anglaise.
verify_long_selection.py vérifie six cas de la ROM originale. Ne pas
confondre ce plafond du banc avec une modification du moteur du jeu.

Pagination V31 : B221-S001/S021/S024/S049, B223-S026 et B224-S008
resserrés après relecture. Les preuves finales utilisent les parcours
corrected et l'état créé avec la ROM finale.

V32 ajoute aux différés B225-S012, B229-S012 et B231-S010/S013/S029/S032.
Le lanceur run_version_checks.py réunit les essais après construction et
refuse les répertoires existants pour éviter de mélanger les preuves.
Exiger le terminateur exact, puis relire toutes les pages sélectionnées.

V33 ajoute B234-S050 aux différés. Les blocs 235/236 ne sont pas traités ;
leurs octets doivent rester identiques à la source. Les articles sont les
affirmations fantaisistes du journal. Les deux menus regroupent trois lignes de choix à
deux colonnes ; newspaper_layout_v33.json documente les largeurs.
La sélection effective d'un article n'est pas validée par un rendu redirigé.

Pagination V33 : B233-S020 et B234-S032/S057 resserrés après relecture.
Les parcours V33 finaux utilisent le tag corrected ; la comparaison avec
V32 utilise son tag final. Recréer les états avec la ROM exacte.

Comparaison V32/V33 : 59/85 captures fixes identiques ; 26 écarts de phase
observés, cause non établie. Ne pas annoncer une équivalence temporelle
complète. Trois écrans finaux de navigation identiques ; contrôles détaillés
dans emulation_report_v33.json et boot_controls_v33/report.json.

V34 ajoute les blocs 241/242/243/246/247/249/252 (123 entrées). Les alias
248 et 250/251 sont couverts. B252-S018/S019 restent différés (effet 09/6E) ;
B252-S098 à S101 sont des invites de débogage laissées en anglais. Les blocs
235/236 et 244/245 sont intacts. Prochain lot : 253 et journal210, ou prise
en charge raisonnée des effets avant de traduire 235/236.

Pagination V34 : B247-S005 et B252-S008/S025 resserrés avant essais ;
B242-S003, B246-S004 et B252-S002/S010/S014/S021/S037/S094 corrigés après
relecture. Les preuves finales utilisent le tag corrected pour V34 et V33.
Les captures intermédiaires de pause peuvent répéter un texte partiel.
B252-S039/S059 gardent des lignes finales vides héritées de la source ;
une capture vide après le texte complet ne signifie pas un message absent.
