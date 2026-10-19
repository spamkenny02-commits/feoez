# V44 — Salons, boutiques et presse du pays du Chien

58 vrais nouveaux textes, non vides et modifiés ; **3 725 entrées intégrées**.
Lot 38 : six textes du Cercle Fleuri (88) et 52 textes du Grand Tigre (95).
Akemi/Sayuri, boutiques aux insignes d'or, articles de L'Aboyeur, Ma-Djinn
et derniers remerciements. Ce lot clôt les sections ordinaires retenues sans
ajouter de textes sans rapport pour atteindre un quota.

Les 3 667 entrées V43 sont identiques en français, mise en page et octets source.
Les nouveaux textes du bloc 95 sont fusionnés : aucun remplacement du lot 37.
Les 32 textes initiaux et les signatures internes de sauvegarde sont conservés.
Les commandes et pauses gardent leur séquence exacte. Les indications restent
vendeur ordinaire à droite, insigne d'or à gauche, réduction de trente pour cent,
article à 10 ryo. Les réclames extravagantes restent les propos du journal.

## Vérifications

IPS autonome construit depuis la ROM anglaise originale épinglée. Encodage,
balises, largeurs jusqu'à 216 pixels, pointeurs, allocation, checksum et
aller-retour IPS vérifiés. 4646 lectures par les routines natives 65816,
16 contrôles de police et 14 de placement réussis. 140 blocs sur place,
34 relocalisés, 77312 octets libres.

La référence V43 locale a retrouvé son empreinte publiée et a été rejouée
sous reference44. Preuves V44 : final44, exclusivement liées à la ROM
`d860c12c0040a7f857312427c8446f380df4d260be122dc905432359fcaaa37c`.
Snes9x 1.63 : démarrage neuf, navigation, A puis reset puis B prolongé.
58 cas ciblés atteignent leur terminateur exact ; 115 captures relues.
85 captures fixes du début identiques à V43, 0 différentes.
Voir navigation_comparison_v43_v44.json pour les trois vues de navigation.
Le manifeste des images relues se trouve dans verification/scenes_v44.
Les pauses peuvent répéter des images intermédiaires partielles de la même page.

## Différés et limites

B088-S001/S002/S006 et B095-S184 : effet 0A/CB non interprété.
B095-S180 : trois lignes de choix à deux colonnes. B095-S011 : noms
dynamiques 05/06/07. Les horaires AM/PM et délais de Miho, S046 (x5),
S056 (achat de maison à colonnes) restent intacts, comme les différés antérieurs.
Motifs et inventaires : deferred_reasons_v44.json, deferred_texts_v44.json,
unprocessed_inventory_v44.json. Le bloc 42 n'a pas de borne de fin validée.
La traduction des dialogues/événements n'est pas complète.

Le rendu ciblé redirige une demande de dialogue : il ne valide pas les quêtes
naturelles, achats, issues des choix, délais, récompenses ou effets en combat.
La saisie détaillée de naissance reste documentée par V35 ; les 32 modifications
sont comparées à V43 et le démarrage standard rejoué. Conditions d'échec,
limites du calendrier, Snes9x 1.60 et matériel réel non testés.

Appliquer Tengai_Makyou_Zero_FR_V44.ips directement à la ROM anglaise originale,
sans cumul. Aucune ROM, sauvegarde d'état ou noyau d'émulateur n'est publié.
