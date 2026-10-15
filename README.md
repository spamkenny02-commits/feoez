# Tengai Makyou Zero — Traduction française V25

144 entrées ajoutées, dont 132 textes modifiés et douze réponses neutres conservées.
**1 985 entrées intégrées avec accents**. Suima, Mugen, Agni, épreuve d'Higan,
libre choix et miroirs de Tenjin et Mizuki. Les 1 841 entrées de V24 sont inchangées.
Variantes et répétitions sont comptées séparément. Premier jet depuis l'anglais
fourni ; noms provisoires au glossaire.

Le bloc 173/174 reçoit une traduction unique. Les récompenses annoncées et les
variantes Tenjin/Mizuki restent distinctes. La condition des jours divisibles en
deux reprend le script sans extrapolation du calendrier. Les douze réponses
neutres sont documentées dans regression_v24_v25.json et le glossaire.
Relecture à l'écran : B171-S018 et B173-S022/S070 raccourcis pour éviter des fins
de page isolées, puis retestés sur la ROM finale. 18 messages différés et le
bloc 132 restent inchangés en anglais.

## Installation

Appliquer **Tengai_Makyou_Zero_FR_V25.ips** directement à une copie de la ROM
anglaise originale, sans cumuler les versions.

- Taille source : 7 340 032 octets, sans en-tête de copieur.
- SHA-256 : `eb07eed483f8f79ab64309c50ad0ef19560946b8e28fbd695470552ba68e356e`.

Le dépôt ne contient ni ROM, ni sauvegarde d'état, ni noyau binaire d'émulateur.

## Construction

```bash
python tools/build_v25.py /chemin/original.sfc --rom-out /chemin/v25.sfc
python tools/verify_font.py /chemin/original.sfc
python tools/verify_storage.py /chemin/original.sfc --version V25 --built-rom /chemin/v25.sfc --build-report verification/build_report.json
```

Python 3 et Pillow. Les vingt lots JSON et corrections_v20.json sont les sources.
Le générateur produit les fichiers bilingues JSON/TSV et lecture_v25.txt localement.
2 565 lectures dans les routines originales 65816 passent, avec les chaînes
inchangées et les alias. Balises, largeur maximale de 216 pixels, pointeurs,
checksum, encodage et aller-retour IPS sont contrôlés. Les 16 contrôles de police
et 14 contrôles du placement passent. 72 blocs sur place, 28 relocalisés,
83 360 octets libres ; le fichier anglais d'entrée n'est pas modifié.

## Essais dans Snes9x

Noyau standard Snes9x 1.63, commit 1bcc369e89f08243e0a462882fb1f3e42e51de3a.
Démarrage neuf et parcours du début. Contrôles A puis reset puis B prolongé
à 60 000 images : COMPLETE / ALL OK (scenario_checks_v25.json).
Les 85 captures communes avec V24 sont identiques. Menus et carte accessibles.
La version 1.60, le jeu complet et le matériel réel ne sont pas testés ici.

Dix-sept essais ciblés contrôlent Suima, l'œuf envoyé tous les vingt ans, Mugen,
le sanctuaire et les directions, Alabaster et son alias, l'épreuve et l'accusation
d'Agni, le miroir de Mizuki, la restauration, le libre choix, la réplique de Mizuki,
la condition et l'amour des miroirs, les reflets unis et la Flamme sur Terre.
Ils utilisent la ROM finale inchangée et un noyau de diagnostic séparé qui
redirige une seule demande de dialogue vers le bloc et le message testés.
Les routines de lookup, sélection, lecture et rendu restent celles du jeu.
Le curseur doit atteindre le terminateur exact, puis les captures sont relues.

**Ces essais valident les textes et leur pagination, pas la progression naturelle,
les combats, les récompenses, la restauration, l'épreuve d'Higan
ou les conditions de calendrier et de progression des miroirs.** Les arrière-plans appartiennent au banc de test.
Rapport et images : verification/scenes_v25.

## Reproduire les essais ciblés

Compiler le noyau standard depuis https://github.com/snes9xgit/snes9x au commit
ci-dessus. NumPy et Pillow sont nécessaires pour le frontend. Le constructeur
de diagnostic restaure le code source et le noyau standard après compilation.

```bash
python verification/reproduction/build_diagnostic_core.py --source /chemin/snes9x --out /chemin/diagnostic.so
python verification/reproduction/prepare_dialogue_state.py --core /chemin/standard.so --rom /chemin/v25.sfc --out /chemin/etat_v25
python verification/reproduction/run_targeted_dialogues.py --core /chemin/diagnostic.so --rom /chemin/v25.sfc --state /chemin/etat_v25/dialogue_entry.state --out /chemin/essais_v25 --cases verification/reproduction/cases_v25.json
```

Créer l'état avec la ROM exacte à tester. Ne pas réutiliser un état d'une autre
version. Le noyau de diagnostic ne sert pas aux essais de progression.
