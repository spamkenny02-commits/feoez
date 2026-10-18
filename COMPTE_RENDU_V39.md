# V39 — La mine d’or

23 textes supplémentaires du bloc 94 : insignes, bourses, mine, promotions
et indications vers les ermites. Total : 3 399 entrées.
Les 3 376 entrées précédentes sont conservées ainsi que les 32 occurrences
initiales (analyses mémoire/SRAM/RTC, naissance et horloge).

B094-S004 conserve ses bytes anglais : sa commande dynamique 07 demande
un traitement dédié. Les différés antérieurs restent également intacts.
La plaisanterie des bourses, le prix de 20 000 ryo, les limites de deux/dix
blocs et les promotions des 10, 20 et 30 sont conservés.

Les essais ciblés utilisent les routines natives pour lire et afficher chaque
texte jusqu’à son terminateur. Ils ne valident pas les achats, échanges,
calendriers commerciaux ou événements en progression naturelle.
Snes9x 1.63 est utilisé ; 1.60 et le matériel réel ne sont pas testés.
Les preuves approfondies de saisie de naissance restent celles de V35.

Appliquer le patch IPS directement à la ROM anglaise originale, sans cumul.
Les résultats définitifs sont dans verification/emulation_report_v39.json.

Construction : 4 215 lectures natives réussies, 133 blocs sur place,
34 relocalisés, 77 312 octets libres. 16 contrôles de police et
14 contrôles de placement réussis.

Les essais définitifs utilisent le tag corrected ; la référence V38
utilise reference39. Deux fins de phrases isolées ont été raccourcies
avant la dernière construction. Les pauses restent dans le même ordre.

Dans B094-S005, la commande 04 affiche la valeur Higan de l’état de test ;
ce rendu ne valide pas l’injection du prix dans la situation naturelle.
La commande et sa réserve de largeur sont conservées.

Résultats finaux : 23 cas ciblés, 31 captures relues. Les 85 captures fixes
du début et les trois écrans de navigation sont identiques à V38.
Les 32 occurrences initiales et les signatures internes sont identiques
octet par octet. 81 lectures natives des différés conservent leurs bytes source.
