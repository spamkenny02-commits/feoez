# Compte rendu V13

161 nouveaux textes traduits dans 162 entrées traitées. L'entrée vide du
journal B093-S041 est conservée. Le total reconstruit passe de 568 à 730 ;
il inclut les variantes, répétitions et la ponctuation déjà documentée.

Blocs 75 (59), 89 (4), 90 (7), 93 (92) : Super Money-King III et les sept
secrets de Kingin, légende de la cascade du Djinn, habitants et journal
satirique du pays du Chien, achat de la maison de Yone, Shigenobu et Rie.
Noms provisoires et choix d'adaptation consignés dans le glossaire.

1 143 lectures dans les routines natives 65816 passent, ainsi que les
16 contrôles de police. Codes de contrôle et substitutions conservés ;
aucun nouveau code bas n'est autorisé par rapport à la V12. Largeur
maximale : 216 pixels. Les deux colonnes des articles du journal gardent
leur disposition, avec un écart mesuré d'un pixel au plus par rapport
à l'anglais. Le prompt est replié indépendamment des libellés de choix.

Les 568 anciennes entrées sont identiques à la V12 : texte français,
texte mis en page et octets source. Les anciens blocs anglais restent
intacts ; le patch IPS reconstruit exactement la ROM testée.
36 blocs physiques relocalisés ; allocation jusqu'à 0x6CD500 ;
11 008 octets disponibles dans la zone autorisée.

Snes9x 1.63 : démarrage neuf, autotests A/B ALL OK, resets et début de
partie jusqu'aux dialogues, menus et carte. 608 commandes reproduites ;
les 85 captures communes avec le parcours V12 sont identiques pixel par pixel.
Le rapport associe les hashes de la ROM et du patch à ce parcours. Les nouveaux textes et le choix des articles attendent une
vérification visuelle dans leurs scènes. Ni les lectures du probe ni
la mesure des colonnes ne constituent cette validation en contexte.

Appliquer le patch V13 directement à la ROM anglaise originale.
Ne pas cumuler les versions. Branche : dev-v12.
Aucun fichier ROM ni état d'émulateur n'est publié.
