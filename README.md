# Tengai Makyou Zero — Traduction française V46

**31 nouveaux textes : 3 828 entrées intégrées.**
Lot 40 : Ran, Miki, Suu et la grotte des Belles (bloc 56, sauf S012).
Les 3 797 entrées V45 et les 32 modifications françaises des écrans initiaux
sont conservées. Les dialogues et événements restent partiels ; les menus
seront traités ensuite.

## Installation

Appliquer **Tengai_Makyou_Zero_FR_V46.ips** directement à la ROM anglaise
originale, sans cumuler les patches. Taille : 7 340 032 octets sans en-tête.
SHA-256 source : `eb07eed483f8f79ab64309c50ad0ef19560946b8e28fbd695470552ba68e356e`.
Le dépôt ne distribue ni ROM, ni sauvegarde d'état, ni noyau d'émulateur.

## Construction

```bash
python tools/build_v46.py /chemin/original.sfc --rom-out /chemin/fr_v46.sfc
python tools/verify_font.py /chemin/original.sfc
python tools/verify_storage.py /chemin/original.sfc --version V46 --built-rom /chemin/fr_v46.sfc --build-report verification/build_report.json
```

Python 3 et Pillow. Quarante lots JSON, corrections_v20.json et startup_text.py.
Les fichiers bilingues JSON/TSV et lecture_v46.txt sont produits localement.
Le constructeur refuse d'écraser une ancienne entrée lors de l'ajout du lot 40.
Il contrôle encodage, ordre des commandes et pauses, lignes de 216 pixels,
pointeurs, allocation, checksum et aller-retour IPS. Les chaînes de tous les
blocs intégrés sont relues par les routines originales 65816.

## Essais et limites

4 751 lectures natives, 16 contrôles de police, 14 de placement ; 31 rendus
ciblés et 39 captures de dialogue relues. Démarrage, navigation et A/reset/B
validés ; 85 captures fixes identiques à V45. 143 blocs sur place, 34 relocalisés,
77 312 octets libres. Voir COMPTE_RENDU_V46.md et emulation_report_v46.json.
Les rendus ciblés ne valident pas naturellement les rencontres aux heures
prévues, le choix d'une des trois belles ou la remise effective des récompenses.
B056-S012 et les différés antérieurs conservent leurs octets source.
Les tests de naissance détaillés restent documentés par V35. Conditions d'échec,
limites de calendrier, Snes9x 1.60 et matériel réel non testés.

## Reproduire

Construire V45 avec build_v45.py pour générer la ROM et les fichiers bilingues.
Empreinte ROM V45 :
`1fcb5d6ddab647de9a72550b6720af7c9a48dee2db2439de9d85a5e8c5819425`.
Rejouer run_scenario.py vers runs/fr_v45_reference46 puis run_navigation.py
vers runs/v45_navigation_reference46. Construire ensuite V46 pour que le
build_report.json corresponde à la ROM testée.

```bash
python verification/reproduction/run_version_checks.py --version v46 --tag final46 --render-workers 3 --source /chemin/original.sfc --emulator-root /chemin/emulator
python verification/reproduction/collect_evidence.py --version v46 --previous v45 --tag final46 --previous-tag reference46 --runs /chemin/emulator/runs --cases 31 --preview /chemin/contact --source /chemin/original.sfc --rom /chemin/emulator/fr_v46.sfc
python tools/audit_v46.py /chemin/original.sfc /chemin/emulator/fr_v45.sfc /chemin/emulator/fr_v46.sfc
```

Les noyaux standard/diagnostic sont compilés localement (Snes9x 1.63,
commit 1bcc369e89f08243e0a462882fb1f3e42e51de3a).
Chaque rendu possède un dossier isolé, un état initial de la ROM exacte
et un contrôle du terminateur. Le collecteur laisse la relecture en attente :
inspecter les captures avant validation. Les dossiers d'essais existants
sont refusés par run_version_checks.py ; utiliser un nouveau tag pour rejouer.
