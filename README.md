# Tengai Makyou Zero — Traduction française V14

**134 nouveaux textes**, soit **864 entrées intégrées avec accents**.
Les 730 anciennes entrées sont identiques à la V13, mise en page comprise.
Le total inclut variantes, répétitions, ponctuation et l'entrée vide conservée
du journal ; ce n'est pas un nombre de dialogues uniques.

## Lot 09

| Bloc | Textes ajoutés | Contenu |
|---|---:|---|
| 97 | 98 | Arcade, boutiques et habitants du Cercle Fleuri |
| 98 | 5 | Générateur et horaires des néons |
| 100 | 18 | Ermite des Insignes, parchemins et cadeaux |
| 101 | 8 | Ermite Pauvre, cœur du Chien divin |
| 103 (alias 104/105) | 5 | Cascade, emblème et bouton |

Onze textes du bloc 97 restent en anglais : 23–28, 58, 98, 104, 107, 109.
Leurs variables 05 et effets 0A ne sont pas encore pris en charge pour
l'édition ; leurs octets sont conservés après reconstruction.

Premier jet depuis l'anglais fourni, sans comparaison avec le script japonais.
Le glossaire indique les noms d'objets et lieux encore provisoires.

## Installation

Appliquer **Tengai_Makyou_Zero_FR_V14.ips** directement à une copie de la ROM
anglaise originale, sans cumuler les versions. Le patch V13 reste disponible
pour revenir à la version précédente.

- Taille source : 7 340 032 octets, sans en-tête de copieur.
- SHA-256 source : `eb07eed483f8f79ab64309c50ad0ef19560946b8e28fbd695470552ba68e356e`.

Le dépôt ne contient ni ROM ni sauvegarde d'état.

## Construction et relecture

```bash
python tools/build_v14.py /chemin/rom_anglaise.sfc --rom-out /chemin/v14_fr.sfc
python tools/verify_font.py /chemin/rom_anglaise.sfc
```

Python 3 ; Pillow pour les contrôles de police. Le générateur repart toujours
de l'original. Les neuf lots JSON sont les sources de traduction. Le générateur crée les fichiers
`traduction/traduction_v14.json`, `.tsv` et `lecture_v14.txt` localement pour
la relecture bilingue. Les lots JSON versionnés suffisent à les reconstruire.
Les résultats des versions précédentes et les anciens générateurs sont historiques.

1 298 lectures dans les routines natives passent. Le placement utilise
28 blocs sur place et 13 déplacés ; 104 896 octets restent libres. Les
blocs sur place remplacent les textes anglais dans la ROM de sortie ;
le fichier anglais d'entrée n'est jamais modifié.

```bash
python tools/verify_storage.py /chemin/rom_anglaise.sfc --built-rom /chemin/v14_fr.sfc --build-report verification/build_report.json
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
Autotests A/B ALL OK, introduction et début de partie vérifiés.
Le scénario ancien à appuis d'une image atteint certains écrans à des
moments différents : 67 captures identiques, 18 différentes.
Le nouveau run_navigation.py utilise des appuis de 12 images : les
réglages et la carte V13/V14 sont identiques, et le menu principal ne
diffère que par l'horloge. Les nouveaux textes restent à observer dans
leurs scènes de progression. Voir verification/emulation_report_v14.json.

Les scripts `verification/reproduction` utilisent NumPy et Pillow.
Ils reproduisent le démarrage, la navigation et les choix de dialogues.
Créer les états avec la même ROM et le même noyau ; ne pas reprendre les états
d'une version antérieure. Les historiques complets et résultats bilingues
peuvent être régénérés localement. Aucun dump mémoire complet n'est publié.

## Vérifications V14

1 298 lectures 65816, 16 contrôles de police et 14 contrôles de placement
réussis. Balises, pointeurs, alias, largeur de 216 pixels et IPS contrôlés.
Le rapport courant build_report.json concerne la V14. La comparaison
regression_v13_v14.json confirme les 730 anciennes entrées préservées.
Les anciens rapports restent des preuves de leurs propres versions.
