# V42 — Village des Paillettes d'Or, Basara et ermites

59 textes nouveaux, non vides et modifiés ; **3 542 entrées intégrées**.
Les 3 483 entrées V41 sont identiques (français, mise en page et octets source).
Sources : lot36_fr.json, blocs 91 (alias 92), 99 et 102.

Les prix restent 100 ryo à l'auberge et 20 000 pour la bourse d'or : une par
client, deux blocs sûrs, dix en forçant, perte de tout l'or en cas de déchirure.
Directions sud-ouest vers la forêt de la Vie, nord-est vers mine/cascade,
sud puis est vers le château d'Or. Basara : lundi-samedi de 18 h à minuit,
dimanche fermé ; sa Lame consomme la moitié de la vitalité. Les récits
conservent les six cents ans, Byakko/Kingin, Agni et les douze bêtes.
Somnolence est réservée à l'être des Enfers sur lui-même. Pas de vertu
pour un personnage encore pétrifié à la fin du combat.

Les sauts de ligne des nouvelles répliques ont été regroupés à des fins
de phrase pour éviter les mots seuls et les consignes coupées aux changements
de page. Toutes les commandes et pauses restent dans leur ordre. Le choix
Combattre/Partir garde la ligne 7 d'origine et sa seconde colonne à un pixel près.
Aucun ancien texte ni moteur d'effet n'est modifié.

## Vérifications

La référence V41 a été reconstruite depuis les sources publiées : empreinte
exactement identique à la V41 publiée. Les parcours de référence utilisent
reference42 ; les preuves V42 utilisent uniquement corrected42 et la ROM finale.
4 433 lectures natives, encodage, balises, largeurs, pointeurs, allocation,
checksum et aller-retour IPS passent. 16 contrôles de police, 14 de placement.
138 blocs sur place, 34 relocalisés, 77312 octets libres.
Les 32 occurrences initiales et les signatures internes sont intactes.

Snes9x 1.63 : démarrage, navigation et A/B prolongé. A TERMINE / TOUT OK ;
B SAUV. RTC et SAUV. SRAM OK. 59 cas ciblés, 137 captures finales relues.
85 captures fixes du début identiques à V41, 0 différentes ; navigation
détaillée dans navigation_comparison_v41_v42.json. Les preuves sont liées
à l'empreinte de la ROM finale dans emulation_report_v42.json.

## Différés et limites

125 lectures des différés conservent les octets de la source.
B091-S001/002 : prix 05 ; S026 : fragment x5 ; S035 : chant 0A/CC.
B099-S001/002/003/011/S014-S019 : groupe horaire (AM/PM, jours, 05/06/07, x2/x3).
B102-S001/003 : questions à colonnes à étudier avec leur sélection effective.
Les différés antérieurs, blocs 132/183 et autres blocs inventoriés restent intacts.

Les essais ciblés redirigent un dialogue ; ils ne valident pas les quêtes
naturelles, achats, échanges, duels, récompenses, choix effectifs ou effets
en combat. La saisie détaillée de naissance reste celle de V35. Conditions
d'échec, toutes les limites de calendrier, Snes9x 1.60 et matériel réel non testés.

Appliquer l'IPS autonome à la ROM anglaise originale, sans cumul.
Aucune ROM, sauvegarde d'état ou noyau d'émulateur n'est publié.
