# Tengai Makyou Zero — Traduction française V17

**103 nouvelles entrées**, soit **1 183 intégrées avec accents**.
Les 1 080 anciennes entrées sont conservées, mise en page et octets source compris.
Les variantes, répétitions et réponses neutres sont comptées séparément.

## Lot 12

Habitants et commerces du pays de la Grue, village des Algues,
galerie du Trésor et descriptions des objets exposés ; ermite Pétillant
et son sort Vitalité. Six blocs : 124 à 129.

La chanson B125-S003 reste en anglais : sa commande d'effet 0A/CC
n'est pas prise en charge pour l'édition. Ses octets sont conservés et
relus avec les routines originales après reconstruction. Les onze
messages à commandes 05/0A du bloc 97 restent également en anglais.
Premier jet depuis l'anglais fourni, sans comparaison avec le script japonais.
Les noms provisoires et adaptations de jeux de mots figurent au glossaire.
Les prix de 50/70/200/2 000 ryo et les horaires de l'exposition sont conservés.

## Installation

Appliquer **Tengai_Makyou_Zero_FR_V17.ips** directement à une copie de la ROM
anglaise originale, sans cumuler les versions. Le patch V16 reste disponible
pour revenir à la version précédente.

- Taille source : 7 340 032 octets, sans en-tête de copieur.
- SHA-256 source : `eb07eed483f8f79ab64309c50ad0ef19560946b8e28fbd695470552ba68e356e`.

Le dépôt ne contient ni ROM ni sauvegarde d'état.

## Construction et relecture

```bash
python tools/build_v17.py /chemin/rom_anglaise.sfc --rom-out /chemin/v17_fr.sfc
python tools/verify_font.py /chemin/rom_anglaise.sfc
```

Python 3 ; Pillow pour les contrôles de police. Le générateur repart toujours
de l'original. Les douze lots JSON sont les sources de traduction. Le générateur crée les fichiers
`traduction/traduction_v17.json`, `.tsv` et `lecture_v17.txt` localement pour
la relecture bilingue. Les lots JSON versionnés suffisent à les reconstruire.
Les résultats des versions précédentes et les anciens générateurs sont historiques.

1 638 lectures dans les routines natives passent. Le placement utilise
43 blocs sur place et 19 déplacés ; 95 648 octets restent libres. Les
blocs sur place remplacent les textes anglais dans la ROM de sortie ;
le fichier anglais d'entrée n'est jamais modifié.

```bash
python tools/verify_storage.py /chemin/rom_anglaise.sfc --version V17 --built-rom /chemin/v17_fr.sfc --build-report verification/build_report.json
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
la carte. Le rapport V17 lie le patch et la ROM testée à ces observations.
Autotests A/B ALL OK ; les 85 captures du parcours commun sont identiques
à V16. Réglages et carte restent identiques ; le menu principal ne diffère
que par l’horloge. Les 103 nouveaux textes restent à vérifier dans leurs scènes.
Voir verification/emulation_report_v17.json.

Les scripts `verification/reproduction` utilisent NumPy et Pillow.
Ils reproduisent le démarrage, la navigation et les choix de dialogues.
Créer les états avec la même ROM et le même noyau ; ne pas reprendre les états
d'une version antérieure. Les historiques complets et résultats bilingues
peuvent être régénérés localement. Aucun dump mémoire complet n'est publié.

## Vérifications V17

1 638 lectures 65816, 16 contrôles de police et 14 contrôles du placement
réussis. Balises, pointeurs, alias, largeur de 216 pixels et IPS contrôlés.
Quatre nouveaux blocs tiennent sur place, deux sont relocalisés.
Il reste 95 648 octets dans le pool de relocalisation.
Le rapport courant build_report.json concerne la V17.
regression_v16_v17.json documente les 1 080 anciennes entrées préservées ;
Les choix des lots antérieurs conservent leur mise en page.
Les anciens rapports restent des preuves de leurs propres versions.
