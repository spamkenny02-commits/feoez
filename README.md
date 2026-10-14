# Tengai Makyou Zero — Traduction française V11

**65 nouvelles entrées**, soit **502 entrées intégrées avec accents**.
Les 437 entrées de V10 sont conservées. Les comptes incluent les répétitions
et variantes ainsi que les trois séquences de ponctuation inchangées de V09.

## Lot 06

| Bloc | Entrées | Contenu |
|---|---:|---|
| 74 | 19 | Épée de Byakuen, sanctuaire et Ours de Feu divin |
| 76 | 4 | Château d'Or et utilisation des chaînes |
| 79 | 15 | Mine, sac à or, insigne et robot d'entrée |
| 84 | 16 | Sanctuaire du Chien divin, histoire et fêtes |
| 85 | 11 | Chien divin, Kingin/Byakko et pierre divine |

Premier jet depuis l'anglais fourni, sans comparaison avec le script japonais.
Le glossaire indique les noms d'objets et lieux encore provisoires.

## Installation

Appliquer **Tengai_Makyou_Zero_FR_V11.ips** directement à une copie de la ROM
anglaise originale, sans cumuler les versions. Le patch V10 reste disponible
pour revenir à la version précédente.

- Taille source : 7 340 032 octets, sans en-tête de copieur.
- SHA-256 source : `eb07eed483f8f79ab64309c50ad0ef19560946b8e28fbd695470552ba68e356e`.

Le dépôt ne contient ni ROM ni sauvegarde d'état.

## Construction et relecture

```bash
python tools/build_v11.py /chemin/rom_anglaise.sfc --rom-out /chemin/v11_fr.sfc
python tools/verify_font.py /chemin/rom_anglaise.sfc
```

Python 3 ; Pillow pour les contrôles de police. Le générateur repart toujours
de l'original. Les six lots JSON sont les sources de traduction. Les fichiers
`traduction/traduction_v11.json`, `.tsv` et `lecture_v11.txt` sont les résultats
bilingues actuels. Les résultats V10 et les anciens générateurs sont historiques.

888 lectures 65816 vérifiées : 502 entrées intégrées, 117 chaînes inchangées
du bloc 29 et 269 lectures supplémentaires par les alias 46/47/48 et 65.
Ce compte ne représente pas 888 scènes observées en partie.

La construction vérifie les balises, pointeurs de groupes, alias, limites
mémoire, préservation des blocs d'origine, checksum et aller-retour IPS.
28 blocs sont relocalisés dans la zone 0x6B0000–0x6D0000 ; l'allocation se termine
à 0x6C5A00, laissant 42 496 octets. Le bloc 70 traverse la frontière 0x6C0000 et
sa lecture reste contrôlée par les routines natives. L'introduction a été
relocalisée à 0x6C4E00. Aucune extension de la ROM n'est nécessaire pour ce lot.

Police française inchangée depuis V06 : 32 lettres accentuées et quatre
ligatures ; Ÿ/ÿ remplacent Ā/ā. Les 16 contrôles de police passent. La largeur
maximale est de 216 pixels, avec une réserve de 96 pixels pour les substitutions
dynamiques et conservation de la disposition du choix Oui/Non.

## Émulation

Snes9x 1.63, commit 1bcc369e89f08243e0a462882fb1f3e42e51de3a.
Source du noyau : https://github.com/snes9xgit/snes9x
La version 1.60 n'est pas testée ici.

Le protocole de démarrage est A, vérification, reset, B, vérification, reset.
La V11 est démarrée à neuf ; son introduction et le début de partie sont
observés. Le rapport et la capture figurent dans `verification`.
Les 65 nouvelles entrées ne sont pas encore vérifiées visuellement dans leurs
scènes. Les contrôles de lecture et de mise en page sont distincts de cette
validation en contexte. Les menus dessinés, la suite de l'aventure, les fêtes
PLGS, la SRAM et le matériel réel restent à vérifier.

Les scripts `verification/reproduction` utilisent NumPy et Pillow.
Ils reproduisent le démarrage, la navigation et les choix de dialogues.
Créer les états avec la même ROM et le même noyau ; ne pas reprendre les états
d'une version antérieure. Les historiques complets et résultats bilingues
peuvent être régénérés localement. Aucun dump mémoire complet n'est publié.
