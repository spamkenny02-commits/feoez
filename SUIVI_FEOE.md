# État actuel — V36

3 203 dialogues intégrés : 43 nouveaux dans lot30_fr.json (167, 244/245, 253).
Les 3 160 entrées antérieures et les 32 occurrences initiales V35 sont conservées.
Prochain lot : récit des crabes et journal 210, puis effets des blocs 235/236.
Les preuves V36 utilisent le tag corrected ; référence V35 : final.
Les choix de boutons et événements ne sont pas validés en progression naturelle.

## Historique et consignes

# Reprise du chantier FEOE

Le README et le HEAD de main font foi. V35 garde les 3 160 dialogues de V34
et traduit 32 occurrences sur les écrans mémoire, naissance et horloge.
Sources : build_v35.py et startup_text.py, en complément des 29 lots et de
corrections_v20.json. Les mises en page particulières sont conservées.

## Ressources locales

La copie de travail peut être retrouvée sous feoez_work dans l'espace de travail.
La ROM anglaise épinglée est dans ../upload/Tengai Makyou Zero.sfc ; son SHA-256
est documenté dans le README. Le matériel de test local est sous ../emulator :
snes9x_libretro_standard.so, snes9x_libretro_diagnostic.so et runs/.
Ces ressources ne sont pas publiées dans le dépôt. Vérifier leur disponibilité
avant de promettre une reconstruction ou un essai ; ne jamais inventer un résultat.

## Priorité demandée : écrans de démarrage et date de naissance

Demande explicite du 16 octobre 2026 : inclure les textes encore anglais
au démarrage, avant de considérer la traduction complète.

- Programme de vérification SPC7110 : mémoire/SRAM, bus de données et
  d'adresses, sauvegardes SRAM et RTC, résultats OK/erreur, fin du contrôle
  et instruction de réinitialisation. Conserver les sigles techniques utiles.
- Questions, choix, champs et confirmations de la date de naissance au
  début du jeu. Les distinguer du réglage de la date et de l'heure RTC ;
  inspecter aussi ce réglage pour relever ses textes encore anglais.
- Repères ASCII confirmés dans la ROM anglaise : titre SPC7110 à 0xFF022,
  RTC BACKUP à 0xFF0AE, S-RAM BACKUP à 0xFF0B9, RESET THE SYSTEM à 0xF18A.
  Ces zones sont auditées dans startup_text_v35.json. Le texte de naissance
  est encodé avec la police native à 0xF1D4 ; celui de l'horloge à 0x6D2511.
  Leur encoder spécifique garde les parenthèses et la barre oblique du menu.
- Captures de référence disponibles dans le parcours standard V34 :
  birthday_question, birth_step1 à birth_step5 et birthday_finished ;
  check_a/check_b dans le parcours A/B. Tester également les confirmations
  et les déplacements entre champs, sans modifier leur logique.

V35 traite ces écrans : 32 occurrences auditées, 43 captures de saisie relues,
38 comparaisons numériques avec V34 réussies. Les marqueurs internes de
sauvegarde restent en anglais volontairement ; ce ne sont pas des textes affichés.

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
  jusqu'aux résultats attendus (V35 : A TERMINE / TOUT OK ; B : SAUV. RTC
  et SAUV. SRAM OK, scenario_checks_v35.json).
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

V35 : ne jamais traduire les marqueurs SPC7110 CHECK OK à 0x2F25/0xFF0E7.
Ils conditionnent le démarrage. startup_text.py les protège explicitement.
Le bandeau ALL OK à 0xFE286 est un flux de tuiles, remplacé par TOUT OK
avec la petite police existante ; aucune instruction n'est modifiée.
Les preuves V35 utilisent le tag final ; la saisie approfondie utilise
v35_startup_inputs_validated et son contrôle v34_startup_inputs_validated.
Le refus d'une naissance future puis l'acceptation de 01-21-1994 sont vérifiés.
Les trois écrans finaux de navigation restent identiques. Les captures fixes
ultérieures peuvent changer de phase ; ne pas annoncer une identité globale.

Pagination V36 : B167-S029, un saut de paragraphe retiré après relecture
pour regrouper une fin de réplique isolée. Balises et texte conservés.
