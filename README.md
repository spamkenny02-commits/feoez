# Tengai Makyou Zero — Traduction française V22

23 nouvelles répliques, **1 582 entrées intégrées avec accents**.
Ce lot ouvre le royaume du Dragon : villages de la Gueule et des Yeux du Dragon,
statues de Ninigi, message de Shiranui et avertissements sur l'état du royaume.
Les références 155/156 partagent la même traduction. Les 1 559 entrées de V21
sont conservées à l'identique. Les variantes et répétitions sont comptées séparément.

Premier jet depuis l'anglais fourni ; noms provisoires documentés dans le glossaire.
Les nouvelles indications conservent leurs directions, les pauses et les variantes
avant/après libération du Dragon. 18 messages différés et le bloc 132 restent
inchangés en anglais.

## Installation

Appliquer **Tengai_Makyou_Zero_FR_V22.ips** directement à une copie de la ROM
anglaise originale, sans cumuler les versions.

- Taille source : 7 340 032 octets, sans en-tête de copieur.
- SHA-256 : `eb07eed483f8f79ab64309c50ad0ef19560946b8e28fbd695470552ba68e356e`.

Le dépôt ne contient ni ROM, ni sauvegarde d'état, ni noyau binaire d'émulateur.

## Construction

```bash
python tools/build_v22.py /chemin/original.sfc --rom-out /chemin/v22.sfc
python tools/verify_font.py /chemin/original.sfc
python tools/verify_storage.py /chemin/original.sfc --version V22 --built-rom /chemin/v22.sfc --build-report verification/build_report.json
```

Python 3 et Pillow. Les dix-sept lots JSON et corrections_v20.json sont les sources.
Le générateur produit les fichiers bilingues JSON/TSV et lecture_v22.txt localement.
2 080 lectures dans les routines originales 65816 passent, avec les chaînes
inchangées et les alias. Balises, largeur maximale de 216 pixels, pointeurs,
checksum, encodage et aller-retour IPS sont contrôlés. Les 16 contrôles de police
et 14 contrôles du placement passent. 60 blocs sur place, 23 relocalisés,
91 104 octets libres ; le fichier anglais d'entrée n'est pas modifié.

## Essais dans Snes9x

Noyau standard Snes9x 1.63, commit 1bcc369e89f08243e0a462882fb1f3e42e51de3a.
Démarrage neuf : A, vérification, reset, B, vérification, reset. Autotests ALL OK.
Le contrôle B est aussi prolongé à 15 000 images après initialisation par A,
pour observer son résultat complet (scenario_checks_v22.json).
Sur 85 captures communes avec V21, 82 sont identiques ; 3
présentent seulement une minute différente sur l'horloge. Menus et carte accessibles.
La version 1.60, le jeu complet et le matériel réel ne sont pas testés ici.

Neuf essais ciblés contrôlent les nouveaux dialogues à l'écran : royaume et
alias, message de Shiranui, statue de Ninigi, directions, caractères du Dragon,
sanctuaire au nord-est, victoire contre Shiranui et état du royaume.
Ils utilisent la ROM finale inchangée et un noyau de diagnostic séparé qui
redirige une seule demande de dialogue vers le bloc et le message testés.
Les routines de lookup, sélection, lecture et rendu restent celles du jeu.
Le curseur doit atteindre le terminateur exact, puis les captures sont relues.

**Ces essais valident les textes et leur pagination, pas la progression naturelle,
les positions des PNJ, les choix de quête, les récompenses ou le recrutement.**
Les arrière-plans de ces captures sont ceux du banc de test. Rapport et images :
verification/scenes_v22. Les messages différés et le bloc 132 restent en anglais.

## Reproduire les essais ciblés

Compiler le noyau standard depuis https://github.com/snes9xgit/snes9x au commit
ci-dessus. NumPy et Pillow sont nécessaires pour le frontend. Le constructeur
de diagnostic restaure le code source et le noyau standard après compilation.

```bash
python verification/reproduction/build_diagnostic_core.py --source /chemin/snes9x --out /chemin/diagnostic.so
python verification/reproduction/prepare_dialogue_state.py --core /chemin/standard.so --rom /chemin/v22.sfc --out /chemin/etat_v22
python verification/reproduction/run_targeted_dialogues.py --core /chemin/diagnostic.so --rom /chemin/v22.sfc --state /chemin/etat_v22/dialogue_entry.state --out /chemin/essais_v22 --cases verification/reproduction/cases_v22.json
```

Créer l'état avec la ROM exacte à tester. Ne pas réutiliser un état d'une autre
version. Le noyau de diagnostic ne sert pas aux essais de progression.
