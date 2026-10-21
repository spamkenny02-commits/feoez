# V52 — Substitutions et Almanach

**400 nouveaux textes distincts, lot 46 complet, phase 1.**
393 sources bornées sur 394 occurrences (un alias exclu du compteur), plus
7 libellés natifs de l’Almanach. Catalogues d’objets/équipement insérés dans
les dialogues, prédictions, messages numériques, chansons et modes différés,
52 notices et 32 libellés calendaires. Aucun diagnostic, vide ou variante de
menu n’a servi à compléter le lot. 20 corrections au checkpoint 83, sans
recompter ces textes ; les 4987 anciennes entrées V51 sont inchangées.
Total intégré : 5381 occurrences bornées, plus 7 libellés natifs.

## Contrôles exécutés

Source épinglée vérifiée ; IPS autonome reconstruit depuis cette source.
6365 lectures natives du constructeur, 788 lectures source/sortie propres
aux ajouts ; encodage, largeur native, commandes, pointeurs, alias, allocation,
réserves, collisions, marqueurs SPC7110, checksum et aller-retour IPS.
16 contrôles de police, 14 de stockage. 1944 copies natives pour 243 occurrences
de noms, 12 prédictions finies, 2140 sondes du producteur numérique et 768
exécutions des handlers 08/09/0A. Les sondes 65816 sont restreintes ; la
multiplication IO est modélisée sans preuve de timing.

488 rendus ciblés frais : 105 textes simples, 128 profils numériques, 12
prédictions et 243 substitutions de noms. Les captures sélectionnées ont été
relues sur la ROM finale ; les valeurs injectées et consommées sont contrôlées.
Démarrage neuf, A/reset/B et navigation exécutés. 85 captures fixes et 7 vues
de navigation identiques à V51. L’Almanach réel a été ouvert au 22/12/1995 :
sept libellés français, Jour faste, Solstice d’hiver et notice B018-S182 relus.
Le flux natif FE conserve exactement la reprise ED53 et les champs limités.
Les deux lignes/séparateurs des notices restent à leur place.

Les essais ont rejeté deux candidats avant publication : alignement du menu
Almanach puis chevauchement numérique et rang d’une chanson. Les nouvelles
captures confirment les corrections. Voir lot46_review_rejections.json.

ROM finale : `d74ba2aaff5e9f01dacde9c630e6e8c34495b7aba5a6a5f5256f6e72d6a4f862`.
IPS : `633989729423429d5b5d85736debf36ac660f1b705a57ddf1091f7ad0a927ff2`.
Preuves : verification/emulation_report_v52.json, scenes_v52/render_report.json,
relecture_v52.json et coverage_v52.json. Tag : lot46p400b.

## Restes et limites

La phase 1 continue. Les rendus avec fixtures sont synthétiques : ils ne prouvent
ni déclenchement naturel des événements, ni vrais choix/valeurs, récompenses,
musique ou effets. La seule date naturelle observée est 22/12/1995. Les
catalogues sont ceux des substitutions ; les variantes de menu restent à
harmoniser. Les anecdotes historiques suivent la source, sans correction inventée.

3657 entrées restent dans l’inventaire borné, dont 2150 non vides, avec menus
et debug. Ce compteur ne prouve pas la couverture du jeu. Bloc 42 non borné,
accès calculés, graphismes, fin et générique exigent encore la phase 2 complète.
La relecture de ce lot ne remplace pas la relecture globale de phase 3.
Snes9x 1.60 et matériel réel non testés. Aucune ROM, noyau, état ou mémoire
n’est distribué.
