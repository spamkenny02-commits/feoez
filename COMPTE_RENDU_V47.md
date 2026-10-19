# V47 — Sanctuaire de la Grue, Momoko et Courrier de la Grue

142 nouveaux textes, non vides et modifiés ; **3 970 entrées intégrées**.
Lot 41 : bloc 132, sauf S059, S095, S096, S099, S122 et S126.
Boutiques et auberges avant/après le sable ; lettres et maison de Momoko ;
Yumi, Arisa et Seiko ; trois articles du Courrier de la Grue ; huit ermites.

Conserver 10 000 ryo pour la maison, 150/50 ryo pour les auberges voisines,
10 ryo par article et la limite de sept lettres sans réponse avant la huitième.
Les noms de chambres et de lieux suivent le glossaire. Les récits du journal
restent les propos sensationnalistes du journaliste, non une validation du récit.
Les commandes, cœurs et pauses sont préservés dans leur ordre.

## Vérifications

ROM anglaise originale épinglée ; référence V46 conforme à son empreinte publiée.
4 899 lectures natives 65816, 16 contrôles de police et 14 de placement réussis.
Encodage, ordre des balises et pauses, largeur maximale de 216 pixels, pointeurs,
allocation, checksum et aller-retour IPS vérifiés. 143 blocs sur place,
35 relocalisés ; 56,608 octets libres.

Snes9x 1.63, tag final47 : démarrage neuf, navigation, A/reset/B prolongé.
A et B terminent avec TERMINE / TOUT OK ; B confirme SAUV. RTC et SAUV. SRAM OK.
142 terminateurs exacts, 286 captures de dialogue et 5 captures système relues.
85 captures fixes identiques à V46, 0 différentes ; les trois vues de navigation
sont identiques. Les 32 modifications initiales et les marqueurs SPC7110 sont intacts.
Les 3 828 anciennes entrées gardent français, mise en page et octets source.
163 lectures natives confirment les messages différés.

ROM V47 : `b121123906aaa00d9a15412dfaa3dc44a8902ea42ff98622458187a55e63b879`.
Patch IPS : `156756900edeed2c1bc46e03b3c7aeebbb3308e95bda9d60153b1323da3fad3d`.
Voir emulation_report_v47.json et scenes_v47/render_report.json.
Les pauses produisent des captures partielles et des pages répétées ; certaines
fins de page contiennent peu de mots. La lecture native complète est vérifiée séparément.

## Limites

B132-S059/S122 : diagnostics ; S095/S096/S126 : choix à disposition particulière ;
S099 : fragment x5 à analyser. Les octets des six entrées et des anciens différés
sont préservés. Le bloc 183 de debug reste entièrement intact.
Les rendus redirigés ne valident pas les parcours naturels, paiements, cadeaux,
choix, effets d'objets, réception des lettres, échéance de la huitième lettre,
Saint-Valentin ou progression des deux lettres de Momoko.
Les dialogues et événements ne sont pas encore complets. Menus ensuite.
Conditions d'échec, limites de calendrier, Snes9x 1.60 et matériel réel non testés.

Appliquer Tengai_Makyou_Zero_FR_V47.ips à la ROM anglaise originale, sans cumul.
Aucune ROM, sauvegarde d'état ou noyau d'émulateur n'est publié.
