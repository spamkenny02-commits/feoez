# V53 — Lot 47 complet

400 nouveaux textes distincts : 388 sources bornées et 12 mois natifs.
580 occurrences bornées intégrées, variantes et alias exclus du compteur.
Les 5 381 entrées V52 sont préservées : aucun ancien texte modifié.
Trois retouches de relecture du nouveau brouillon ne sont pas recomptées.
Total : 5 961 occurrences bornées, plus les libellés natifs hors inventaire.

Le lot couvre les substitutions d’accessoires, parchemins et techniques,
les lieux et titres de progression, la boussole, des services et événements,
l’élevage et ses choix, les dates/horaires, des chansons et six résultats de
combat. Les variantes de catalogue, de lieu, de pause, de variable ou de cri
partagé restent intégrées sans constituer de nouveaux textes distincts.
Le lecteur x1 des mois à deux chiffres est corrigé ; les ordinaux deviennent
1er, 2e..31e. Les producteurs de date et les formats spéciaux sont documentés.

## Vérifications exécutées

IPS autonome reconstruit depuis la source anglaise épinglée. Deux constructions
produisent exactement la même ROM ; `tools/build_v53.py` reproduit le patch.
Encodage, commandes, pointeurs, alias, réserves, collisions, checksum,
aller-retour IPS et données hors périmètre contrôlés. 6 756 lectures natives,
14 contrôles de stockage ; 42 400 octets libres dans la réserve contrôlée.
Les 5 381 textes V52 et les octets V52 hors plages autorisées sont préservés.

Sur la ROM finale exacte : démarrage neuf, A/reset/B, navigation vers le menu,
les paramètres et la carte ; 722 cas natifs avec état neuf de cette même ROM.
236 cas de catalogue, 153 messages, 191 libellés, 103 formats et 39 contraintes
extrêmes. Les variables réellement consommées par ces fixtures sont vérifiées.
Les 619 captures de texte distinctes ont toutes été ouvertes et relues,
préfixes et pages compris ; cinq vues système et l’Almanach réel également.
Les instantanés intermédiaires de pause sont distingués des pages complètes.

447 expansions finies des résultats de combat sont contrôlées : 43 octets
et 196 pixels au maximum. Leur lecteur FD8B s’arrêtant au saut de ligne,
ces six messages restent sur une ligne. Ce contrôle ne constitue pas une
relecture de la boîte de résultat pendant un véritable combat.

La carte réelle affiche « Pays de l’Ours de Feu » et « O + E ».
L’Almanach réel au 22/12/1995 conserve les libellés français, Jour faste,
Solstice d’hiver et la notice B018-S182. Les autres dates restent à parcourir.

Comparaison à V52 : 69/85 captures de démarrage et 2/7 vues de navigation
identiques. Les 21 paires différentes ont été réellement ouvertes : animations,
positions des PNJ, clignotement de la flèche et carte traduite. Aucune corruption
visuelle évidente observée ; la cause de chaque écart de phase n’est pas tracée.
Il ne s’agit donc pas d’une régression intégralement identique au pixel près.

ROM finale : `ba2b468c2ba2f05ba542d421213c1564861fed7e35018704b88038608dcc2f7c`.
IPS : `0ac14f5583ba54ab3a7b00156a3dac61f4274b9fff14b0f9436c47713f7c9272`.
Preuves fraîches : `lot47p400d` ; rapports dans `verification/emulation_report_v53.json`,
`relecture_v53.json`, `coverage_v53.json` et `scenes_v53/render_report.json`.

## Restes et limites

La phase 1 reste ouverte : événements/dialogues/calendrier différés et parcours
naturels des services, de l’élevage, des choix, des variables et des chansons.
Les rendus injectés ne prouvent ni les vraies valeurs ni les sélecteurs,
récompenses, échéances ou la synchronisation musicale. Les libellés de lieu
rendus dans une fenêtre de dialogue ne valident pas tous les champs de carte
ou de sauvegarde. Les sept anciennes étiquettes d’Almanach ne traduisent pas
ses graphismes : « Biorhythm » et les jours graphiques restent visibles en anglais.

Les phases 2 et 3 restent ouvertes : menus et sous-menus, variantes 8/9,
combats, fins/générique, graphismes, accès calculés, bloc 42 non borné, puis
relecture globale du français avec registre de zones/écrans/branches.
L’inventaire borné compte encore 3 077 entrées, dont 1 570 non vides,
menus et debug compris. Il ne mesure pas la couverture de tout le jeu.

Les619 captures de texte relues sont regroupées en40 planches compactes,
avec empreintes et coordonnées par cas dans scenes_v53/render_report.json.
Les pixels des fenêtres de texte sont conservés exactement, à échelle2.
