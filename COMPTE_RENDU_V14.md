# Compte rendu V14

134 nouveaux textes intégrés, 864 entrées au total. Bloc 97 : 98 textes
d'arcade, boutiques et habitants ; bloc 98 : 5 textes du générateur ;
bloc 100 : 18 textes de l'ermite des Insignes ; bloc 101 : 8 textes
de l'ermite Pauvre ; bloc 103 (alias 104/105) : 5 textes de la cascade.
Les 11 autres entrées du bloc 97 sont laissées en anglais et préservées
octet pour octet : variables 05 et effets 0A encore exclus de l'éditeur.
Le glossaire documente les noms provisoires et la contradiction source
entre récompense annoncée et popup dans B097-S102.

La zone libre V13 ne contenait plus que 11 008 octets. Nouveau placement :
les blocs reconstruits qui tiennent dans leur ancienne zone sont écrits
sur place ; seuls les blocs trop longs sont relocalisés. 28 blocs sur
place, 13 déplacés, alignement de 16 octets, fin à 0x6B6640.
Il reste 104 896 octets libres. Le fichier anglais d'entrée reste intact ;
les anciens textes sont remplacés dans la ROM de sortie pour les blocs
écrits sur place. Les sources anglaises des blocs déplacés restent intactes.

1 298 lectures passent dans les routines natives 65816 : tous les textes,
les chaînes inchangées et leurs alias. Les 730 anciennes traductions
sont identiques à la V13, mise en page comprise. 16 contrôles de police
et 14 contrôles du placement passent, dont refus des chevauchements,
des alias manquants, d'une zone occupée et du dépassement de capacité.
La reconstruction avec le module actuel reproduit la ROM testée octet
pour octet. Balises, pointeurs, largeur de 216 pixels et aller-retour IPS
sont contrôlés. Les codes bas autorisés restent ceux de la V13.

Snes9x 1.63 : autotests A/B ALL OK, resets, introduction et début de partie.
La comparaison du scénario ancien trouve 67 captures identiques sur 85 ;
18 captures tardives montrent des états de navigation différents.
Ce scénario à appuis d'une image ne constitue pas une comparaison
alignée de ces écrans. Un nouveau parcours à appuis de 12 images
ouvre les mêmes menus, réglages et carte dans V13 et V14. Réglages et
carte sont identiques ; le menu principal ne diffère que par l'horloge.
Les nouveaux dialogues restent à observer dans leurs scènes.

Appliquer V14 directement à la ROM anglaise originale, sans cumul.
Branche : dev-v12. Aucune ROM ni sauvegarde d'état n'est publiée.
