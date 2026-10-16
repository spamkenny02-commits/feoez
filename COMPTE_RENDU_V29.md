# V29 — Énigmes de Juri et château de la Tortue

198 entrées ajoutées : 194 textes modifiés, trois entrées vides et une réplique
neutre conservées. Total : 2 563 entrées. Les 2 365 entrées de V28 sont
inchangées, y compris leur disposition en jeu.

Le lot couvre les énigmes de Juri et le roi de la Forêt, la Tortue divine,
Mitsuko et son coffret, les auberges et les liaisons maritimes. Les accès
206/207 partagent leur texte. DOG/GOD sont conservés avec leur sens français
pour garder le jeu de lettres ; T/F restent les lettres des portes. L’énigme
du un et un garde son ambiguïté entre somme et juxtaposition. La course
des fruits garde sa question sur son début, sans inventer une solution.

La première relecture a conduit à raccourcir B206-S001, B208-S013,
B209-S025 et B211-S005/S010 pour améliorer leur pagination. Les balises,
montants et directions sont conservés ; les preuves publiées proviennent de
la ROM finale reconstruite.

## Validation

- 3 316 lectures natives, encodage, checksum et aller-retour IPS.
- 16 contrôles de police et 14 contrôles de placement.
- 98 blocs sur place, 30 relocalisés ; 81 152 octets libres.
- 36 cas de rendu ciblé ; voir verification/scenes_v29/render_report.json.
- Démarrage et navigation : voir verification/emulation_report_v29.json.

Les essais de rendu redirigent un appel de dialogue : ils ne valident pas
les réponses choisies aux portes, les combats, les soins, paiements, trajets,
récompenses ni la maturation du coffret en progression normale.
Parmi les blocs traités, 40 messages sont différés ; le journal 210 reste
à traiter, et les blocs 132/183 demeurent inchangés.

Appliquer Tengai_Makyou_Zero_FR_V29.ips directement à la ROM anglaise originale,
sans cumuler les patches.
