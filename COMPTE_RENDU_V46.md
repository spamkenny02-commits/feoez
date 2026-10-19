# V46 — Ran, Miki, Suu et la grotte des Belles

31 nouveaux textes, non vides et modifiés ; **3 828 entrées intégrées**.
Lot 40 : bloc 56, S001–S032 sauf S012. Récompenses, retrouvailles,
présentation des trois belles, fontaine et passage vers le pays du Paon.
Les 3 797 entrées V45 restent conservées ; contrôles détaillés ci-dessous.

La source garde son ton et ses allusions ; les noms, l'épellation S-U-U,
les cœurs, l'ordre des pauses et les indications de temps sont conservés.
La fontaine change trois ou quatre fois par heure ; ses trois couleurs
peuvent devenir pêche. Le Héros de la Flamme reste ainsi nommé par Miki.

## Vérifications

ROM anglaise originale épinglée ; la V45 reconstruite retrouve son empreinte publiée.
4 751 lectures natives 65816, 16 contrôles de police et 14 de placement réussis.
Encodage, ordre des balises, pauses, largeur maximale de 216 pixels, pointeurs,
allocation, checksum et aller-retour IPS vérifiés. 143 blocs sur place,
34 relocalisés ; 77 312 octets libres.

Snes9x 1.63, tag final46 : démarrage neuf, navigation, A/reset/B prolongé.
A et B terminent avec TERMINE / TOUT OK ; B confirme SAUV. RTC et SAUV. SRAM OK.
31 terminateurs exacts, 39 captures de dialogue et 5 captures système relues.
85 captures fixes identiques à V45, 0 différentes ; les trois écrans de
navigation sont identiques. 157 lectures natives confirment les octets différés.
Les 32 modifications initiales et les deux marqueurs SPC7110 CHECK OK sont intacts.
Les 3 797 anciennes entrées gardent français, mise en page et octets source.

ROM V46 : `3c7b27e6a171877b10f8cc000daeb376505b3ce12aec4ab00881d39908403eb5`.
Patch IPS : `9127c1100673f89de8b01c4fa98eaa519f5b086237ff9b0e80086276aea777b5`.
Voir emulation_report_v46.json et scenes_v46/render_report.json.
L'inventaire restant distingue les blocs bornés, les entrées vides et le bloc 42
sans borne finale validée ; il ne mesure pas le seul nombre de dialogues.

## Limites

B056-S012 reste en anglais : fragment x5 et espacement particulier à analyser.
Les autres textes différés restent préservés octet par octet.
Les rendus ciblés ne prouvent ni rencontres naturelles aux heures prévues,
ni sélection d'une des trois belles, ni remise effective des récompenses.
Les dialogues et événements ne sont pas encore complets.

Appliquer Tengai_Makyou_Zero_FR_V46.ips à la ROM anglaise originale, sans cumul.
Aucune ROM, sauvegarde d'état ou noyau d'émulateur n'est publié.
