# V31 — Pays du Paon, ermites et fins

150 entrées ajoutées, dont 149 modifiées et une entrée de ponctuation
conservée. Total : 2 751. Les 2 601 entrées de V30 gardent leur texte
et leur disposition. Les fins partagées par 217/218, les ermites,
le Temple de la Pluie et Double-Chance constituent ce lot.

Les huit indices de l'ermite Bouddhiste gardent les objets, directions,
conditions et commandes, notamment X avec gauche, bas-gauche, bas,
bas-droite, droite, puis A pour le Ma-Djinn. La chrysalide dure 40 à
50 heures. Le tarif de l'auberge est cinquante ryo. Les seize fusions
sont présentées en conservant l'ordre des éléments.

Le banc de lecture bornait chaque appel à 100 000 instructions. Or,
l'anglais B221-S011 en demande déjà 118 082 pour sélectionner sa chaîne.
La sélection dispose maintenant d'un plafond de 500 000, configurable ;
le moteur de la ROM n'est pas modifié. Six sélections sur la source anglaise
sont vérifiées dans selection_checks_v31.json.

La relecture a conduit à resserrer B221-S001/S021/S024/S049,
B223-S026 et B224-S008, sans changer la séquence des balises.
Le refrain absurde de Ça-Roule conserve ses rimes dans les deux variantes.

## Validation

3 532 lectures natives, 16 contrôles de police et 14 de placement réussis.
107 blocs sur place, 31 relocalisés ; 80848 octets libres.
A : COMPLETE / ALL OK ; B : les deux BACKUP OK.

Voir verification/build_report.json, verification/emulation_report_v31.json
et verification/scenes_v31/render_report.json pour les résultats.
Soixante cas ciblés couvrent les passages longs, les panneaux, le choix
de fin et son alias, les indices et les variantes avant/après la pluie.

Les essais redirigent un appel de dialogue. Ils ne valident pas la
progression naturelle, la sélection effective des fins, les combats,
les effets des sorts, les paiements, les récompenses ni le vol du
Mahamayuri. Les 41 messages différés restent intacts, notamment
B221-S022 contenant le fragment ambigu x5. Le journal 210 reste à
traiter ; les blocs 132 et 183 sont inchangés.

Appliquer Tengai_Makyou_Zero_FR_V31.ips directement à la ROM anglaise
originale, sans cumuler les patches.
