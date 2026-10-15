# V26 — Subaru, miroirs et Feu d’Agni

102 entrées ajoutées, dont 97 textes modifiés et cinq réponses neutres :
2 087 intégrées. Les 1 985 entrées de V25 sont conservées sans modification.

Le lot couvre les œufs de fée et le retour de Subaru, les révélations sur Agni
et Ninigi, les variantes Tenjin/Mizuki, le calendrier du sanctuaire, le village
du Katana, la grotte des Nuages et la transformation de l’épée d’Agni.
L’indice de l’anneau de l’Âme est rimé en français et garde la condition du vol
de l’Arche. Toutes les balises et leur ordre sont préservés.

La première relecture à l’écran a conduit à raccourcir six répliques :
B177-S005/S025, B178-S025/S031/S035 et B179-S015. Ces retouches évitent
notamment des fins de page isolées et conservent les pauses du script source.
Les preuves publiées doivent toutes provenir de la ROM finale reconstruite.

## Validation

- 2 667 lectures natives 65816, encodage, checksum et aller-retour IPS.
- 16 contrôles de police et 14 contrôles de placement.
- 77 blocs sur place, 28 relocalisés ; 83 360 octets libres.
- Comparaison V25 : textes précédents identiques.
- Vingt cas de rendu ciblé ; voir verification/scenes_v26/render_report.json.
- Démarrage, contrôles A/B et navigation : voir emulation_report_v26.json.

Les essais ciblés redirigent un appel de dialogue avec un noyau de diagnostic.
Ils vérifient le rendu et le terminateur exact, sans valider la progression
naturelle, les récompenses, le repos, les combats, les conditions de calendrier
ou l’obtention de l’épée. Dix-huit messages différés et le bloc 132 restent
en anglais. Appliquer le patch directement à la ROM anglaise originale.
