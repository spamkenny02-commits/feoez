# Tengai Makyou Zero — Traduction française V19

**112 entrées ajoutées**, dont **111 textes modifiés** ;
**1 381 entrées intégrées avec accents** au total.
Les 1 269 anciennes entrées sont conservées, mise en page et octets source compris.
Les variantes, répétitions et réponses neutres sont comptées séparément.

## Lot 14

Grue divine et pierre de la Grue, village du Saké avant et après sa
libération, boutiques et production du saké, grotte du Clapotis et Omine.
Cinq blocs : 136, 137, 138, 139 et 141, ce dernier partagé avec 142.
Les deux références de la grotte reçoivent la même traduction.
B141-S015 (« !!! ») est conservée sans modification.

Les tarifs de 90/1 000/5 000 ryo, les cinq secondes de la poche d'air,
les 20 pour cent de remise de 17 h à 20 h et le symbole 14 sont conservés.
L'eau de vie de la fontaine et le Saké de vie sont deux noms distincts.
Les treize entrées différées et les blocs 132/140 restent en anglais,
avec leurs octets conservés.
Premier jet depuis l'anglais fourni, sans comparaison avec le script japonais.
Noms provisoires et adaptations consignés au glossaire.

## Installation

Appliquer **Tengai_Makyou_Zero_FR_V19.ips** directement à une copie de la ROM
anglaise originale, sans cumuler les versions. Le patch V18 reste disponible
pour revenir à la version précédente.

- Taille source : 7 340 032 octets, sans en-tête de copieur.
- SHA-256 source : `eb07eed483f8f79ab64309c50ad0ef19560946b8e28fbd695470552ba68e356e`.

Le dépôt ne contient ni ROM ni sauvegarde d'état.

## Construction et relecture

```bash
python tools/build_v19.py /chemin/rom_anglaise.sfc --rom-out /chemin/v19_fr.sfc
python tools/verify_font.py /chemin/rom_anglaise.sfc
```

Python 3 ; Pillow pour les contrôles de police. Le générateur repart toujours
de l'original. Les quatorze lots JSON sont les sources de traduction. Le générateur crée les fichiers
`traduction/traduction_v19.json`, `.tsv` et `lecture_v19.txt` localement pour
la relecture bilingue. Les lots JSON versionnés suffisent à les reconstruire.
Les résultats des versions précédentes et les anciens générateurs sont historiques.

1 858 lectures dans les routines natives passent. Le placement utilise
53 blocs sur place et 19 déplacés ; 95 648 octets restent libres. Les
blocs sur place remplacent les textes anglais dans la ROM de sortie ;
le fichier anglais d'entrée n'est jamais modifié.

```bash
python tools/verify_storage.py /chemin/rom_anglaise.sfc --version V19 --built-rom /chemin/v19_fr.sfc --build-report verification/build_report.json
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
la carte. Le rapport V19 lie le patch et la ROM testée à ces observations.
Autotests A/B ALL OK ; les 85 captures du parcours commun sont identiques
à V18. Le menu principal, les réglages et la carte sont également identiques. Les 111 nouveaux textes restent à vérifier dans leurs scènes.
Voir verification/emulation_report_v19.json.

Les scripts `verification/reproduction` utilisent NumPy et Pillow.
Ils reproduisent le démarrage, la navigation et les choix de dialogues.
Créer les états avec la même ROM et le même noyau ; ne pas reprendre les états
d'une version antérieure. Les historiques complets et résultats bilingues
peuvent être régénérés localement. Aucun dump mémoire complet n'est publié.

## Vérifications V19

1 858 lectures 65816, 16 contrôles de police et 14 contrôles du placement
réussis. Balises, pointeurs, alias, largeur de 216 pixels et IPS contrôlés.
Les cinq nouveaux blocs tiennent à leur emplacement d’origine.
Il reste 95 648 octets dans le pool de relocalisation.
Le rapport courant build_report.json concerne la V19.
regression_v18_v19.json documente les 1 269 anciennes entrées préservées ;
Les choix des lots antérieurs conservent leur mise en page.
Les anciens rapports restent des preuves de leurs propres versions.
