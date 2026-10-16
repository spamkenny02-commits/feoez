# V33 — Sanctuaire du Paon, presse et vallée de Pierre

152 entrées ajoutées, dont 151 modifiées et une entrée vide conservée.
Total : 3 037. Les 2 885 entrées de V32 gardent leur texte et leur disposition.
Le lot couvre le sanctuaire du Paon, ses fêtes, la Presse du Paon et la
vallée de Pierre.

Les articles conservent leurs affirmations fantaisistes et accusations.
Les titres et leur ordre sont conservés dans les deux menus. Les débuts
de seconde colonne restent à un pixel au plus de ceux de l'anglais,
selon les largeurs de la police ; les lignes du menu sont explicites.
Le jeu de mots new year/new ear est adapté en « bonne oreillée ».

Le thé annonce dix points de santé, le don du Nouvel An 5 000 ryo,
la nuit 50 ryo et l'article dix ryo. Fêtes dès le 1er janvier et le
1er avril, foires les dimanches de mars et septembre. La pierre du Paon
réduit la consommation de technique sans quantité inventée.

Après relecture, B233-S020 et B234-S032/S057 ont été resserrés pour
regrouper leurs fins de phrase. Les preuves finales proviennent de la
ROM reconstruite après ces corrections.

## Validation

3 828 lectures natives, 16 contrôles de police et 14 de placement réussis.
120 blocs sur place, 31 relocalisés ; 80848 octets libres.
A : COMPLETE / ALL OK ; B : les deux BACKUP OK.

Voir verification/build_report.json, verification/emulation_report_v33.json
et verification/scenes_v33/render_report.json. Soixante-trois cas couvrent
les menus, les longs articles, les indices et les variantes du sanctuaire.


La comparaison à images fixes donne 59 captures identiques sur 85 et 26
écarts de phase d’animation, de transition ou de dialogue. Leur cause
reste non établie. Aucun texte visiblement corrompu n’a été observé dans
ces paires. Le contrôle V32 frais reproduit la V32 historique ; deux
constructions V33 reproduisent les mêmes 85 captures. L’échange des sommes
de contrôle d’en-tête ne modifie pas ces résultats.
Les trois écrans finaux de navigation sont identiques. Après 1 200 images
sans entrée, deux fenêtres de dialogue sont identiques ; la troisième,
dans une cinématique animée, reste décalée. Ces contrôles ne démontrent
pas l’équivalence temporelle complète des deux versions.
Voir verification/comparison_v32_v33.json, control_comparison_v33.json,
checksum_controls_v33.json et boot_controls_v33/report.json.

Les essais de rendu redirigent un dialogue : ils ne valident pas la
progression naturelle, les sélections d'articles, les combats, récompenses,
effets du thé ou de la pierre, paiements et calendrier réels.
48 messages sont différés, dont B234-S050. Le journal 210 et les blocs
235/236 restent à traiter ; les blocs 132 et 183 demeurent inchangés.

Appliquer Tengai_Makyou_Zero_FR_V33.ips directement à la ROM anglaise
originale, sans cumuler les patches.
