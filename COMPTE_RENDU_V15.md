# Compte rendu V15

149 entrées traitées, dont 146 textes modifiés ; trois réponses neutres
restent identiques à la source : B106-S024, B113-S004 et B113-S006.
Le total reconstruit est de 1 013 entrées. Les variantes et répétitions
sont comptées séparément ; ce n'est pas le nombre de dialogues uniques.

Lot 10 : mine et insectes mange-or, wagonnets et ascenseurs, confrontation
avec Akamaru/Aomaru/Kimaru, choix d'achever ou de pardonner, Ma-Djinn et
ses commandes, usine Hanamaru, Shiranui, château des Pièges, château
Fantôme et robe de la Grue, marais rouge du pays de la Grue.
Le glossaire donne les noms provisoires des objets, lieux et titres.
Les 11 entrées différées du bloc 97 restent en anglais, sans modification.

1 462 lectures réussies dans les routines natives 65816, incluant les
chaînes inchangées et les alias. Les 864 anciennes entrées sont identiques
à la V14, en français, mise en page et octets source. 16 contrôles de
police et 14 contrôles du placement passent. Codes de contrôle ordonnés,
pointeurs, alias, checksum, aller-retour IPS et limite de 216 pixels
contrôlés. Les huit lignes de choix d'ascenseur gardent leurs positions
et leur ordre. La séquence de commandes du robot est conservée.

Les neuf nouveaux blocs tiennent dans leurs zones d'origine. Au total :
37 blocs sur place, 13 déplacés ; fin du pool à 0x6B6640. Les 104 896
octets disponibles de V14 restent libres. La ROM d'entrée ne change pas.
Le module de placement actuel reproduit la ROM testée octet pour octet.

Le rapport d'émulation V15 décrit séparément le démarrage et la navigation
observés sous Snes9x 1.63, avec un état propre à chaque ROM et des appuis
de 12 images. Les nouveaux textes et les choix d'ascenseur restent à
observer dans leurs scènes ; les contrôles binaires ne remplacent pas
cette vérification en contexte.

Appliquer le patch V15 directement à la ROM anglaise originale, sans
cumuler les patches. Branche : dev-v12. Aucune ROM ni état d'émulateur
n'est publié.

Résultat Snes9x : autotests A/B ALL OK, 608 commandes de démarrage,
85 captures communes avec V14 identiques pixel par pixel. Le parcours
séparé de navigation ouvre réglages et carte, identiques à V14 ; le
menu principal ne diffère que par l’horloge. Les hashes du rapport
correspondent à la ROM et au patch de cette version.
