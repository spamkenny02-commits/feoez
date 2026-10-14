# Compte rendu V12

66 nouvelles entrées intégrées, soit 568 au total. Le lot 07 traduit
l'orpaillage au village des Paillettes d'Or (bloc partagé 77/78), le bouton
du château (81/82), l'affrontement avec Kingin et le Goldsilver (83), puis
les habitants et les fêtes du sanctuaire du Chien divin (87).
Les alias ne sont pas comptés deux fois. Ce lot est un premier jet depuis
l'anglais ; Goldsilver et Atramentous Alabaster restent provisoirement inchangés.

Les 502 anciennes entrées sont identiques à la V11, texte et mise en page.
981 lectures passent dans les routines originales 65816, y compris les
alias et les chaînes non traduites du bloc des choix. Les 16 contrôles de
police passent ; accents, ordre des balises, pointeurs et aller-retour IPS
sont vérifiés. La largeur maximale est de 216 pixels. Les substitutions
dynamiques conservent une réserve de 96 pixels.

La commande 0E rencontrée dans ces blocs est conservée à l'identique. Le
calcul de largeur lui attribue une avance nulle, sans réinterpréter son
effet de contrôle. Son comportement dans ces nouvelles scènes reste à
vérifier en progression. Aucun autre code bas nouveau n'est autorisé.

32 blocs physiques relocalisés, allocation jusqu'à 0x6C7B00 ; 34 048 octets
restent libres. Les blocs anglais d'origine sont conservés.

Snes9x 1.63 : démarrage neuf, autotests A/B ALL OK, resets, introduction et
début de partie jusqu'aux menus et à la carte. 608 commandes reproduites.
Les 85 captures communes avec le parcours V11 sont identiques pixel par pixel.
Les 66 nouvelles entrées ne sont pas encore observées dans leurs scènes.
Le rapport V12 associe explicitement les hashes du patch et de la ROM testée.

Appliquer le patch V12 à la ROM anglaise originale ; ne pas cumuler les patches.
Branche de travail : dev-v12. Aucun fichier ROM ou état d'émulateur n'est publié.
