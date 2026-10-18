# V40 — Omine et la ville du Grand Tigre

41 textes supplémentaires du bloc 86. Total : 3 440 entrées intégrées.
Les 3 399 entrées V39 et les 32 occurrences initiales sont conservées :
analyses mémoire/SRAM/RTC, naissance et horloge.

Omine au grand cœur vend trois insignes pour 3 000 ryo, soit 1 000 pièce.
Les habitants parlent de la mine, des distractions et des dons de 1 000 ryo.
L’épreuve de l’ermite et son échec en quittant la ville restent décrits.
La séquence du jeu conserve centre, droite, gauche, centre, gauche.
Le sanctuaire de Byakko et l’insecte mange-or gardent leur sens.
Le surnom d’Omine et la grotte du Clapotis suivent le glossaire établi.

B086-S007/008/009 conservent leurs bytes anglais : commandes de noms
variables 05/06/07 non prises en charge. Les différés antérieurs restent
également intacts. Le cœur B086-S015 conserve sa séquence 09/6E/08,
sans modifier les routines d’effet.

Les essais ciblés redirigent une demande vers chaque texte avec les routines
natives. Ils vérifient pages et terminateur exact, pas les achats, dons,
effets des insignes ou réussite de l’épreuve en progression naturelle.
Snes9x 1.63 est utilisé ; 1.60 et le matériel réel ne sont pas testés.
Les preuves approfondies de saisie de naissance restent celles de V35.
Les essais V40 utilisent final ; la référence V39 utilise reference40.

Appliquer le patch IPS directement à la ROM anglaise originale, sans cumul.
Les résultats définitifs sont dans verification/emulation_report_v40.json.

Construction : 4 259 lectures natives réussies. 134 blocs sur place,
34 relocalisés, 77 312 octets libres. 16 contrôles de police et
14 contrôles de placement réussis. Les 3 399 entrées antérieures
sont identiques (texte français, texte mis en page et bytes source).

Résultats finaux : 41 cas ciblés, 57 captures relues. Les 85 captures fixes
du début et les trois écrans de navigation sont identiques à V39.
Les 32 occurrences initiales et les signatures internes sont identiques
octet par octet. 84 lectures des différés conservent leurs bytes source.
Les captures intermédiaires de pause peuvent répéter un texte partiel ;
chaque cas termine sa lecture au terminateur natif exact.
