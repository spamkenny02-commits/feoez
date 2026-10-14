# Tengai Makyou Zero — Traduction française V24

122 nouvelles entrées, **1 841 intégrées avec accents**. Habitants et soldats du
royaume du Dragon, nouveaux ermites, anneau de l'Âme et village du Katana.
Les 1 719 entrées de V23 sont inchangées. Variantes et répétitions sont comptées
séparément. Premier jet depuis l'anglais fourni ; noms provisoires au glossaire.

L'indice de trésor garde un texte codé adapté au français. Vivacité, Esprit et
Âme conservent les restrictions décrites dans les dialogues. Les nuits à 180,
100 et 250 ryo et les directions restent conformes au script.
18 messages différés et le bloc 132 restent inchangés en anglais.

## Installation

Appliquer **Tengai_Makyou_Zero_FR_V24.ips** directement à une copie de la ROM
anglaise originale, sans cumuler les versions.

- Taille source : 7 340 032 octets, sans en-tête de copieur.
- SHA-256 : `eb07eed483f8f79ab64309c50ad0ef19560946b8e28fbd695470552ba68e356e`.

Le dépôt ne contient ni ROM, ni sauvegarde d'état, ni noyau binaire d'émulateur.

## Construction

```bash
python tools/build_v24.py /chemin/original.sfc --rom-out /chemin/v24.sfc
python tools/verify_font.py /chemin/original.sfc
python tools/verify_storage.py /chemin/original.sfc --version V24 --built-rom /chemin/v24.sfc --build-report verification/build_report.json
```

Python 3 et Pillow. Les dix-neuf lots JSON et corrections_v20.json sont les sources.
Le générateur produit les fichiers bilingues JSON/TSV et lecture_v24.txt localement.
2 339 lectures dans les routines originales 65816 passent, avec les chaînes
inchangées et les alias. Balises, largeur maximale de 216 pixels, pointeurs,
checksum, encodage et aller-retour IPS sont contrôlés. Les 16 contrôles de police
et 14 contrôles du placement passent. 69 blocs sur place, 26 relocalisés,
87 904 octets libres ; le fichier anglais d'entrée n'est pas modifié.

## Essais dans Snes9x

Noyau standard Snes9x 1.63, commit 1bcc369e89f08243e0a462882fb1f3e42e51de3a.
Démarrage neuf et parcours du début. Contrôles A puis reset puis B prolongé
à 60 000 images : COMPLETE / ALL OK (scenario_checks_v24.json).
Les 85 captures communes avec V23 sont identiques. Menus et carte accessibles.
La version 1.60, le jeu complet et le matériel réel ne sont pas testés ici.

Quinze essais ciblés contrôlent les nouveaux dialogues à l'écran : auberges à
180 et 250 ryo, indice codé, duel de Byakuen, refus de Dejima, père d'Higan,
cœur, Vivacité, Esprit, récit des flammes, anneau et résurrection Âme, ermite
des Cieux, Gaen et entrée en feu.
Ils utilisent la ROM finale inchangée et un noyau de diagnostic séparé qui
redirige une seule demande de dialogue vers le bloc et le message testés.
Les routines de lookup, sélection, lecture et rendu restent celles du jeu.
Le curseur doit atteindre le terminateur exact, puis les captures sont relues.

**Ces essais valident les textes et leur pagination, pas la progression naturelle,
la cache du trésor, les prix réellement débités, les effets des parchemins,
le combat de Gaen ou l'accès aux bâtiments en feu.** Les arrière-plans appartiennent au banc de test.
Rapport et images : verification/scenes_v24.

## Reproduire les essais ciblés

Compiler le noyau standard depuis https://github.com/snes9xgit/snes9x au commit
ci-dessus. NumPy et Pillow sont nécessaires pour le frontend. Le constructeur
de diagnostic restaure le code source et le noyau standard après compilation.

```bash
python verification/reproduction/build_diagnostic_core.py --source /chemin/snes9x --out /chemin/diagnostic.so
python verification/reproduction/prepare_dialogue_state.py --core /chemin/standard.so --rom /chemin/v24.sfc --out /chemin/etat_v24
python verification/reproduction/run_targeted_dialogues.py --core /chemin/diagnostic.so --rom /chemin/v24.sfc --state /chemin/etat_v24/dialogue_entry.state --out /chemin/essais_v24 --cases verification/reproduction/cases_v24.json
```

Créer l'état avec la ROM exacte à tester. Ne pas réutiliser un état d'une autre
version. Le noyau de diagnostic ne sert pas aux essais de progression.
