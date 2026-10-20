# Tengai Makyou Zero — Traduction française V49

**300 nouveaux textes : 4 387 entrées intégrées.**
Lot 43 : fêtes saisonnières, concours, marchands et Pavillon des Geishas.
Blocs 31, 37, 39 et 40 partiels.
Les 4 087 entrées V48 et les 32 modifications initiales sont conservées.
Dialogues et événements restent partiels ; les menus seront traités ensuite.

## Installation

Appliquer **Tengai_Makyou_Zero_FR_V49.ips** directement à la ROM anglaise
originale, sans cumuler les patches. Taille : 7 340 032 octets sans en-tête.
SHA-256 source : `eb07eed483f8f79ab64309c50ad0ef19560946b8e28fbd695470552ba68e356e`.
Le dépôt ne distribue ni ROM, ni sauvegarde d'état, ni noyau d'émulateur.

## Construction

```bash
python tools/build_v49.py /chemin/original.sfc --rom-out /chemin/fr_v49.sfc
python tools/verify_font.py /chemin/original.sfc
python tools/verify_storage.py /chemin/original.sfc --version V49 --built-rom /chemin/fr_v49.sfc --build-report verification/build_report.json
```

Python 3 et Pillow. Quarante-trois lots JSON, corrections_v20.json et startup_text.py.
Les fichiers bilingues JSON/TSV et lecture_v49.txt sont produits localement.
Le constructeur refuse d'écraser une ancienne entrée lors de l'ajout du lot 43.
Il contrôle encodage, ordre des commandes et pauses, lignes de 216 pixels,
pointeurs, allocation, checksum et aller-retour IPS. Les chaînes de tous les
blocs intégrés sont relues par les routines originales 65816.

## Essais et limites

5 446 lectures natives, 16 contrôles de police, 14 de placement ; 300 rendus
ciblés et 446 captures de dialogue relues. Démarrage, navigation et A/reset/B
validés ; 85 captures fixes identiques à V48. 148 blocs sur place,
35 relocalisés, 56608 octets libres.
Voir COMPTE_RENDU_V49.md et emulation_report_v49.json.
Progression naturelle, paiements, récompenses, concours, voeux et limites du
calendrier non validés. Différés des quatre nouveaux blocs et différés antérieurs
préservés. Noms d'objets à harmoniser avec les menus.
Naissance détaillée : preuves V35. Snes9x 1.60 et matériel réel non testés.

## Reproduire

Construire V48 avec build_v48.py pour produire ROM et fichiers bilingues.
SHA-256 V48 : `a8451782359c523bd0d37a29dd2e30006b2e9f6e9c79768e7b31c5a86148491a`.
Référence : rejeu V48 corrected48 conservé, de cette ROM exacte. Pour le recréer,
run_scenario.py vers runs/fr_v48_corrected48 puis run_navigation.py vers
runs/v48_navigation_corrected48. Construire ensuite V49 pour actualiser build_report.json.

```bash
python verification/reproduction/run_version_checks.py --version v49 --tag final49 --render-workers 3 --source /chemin/original.sfc --emulator-root /chemin/emulator
python verification/reproduction/collect_evidence.py --version v49 --previous v48 --tag final49 --previous-tag corrected48 --runs /chemin/emulator/runs --cases 300 --preview /chemin/contact --source /chemin/original.sfc --rom /chemin/emulator/fr_v49.sfc
python tools/audit_v49.py /chemin/original.sfc /chemin/emulator/fr_v48.sfc /chemin/emulator/fr_v49.sfc
```

Noyaux standard/diagnostic compilés localement : Snes9x 1.63,
commit 1bcc369e89f08243e0a462882fb1f3e42e51de3a.
Chaque rendu possède un dossier isolé, un état initial de la ROM exacte et
un contrôle du terminateur. Le collecteur laisse la relecture en attente :
inspecter les captures avant validation. Les dossiers d'essais existants sont
refusés ; utiliser un nouveau tag pour rejouer.
