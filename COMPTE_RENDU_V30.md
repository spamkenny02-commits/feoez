# V30 — Ermites et Arche des Cieux

38 entrées ajoutées, total de 2 601. Les 2 563 entrées de V29 sont
conservées, y compris leur disposition en jeu. Le lot traduit les marchands
du pays du Chien, les ermites Cochon, Rapide et Courant et l'invocation
de l'Arche des Cieux.

Les descriptions de Grognement, Rapidité et Piqûre gardent les cibles
et les caractéristiques indiquées en anglais. Grognement peut atteindre
un allié ou un ennemi ; aucun sens de variation n'est ajouté. Les cinq
créatures, les six cents ans du récit et les directions sont conservés.
Les noms des sorts et des nouvelles créatures restent provisoires.

Trois répliques ont été raccourcies après relecture : B215-S006,
B215-S012 et B216-S005, pour supprimer des fins de page isolées.

## Validation

3 354 lectures natives, 16 contrôles de police et 14 contrôles de placement
réussis. 101 blocs sur place, 30 relocalisés ; 81 152 octets libres.
A : COMPLETE / ALL OK ; B : RTC BACKUP OK et S-RAM BACKUP OK.
Les 38 essais de rendu atteignent leur terminateur ; les pages sont relues.

Les résultats détaillés sont dans verification/build_report.json,
verification/emulation_report_v30.json et verification/scenes_v30/render_report.json.
La comparaison avec V29 porte sur tous les textes déjà intégrés et leur
présentation, le parcours du début et les menus. Les 38 nouvelles entrées
font chacune l'objet d'un essai de rendu ciblé.

Les essais de rendu redirigent un appel de dialogue : ils ne valident pas
la progression naturelle, les combats, les effets des sorts, les récompenses
ni le voyage effectif vers Takamagahara. Les 40 messages différés demeurent
intacts. Le journal 210 et les blocs 217 et suivants restent à traiter ;
les blocs 132 et 183 demeurent inchangés.

Appliquer Tengai_Makyou_Zero_FR_V30.ips directement à la ROM anglaise originale,
sans cumuler les patches.
