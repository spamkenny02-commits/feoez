# Tengai Makyou Zero — Traduction française V15

**146 nouveaux textes modifiés**, dans **149 entrées traitées** ;
**1 013 entrées intégrées avec accents** au total.
Les 864 anciennes entrées sont identiques à la V14, mise en page comprise.
Les trois répliques neutres Hmm... / ??? / ??? sont conservées ;
les variantes, répétitions et entrées neutres sont incluses dans le total.

## Lot 10

| Bloc | Entrées traitées | Contenu |
|---|---:|---|
| 106 | 34 | Mine, ascenseurs, insectes mange-or |
| 107 | 25 | Mine, contrôle, wagonnets et lingots |
| 108 | 37 | Trio Akamaru, cœur du Chien divin, pardon |
| 109 | 8 | Pilotage et combat du Ma-Djinn |
| 110 | 9 | Usine et clonage Hanamaru |
| 111 | 7 | Shiranui et Sabreur des Ténèbres |
| 112 | 14 | Château des Pièges, règles et récompenses |
| 113 (alias 114) | 12 | Château Fantôme et robe de la Grue |
| 115 (alias 116) | 3 | Marais rouge et pays de la Grue |

Les huit lignes de choix d'ascenseur gardent leur ordre et leurs positions.
N1/N2/N3 désignent les niveaux ; S1/S2 les sous-sols. Le tutoriel du
Ma-Djinn garde les boutons A/B et la séquence X, bas, bas-droite, droite, A.

Onze textes du bloc 97 restent en anglais : 23–28, 58, 98, 104, 107, 109.
Leurs commandes 05/0A restent exclues de l'édition et leurs octets conservés.

Premier jet depuis l'anglais fourni, sans comparaison avec le script japonais.
Le glossaire indique les noms d'objets et lieux encore provisoires.

## Installation

Appliquer **Tengai_Makyou_Zero_FR_V15.ips** directement à une copie de la ROM
anglaise originale, sans cumuler les versions. Le patch V14 reste disponible
pour revenir à la version précédente.

- Taille source : 7 340 032 octets, sans en-tête de copieur.
- SHA-256 source : `eb07eed483f8f79ab64309c50ad0ef19560946b8e28fbd695470552ba68e356e`.

Le dépôt ne contient ni ROM ni sauvegarde d'état.

## Construction et relecture

```bash
python tools/build_v15.py /chemin/rom_anglaise.sfc --rom-out /chemin/v15_fr.sfc
python tools/verify_font.py /chemin/rom_anglaise.sfc
```

Python 3 ; Pillow pour les contrôles de police. Le générateur repart toujours
de l'original. Les dix lots JSON sont les sources de traduction. Le générateur crée les fichiers
`traduction/traduction_v15.json`, `.tsv` et `lecture_v15.txt` localement pour
la relecture bilingue. Les lots JSON versionnés suffisent à les reconstruire.
Les résultats des versions précédentes et les anciens générateurs sont historiques.

1 462 lectures dans les routines natives passent. Le placement utilise
37 blocs sur place et 13 déplacés ; 104 896 octets restent libres. Les
blocs sur place remplacent les textes anglais dans la ROM de sortie ;
le fichier anglais d'entrée n'est jamais modifié.

```bash
python tools/verify_storage.py /chemin/rom_anglaise.sfc --version V15 --built-rom /chemin/v15_fr.sfc --build-report verification/build_report.json
```

Police française inchangée depuis V06 : 32 lettres accentuées et quatre
ligatures ; Ÿ/ÿ remplacent Ā/ā. Les 16 contrôles de police passent. La largeur
maximale est de 216 pixels, avec une réserve de 96 pixels pour les substitutions
dynamiques et conservation de la disposition du choix Oui/Non.

## Émulation

Snes9x 1.63, commit 1bcc369e89f08243e0a462882fb1f3e42e51de3a.
Source du noyau : https://github.com/snes9xgit/snes9x
La version 1.60 n'est pas testée ici.

Le protocole de démarrage est A, vérification, reset, B, vérification, reset.
Le parcours repart d'un démarrage neuf avec autotests A/B et resets,
puis introduction et début de partie. Le scénario run_navigation.py
utilise des appuis de 12 images pour ouvrir les menus, les réglages et
la carte. Le rapport V15 lie le patch et la ROM testée à ces observations.
Autotests A/B ALL OK ; les 85 captures du parcours commun sont identiques
à V14. Réglages et carte restent identiques ; le menu principal ne diffère
que par l’horloge. Les 146 nouveaux textes restent à vérifier dans leurs scènes.
Voir verification/emulation_report_v15.json.

Les scripts `verification/reproduction` utilisent NumPy et Pillow.
Ils reproduisent le démarrage, la navigation et les choix de dialogues.
Créer les états avec la même ROM et le même noyau ; ne pas reprendre les états
d'une version antérieure. Les historiques complets et résultats bilingues
peuvent être régénérés localement. Aucun dump mémoire complet n'est publié.

## Vérifications V15

1 462 lectures 65816, 16 contrôles de police et 14 contrôles du placement
réussis. Balises, pointeurs, alias, largeur de 216 pixels et IPS contrôlés.
Tous les nouveaux blocs tiennent sur place. L'espace libre reste de
104 896 octets : aucun ajout dans le pool de relocalisation depuis V14.
Le rapport courant build_report.json concerne la V15.
regression_v14_v15.json documente les 864 anciennes entrées préservées ;
elevator_layout_v15.json documente la disposition des choix.
Les anciens rapports restent des preuves de leurs propres versions.
