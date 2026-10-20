# V49 — Fêtes saisonnières, marchands et Pavillon des Geishas

**300 nouveaux textes ; 4 387 entrées intégrées.**
Lot 43 : 13 annonces calendaires (bloc 31), 74 messages de coffres,
de marchands et de salons (bloc 37), 36 répliques du Pavillon des Geishas
(bloc 39) et 177 textes de fêtes et concours (bloc 40).
Les quatre blocs restent partiels ; leurs autres entrées gardent leurs octets source.
Aucun texte vide ni diagnostic ajouté au compteur.

Les prix, dates, cinq lettres du voeu, cinq victoires de sumo et dix secondes
du sablier restent ceux du jeu source. Les commandes X/A, les directions,
les pauses et les balises gardent leur ordre. Les fêtes conservent leur calendrier
interne et les annonces leur contexte d'origine, même quand leurs dates diffèrent
des jours fériés actuels. Les allusions et plaisanteries restent celles de la source.

## Vérifications

ROM anglaise originale épinglée ; référence V48 conforme à son empreinte publiée.
5 446 lectures natives, 16 contrôles de police et 14 de placement réussis.
Encodage, balises, pauses, largeur de 216 pixels, pointeurs, allocation,
checksum et aller-retour IPS vérifiés. 148 blocs sur place,
35 relocalisés ; 56608 octets libres.
Snes9x 1.63, tag final49 : démarrage neuf, navigation, A/reset/B prolongé.
300 terminateurs exacts, 446 captures de dialogue et cinq captures système relues.
85 captures fixes et trois vues de navigation identiques à V48.
Les 4 087 anciennes entrées gardent français, mise en page et octets source.
32 modifications initiales et marqueurs SPC7110 intacts ; 293 lectures de différés.
A et B : TERMINE / TOUT OK ; B confirme SAUV. RTC et SAUV. SRAM OK.
Les pauses peuvent produire des captures partielles ou répétées ; certaines
fins de page contiennent peu de mots. La lecture complète est vérifiée séparément.
ROM : `e13a8bcdee8cac7d53e33fb9092de5ec5d84d5613ef83ff5836cd70b6c2af396`.
IPS : `8b808eaf756527b58f0fc11b14cd22a303b5872a51fd258fded0aa6708ffabbe`.
Voir emulation_report_v49.json et scenes_v49/render_report.json.

## Limites

Les rendus ciblés vérifient le texte affiché et sa lecture complète ; ils ne
valident pas la progression naturelle, les paiements, récompenses, concours,
voeux saisis ou limites du calendrier. Les sélecteurs particuliers, libellés
et commandes restant à analyser sont différés. Les différés antérieurs et le bloc
183 de debug sont préservés. Les noms d'objets nouveaux sont provisoires,
à harmoniser avec la traduction future des menus.
Naissance détaillée : preuves V35. Snes9x 1.60 et matériel réel non testés.
Les dialogues et événements ne sont pas complets ; menus ensuite.

Appliquer Tengai_Makyou_Zero_FR_V49.ips à la ROM anglaise originale, sans cumul.
Aucune ROM, sauvegarde d'état ou noyau d'émulateur n'est publié.
