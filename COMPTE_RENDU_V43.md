# V43 — Grand Tigre, Miho et retrouvailles

125 vrais nouveaux textes, non vides et modifiés ; **3 667 entrées intégrées**.
Lot 37, bloc 95 partiel : insignes d'or, auberge, Shiranui, demandes de Miho,
parfums et retrouvailles de Rie et Shigenobu. Les 3 542 entrées V42 sont
identiques en français, mise en page et octets source. Les 32 modifications
françaises initiales et les signatures internes sont conservées.

Les insignes coûtent 20 000 ryo, trois 60 000, ou 50 000 en promotion ;
ils empêchent les rouleaux et ne s'enlèvent pas soi-même. L'ermite se trouve
au nord-ouest de la mine. L'auberge coûte 1 000 ryo. Les prélèvements de Miho
restent à 100 000 ryo. La clé de l'Amour uni garde le nom déjà employé chez
Shigenobu ; elle doit lui être remise au sanctuaire du Chien divin.

## Vérifications

ROM anglaise originale épinglée ; IPS autonome, encodage, séquence exacte des
balises et pauses, largeurs de 216 pixels, pointeurs, allocation, checksum et
aller-retour IPS contrôlés. 4637 lectures par les routines natives
65816, 16 contrôles de police et 14 de placement réussis.

La référence V42 existante retrouve son empreinte publiée et a été rejouée
sous le tag reference43. Les preuves finales V43 utilisent exclusivement
corrected43 et l'empreinte 4693478e747d1be3138464db6c7cf0c4aef0a5a6113fde6dc00315b3a07b660f.
Snes9x 1.63 : démarrage neuf, navigation, A puis reset puis B prolongé.
125 rendus ciblés atteignent le terminateur exact ; 172 captures relues.
85 captures fixes identiques à V42,
0 différentes. Navigation détaillée dans
navigation_comparison_v42_v43.json. Les fins de page ont été regroupées par
phrases ; notamment S134/S137 ne finissent plus seules sur « Compris ? ».

## Différés et limites

Les horaires AM/PM et délais de Miho restent intacts, avec leurs commandes
04/05/06 et fragments x1..x5. S011 : noms dynamiques 05/06/07 ; S046 : x5 ;
S056 : achat de maison à colonnes. S095-S108 (autres chambres) et S165-S204
(boutiques, journal, variantes de ville) restent à reprendre ; ce ne sont pas
tous des blocages techniques. S180 : choix à colonnes, S184 : effet 0A/CB.
Tous les différés antérieurs restent intacts ; voir deferred_texts_v43.json,
deferred_reasons_v43.json et unprocessed_inventory_v43.json.

Le rendu ciblé redirige une demande de dialogue : il ne valide ni progression
naturelle des quêtes, ni achats, cadeaux, affection, délais, effets de combat
ou choix effectifs. La saisie détaillée de naissance reste documentée par V35 ;
les 32 modifications sont comparées à V42 et le démarrage standard est rejoué.
Conditions d'échec, limites de calendrier, Snes9x 1.60 et matériel réel non testés.

Appliquer Tengai_Makyou_Zero_FR_V43.ips directement à la ROM anglaise originale,
sans cumul. Aucune ROM, sauvegarde d'état ou noyau d'émulateur n'est publié.
