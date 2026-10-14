# Tengai Makyou Zero — V10

63 nouvelles entrées, soit 437 entrées intégrées avec la police française.
Les comptes incluent les répétitions et variantes. Les trois séquences de
ponctuation de V09 sont toujours comprises dans le total.

## Nouveau lot

| Bloc | Entrées | Contenu |
|---|---:|---|
| 69 | 13 | Hisui, Subaru, anneau et coffre de l'Éléphant ardent |
| 70 | 4 | Œuf prisonnier de la glace et urgence de la naissance |
| 71 | 29 | Épreuve et transmission de la Flamme éternelle |
| 72 | 17 | Habitants, histoire et lois du village de la Pointe du Feu |

Traduction depuis l'anglais fourni, premier jet à relire. Le script japonais
n'a pas été comparé. Éléphant ardent et Feu primordial sont des termes
provisoires consignés dans le glossaire.

## Installation

Appliquer **Tengai_Makyou_Zero_FR_V10.ips** directement à une copie de la ROM
anglaise originale. Ne pas cumuler les patches des versions précédentes.

Taille : 7 340 032 octets, sans en-tête de copieur.
SHA-256 source : `eb07eed483f8f79ab64309c50ad0ef19560946b8e28fbd695470552ba68e356e`.

Aucune ROM ni sauvegarde d'état n'est incluse.

## Reconstruction et relecture

```bash
python tools/build_v10.py /chemin/rom_anglaise.sfc --rom-out /chemin/v10_fr.sfc
```

Python 3 et Pillow. Le générateur repart de l'original et reconstruit les cinq
lots. La liste bilingue actuelle est `traduction/traduction_v10.json` et `.tsv` ;
`lecture_v10.txt` permet la relecture. Les anciens fichiers restent historiques.

823 lectures par les routines 65816 vérifiées : 437 entrées intégrées,
117 chaînes inchangées du bloc 29 et 269 lectures supplémentaires par les
alias 46/47/48 et 65. Ce compte n'est pas un nombre de scènes testées en jeu.
Les balises, pointeurs de groupes, alias, limites d'allocation, checksum,
préservation des blocs d'origine et reconstruction IPS sont contrôlés.

23 blocs sont déplacés dans la zone 0x6B0000–0x6D0000. Le bloc 70 commence à
0x6BFF00 et franchit la frontière 0x6C0000 : les quatre chaînes sont vérifiées
par les routines natives. L'introduction se trouve désormais à 0x6C1B00.
La nouvelle allocation se termine à 0x6C2700 ; 55 552 octets restent disponibles.

La police demeure celle de V06 (Ÿ/ÿ remplacent Ā/ā). Les 16 contrôles de police
passent, avec une largeur maximale de 216 pixels et préservation du choix Oui/Non.

## Émulation et limites

Le rapport `verification/emulation_report.json` et les captures documentent
le démarrage de cette V10 avec Snes9x 1.63, commit
1bcc369e89f08243e0a462882fb1f3e42e51de3a, puis le début de partie.
Le protocole est A, vérification, reset, B, vérification, reset.
Snes9x 1.60 n'a pas été testé ici.

Les 63 nouveaux dialogues ne sont pas encore observés dans leur contexte de
jeu. Leur contrôle actuel concerne les données et la lecture native, pas une
partie jusqu'à ces scènes. Les menus dessinés, le reste de l'aventure, les
événements PLGS, les sauvegardes SRAM et le matériel réel restent à vérifier.
Les scripts de reproduction sont fournis ; employer les états de la même ROM
et du même noyau, jamais ceux d'une ancienne version.
