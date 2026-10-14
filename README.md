# Tengai Makyou Zero — Traduction française V12

**66 nouvelles entrées**, soit **568 entrées intégrées avec accents**.
Les 502 entrées de V11 sont conservées à l'identique, y compris leur mise
en page. Les variantes et répétitions sont comptées séparément. Le total
inclut les trois séquences de ponctuation inchangées de V09.

## Lot 07

| Bloc | Entrées traduites | Contenu |
|---|---:|---|
| 77 (alias 78) | 25 | Village des Paillettes d'Or, orpaillage |
| 81 (alias 82) | 2 | Bouton du château |
| 83 | 24 | Kingin, Goldsilver et fuite du château |
| 87 | 15 | Sanctuaire du Chien divin, habitants et fêtes |

Les alias désignent le même bloc physique ; ils ne sont pas comptés comme
des traductions supplémentaires.

Premier jet depuis l'anglais fourni, sans comparaison avec le script japonais.
Le glossaire indique les noms d'objets et lieux encore provisoires.

## Installation

Appliquer **Tengai_Makyou_Zero_FR_V12.ips** directement à une copie de la ROM
anglaise originale, sans cumuler les versions. Le patch V11 reste disponible
pour revenir à la version précédente.

- Taille source : 7 340 032 octets, sans en-tête de copieur.
- SHA-256 source : `eb07eed483f8f79ab64309c50ad0ef19560946b8e28fbd695470552ba68e356e`.

Le dépôt ne contient ni ROM ni sauvegarde d'état.

## Construction et relecture

```bash
python tools/build_v12.py /chemin/rom_anglaise.sfc --rom-out /chemin/v12_fr.sfc
python tools/verify_font.py /chemin/rom_anglaise.sfc
```

Python 3 ; Pillow pour les contrôles de police. Le générateur repart toujours
de l'original. Les sept lots JSON sont les sources de traduction. Le générateur crée les fichiers
`traduction/traduction_v12.json`, `.tsv` et `lecture_v12.txt` localement pour
la relecture bilingue. Les lots JSON versionnés suffisent à les reconstruire.
Les résultats des versions précédentes et les anciens générateurs sont historiques.

981 lectures 65816 vérifiées : 568 entrées traduites et 413 lectures
supplémentaires pour les chaînes inchangées et les alias. Ce compte ne
représente pas des scènes observées en partie. 32 blocs physiques sont
relocalisés dans la zone autorisée.

Police française inchangée depuis V06 : 32 lettres accentuées et quatre
ligatures ; Ÿ/ÿ remplacent Ā/ā. Les 16 contrôles de police passent. La largeur
maximale est de 216 pixels, avec une réserve de 96 pixels pour les substitutions
dynamiques et conservation de la disposition du choix Oui/Non.

## Émulation

Snes9x 1.63, commit 1bcc369e89f08243e0a462882fb1f3e42e51de3a.
Source du noyau : https://github.com/snes9xgit/snes9x
La version 1.60 n'est pas testée ici.

Le protocole de démarrage est A, vérification, reset, B, vérification, reset.
La V12 démarre à neuf ; les deux autotests affichent ALL OK. Le parcours
va jusqu'au début de partie, aux menus et à la carte. 85 captures communes
avec la V11 sont identiques pixel par pixel. Les 66 nouvelles entrées
restent à vérifier dans leurs scènes. Les menus dessinés, la suite de
l'aventure, les fêtes PLGS, la SRAM et le matériel réel restent à vérifier.

Les scripts `verification/reproduction` utilisent NumPy et Pillow.
Ils reproduisent le démarrage, la navigation et les choix de dialogues.
Créer les états avec la même ROM et le même noyau ; ne pas reprendre les états
d'une version antérieure. Les historiques complets et résultats bilingues
peuvent être régénérés localement. Aucun dump mémoire complet n'est publié.

## Vérifications V12

981 lectures exécutées par les routines natives 65816, 16 contrôles de
police, balises ordonnées, pointeurs et alias, reconstruction IPS et limite
de 216 pixels contrôlés. Allocation jusqu'à 0x6C7B00 : 34 048 octets libres.
Le fichier verification/build_report.json concerne la V12.

Le rapport verification/emulation_report_v12.json décrit uniquement le
parcours observé dans Snes9x 1.63. Les nouvelles scènes restent à vérifier
visuellement dans leur contexte. Les anciens rapports restent des preuves
de leur propre version, et non de la V12.
