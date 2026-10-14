# Tengai Makyou Zero — Traduction française V13

**161 nouveaux textes**, soit **730 entrées intégrées avec accents**.
Le lot traite 162 entrées : 161 textes et une entrée vide conservée (93/41).
Les 568 anciennes entrées sont identiques à la V12, y compris leur mise
en page. Les variantes, répétitions et séquences de ponctuation sont
comptées séparément ; le total n'est pas un nombre de dialogues uniques.

## Lot 08

| Bloc | Entrées traitées | Contenu |
|---|---:|---|
| 75 | 59 | Kingin, Super Money-King III, combat de robots |
| 89 | 4 | Cascade du Djinn, direction du royaume du Dragon |
| 90 | 7 | Légende du Ma-Djinn et pierre du Chien divin |
| 93 | 92 | Habitants, journal Le Chien, maison de Yone, Shigenobu et Rie |

Les deux colonnes des articles du journal sont conservées sans repli
automatique : leur seconde colonne reste à un pixel près de la position
anglaise. Cette mesure ne remplace pas une observation du menu en contexte.

Premier jet depuis l'anglais fourni, sans comparaison avec le script japonais.
Le glossaire indique les noms d'objets et lieux encore provisoires.

## Installation

Appliquer **Tengai_Makyou_Zero_FR_V13.ips** directement à une copie de la ROM
anglaise originale, sans cumuler les versions. Le patch V12 reste disponible
pour revenir à la version précédente.

- Taille source : 7 340 032 octets, sans en-tête de copieur.
- SHA-256 source : `eb07eed483f8f79ab64309c50ad0ef19560946b8e28fbd695470552ba68e356e`.

Le dépôt ne contient ni ROM ni sauvegarde d'état.

## Construction et relecture

```bash
python tools/build_v13.py /chemin/rom_anglaise.sfc --rom-out /chemin/v13_fr.sfc
python tools/verify_font.py /chemin/rom_anglaise.sfc
```

Python 3 ; Pillow pour les contrôles de police. Le générateur repart toujours
de l'original. Les huit lots JSON sont les sources de traduction. Le générateur crée les fichiers
`traduction/traduction_v13.json`, `.tsv` et `lecture_v13.txt` localement pour
la relecture bilingue. Les lots JSON versionnés suffisent à les reconstruire.
Les résultats des versions précédentes et les anciens générateurs sont historiques.

1 143 lectures 65816 vérifiées : les textes intégrés, les chaînes
inchangées du bloc des choix et leurs alias. Ce compte ne représente pas
des scènes observées en partie. 36 blocs physiques sont relocalisés
dans la zone autorisée.

Police française inchangée depuis V06 : 32 lettres accentuées et quatre
ligatures ; Ÿ/ÿ remplacent Ā/ā. Les 16 contrôles de police passent. La largeur
maximale est de 216 pixels, avec une réserve de 96 pixels pour les substitutions
dynamiques et conservation de la disposition du choix Oui/Non.

## Émulation

Snes9x 1.63, commit 1bcc369e89f08243e0a462882fb1f3e42e51de3a.
Source du noyau : https://github.com/snes9xgit/snes9x
La version 1.60 n'est pas testée ici.

Le protocole de démarrage est A, vérification, reset, B, vérification, reset.
Le parcours de test repart d'un démarrage neuf : autotests A/B, resets,
introduction et début de partie jusqu'aux menus et à la carte. Les résultats
V13 sont consignés dans verification/emulation_report_v13.json : autotests
ALL OK, 608 commandes, 85 captures communes identiques pixel par pixel
à la V12. Les nouveaux
textes restent à vérifier dans leurs scènes ; les menus dessinés, la suite
de l'aventure, les fêtes PLGS, la SRAM et le matériel réel restent à vérifier.

Les scripts `verification/reproduction` utilisent NumPy et Pillow.
Ils reproduisent le démarrage, la navigation et les choix de dialogues.
Créer les états avec la même ROM et le même noyau ; ne pas reprendre les états
d'une version antérieure. Les historiques complets et résultats bilingues
peuvent être régénérés localement. Aucun dump mémoire complet n'est publié.

## Vérifications V13

1 143 lectures exécutées par les routines natives 65816, 16 contrôles de
police, balises ordonnées, pointeurs et alias, reconstruction IPS et limite
de 216 pixels contrôlés. Allocation jusqu'à 0x6CD500 : 11 008 octets libres.
Le fichier verification/build_report.json concerne la V13.

Les rapports regression_v12_v13.json et choice_layout_v13.json documentent
la préservation des anciennes entrées et la géométrie des articles.
La commande 0E reste conservée, sans réinterprétation de son effet.
Les anciens rapports restent des preuves de leur propre version.
