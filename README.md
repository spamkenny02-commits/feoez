# Tengai Makyou Zero — Traduction française V34

123 textes ajoutés, soit **3 160 entrées intégrées avec accents**.
Les 3 037 entrées de V33 restent inchangées. Variantes et répétitions sont
comptées séparément. Premier jet depuis l'anglais fourni ; noms au glossaire.

Le lot couvre les statues des gardiens, les scènes d'Akamaru et Doki,
Ninigi et les discours du couronnement. Les alias 248 et 250/251 sont couverts.
50 messages restent différés dans les blocs traités, auxquels s'ajoutent
quatre invites de débogage B252-S098 à S101. Le journal 210, les blocs
235/236, le menu 244/245 et le bloc 253 restent à traiter. Les blocs 132 et
183 sont conservés.

## Installation

Appliquer **Tengai_Makyou_Zero_FR_V34.ips** directement à une copie de la ROM
anglaise originale, sans cumuler les versions.

- Taille source : 7 340 032 octets, sans en-tête de copieur.
- SHA-256 : `eb07eed483f8f79ab64309c50ad0ef19560946b8e28fbd695470552ba68e356e`.

Le dépôt ne contient ni ROM, ni sauvegarde d'état, ni noyau binaire d'émulateur.

## Construction

```bash
python tools/build_v34.py /chemin/original.sfc --rom-out /chemin/v34.sfc
python tools/verify_font.py /chemin/original.sfc
python tools/verify_storage.py /chemin/original.sfc --version V34 --built-rom /chemin/v34.sfc --build-report verification/build_report.json
```

Python 3 et Pillow. Les vingt-neuf lots JSON et corrections_v20.json sont les sources.
Le générateur produit les fichiers bilingues JSON/TSV et lecture_v34.txt localement.
3 968 lectures dans les routines originales 65816 passent, avec les chaînes
inchangées et les alias. Balises, largeur maximale de 216 pixels, pointeurs,
checksum, encodage et aller-retour IPS sont contrôlés. Le banc permet
500 000 instructions par sélection : certains indices anglais dépassent
l'ancien plafond de 100 000 (selection_checks_v31.json). Les 16 contrôles de police
et 14 contrôles du placement passent. 125 blocs sur place, 33 relocalisés,
80 656 octets libres ; le fichier anglais d'entrée n'est pas modifié.

## Essais dans Snes9x

Noyau standard Snes9x 1.63, commit 1bcc369e89f08243e0a462882fb1f3e42e51de3a.
Démarrage neuf et parcours du début. Contrôles A puis reset puis B prolongé
à 60 000 images : A affiche COMPLETE / ALL OK ; B indique OK pour
RTC BACKUP et S-RAM BACKUP (scenario_checks_v34.json).
Sur 85 captures communes avec V33 : 85 identiques, 0 différentes.
Voir verification/comparison_v33_v34.json et
verification/navigation_comparison_v33_v34.json. Les écarts de phase fixes
observés entre V32 et V33 restent documentés dans les rapports V33 ; ils
ne prouvent pas une équivalence temporelle complète avec V32.
Menus et carte accessibles.
La version 1.60, le jeu complet et le matériel réel ne sont pas testés ici.

126 essais ciblés couvrent les 123 textes nouveaux et trois alias,
y compris les longues interventions de Ninigi et les variantes Tenjin/Mizuki.
Ils utilisent la ROM finale inchangée et un noyau de diagnostic séparé qui
redirige une seule demande de dialogue vers le bloc et le message testés.
Les routines de lookup, sélection, lecture et rendu restent celles du jeu.
Le curseur doit atteindre le terminateur exact, puis les captures sont relues.

**Ces essais valident les textes et leur pagination, pas les combats,
les choix, le vol en Mahamayuri, la progression jusqu'au dénouement ni
le couronnement jouable.** Les arrière-plans appartiennent au banc de test.
Rapport et images : verification/scenes_v34.

## Reproduire les essais ciblés

Compiler le noyau standard depuis https://github.com/snes9xgit/snes9x au commit
ci-dessus. NumPy et Pillow sont nécessaires pour le frontend. Le constructeur
de diagnostic restaure le code source et le noyau standard après compilation.

```bash
python verification/reproduction/build_diagnostic_core.py --source /chemin/snes9x --out /chemin/diagnostic.so
python verification/reproduction/prepare_dialogue_state.py --core /chemin/standard.so --rom /chemin/v34.sfc --out /chemin/etat_v34
python verification/reproduction/run_targeted_dialogues.py --core /chemin/diagnostic.so --rom /chemin/v34.sfc --state /chemin/etat_v34/dialogue_entry.state --out /chemin/essais_v34 --cases verification/reproduction/cases_v34.json
```

Créer l'état avec la ROM exacte à tester. Ne pas réutiliser un état d'une autre
version. Le noyau de diagnostic ne sert pas aux essais de progression.

Le lanceur commun refuse de réutiliser un répertoire de parcours existant :

```bash
python verification/reproduction/run_version_checks.py --version v34 --tag final --source /chemin/original.sfc --emulator-root /chemin/emulator
```

Ce dossier emulator contient fr_v34.sfc, les noyaux standard et de diagnostic
nommés comme dans SUIVI_FEOE.md, puis reçoit les parcours et journaux locaux.
Relire les captures avant de considérer les essais de rendu comme vérifiés.
