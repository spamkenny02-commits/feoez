# Compte rendu V20

61 entrées ajoutées, dont 60 textes modifiés et B140-S024 conservée.
Total : 1 442 entrées intégrées. Galerie de Sara, libération de Tenjin,
Binan et Chitose, parchemins et statue de Sara (alias 143/144/145/146).
Les chansons 140/2, 22 et 27 restent en anglais, avec leurs commandes intactes.

Correction volontaire de B136-S010 après essai à l'écran : phrase raccourcie
pour éviter « Feu ! » seul sur une dernière page. Les 1 380 autres entrées
antérieures restent identiques. Correction séparée dans corrections_v20.json,
sans changer les sources historiques de V19.

1 925 lectures natives 65816, 16 contrôles de police et 14 contrôles du
placement passent. Encodage, balises, largeur, alias, checksum et IPS vérifiés.
55 blocs sur place, 19 déplacés ; 95 648 octets libres.
16 messages différés et le bloc 132 restent inchangés en anglais.

Snes9x standard 1.63 : démarrage neuf, autotests A/B ALL OK, introduction,
début de partie, menus et carte. 85 captures communes avec V19 identiques.
Réglages et carte identiques ; différence du menu limitée à l'horloge.

Douze essais ciblés supplémentaires sur la ROM finale, sans changer ses octets :
pierre de la Grue, lettre, remise 20 %, Omine 5 000/1 000 ryo, Sara,
annonce d'arrivée et présentation de Tenjin, parchemins, statue et alias.
Le noyau de diagnostic redirige une seule demande de dialogue vers le bloc/index
retenu. Lookup, sélection, lecture et rendu natifs ; terminateur exact contrôlé.
Captures fréquentes et relecture visuelle : textes, accents et pagination observés.
La page finale de la Grue corrigée et les montants d'Omine sont capturés.
Le message de sauvetage conserve ses lignes vides et une fin de page courte.

Ces essais ciblés sont un banc de rendu : arrière-plans hors contexte, et aucune
validation des positions des PNJ, choix de quête, récompenses ou recrutement.
Les scènes complètes en progression normale restent à vérifier. Le noyau standard
reste distinct du noyau de diagnostic ; les scripts de construction et de rejeu
sont inclus. Aucun noyau binaire, ROM, état ou dump mémoire publié.

Appliquer le patch V20 directement à la ROM anglaise originale, sans cumuler
les versions. Sauvegarde sur main. Rapports et captures : verification/scenes_v20.
