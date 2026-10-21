# Tengai Makyou Zero — Traduction française V50

**300 nouveaux textes : 4 687 entrées intégrées.**
Lot 44 : voyance, change, lettres de Momoko, élevage, fêtes, salons et
textes différés régionaux. Les dialogues et formats spéciaux restent partiels.
Les 4 387 entrées V49 et les 32 modifications initiales sont conservées.
Dialogues et événements restent partiels ; les menus seront traités ensuite.

## Installation

Appliquer **Tengai_Makyou_Zero_FR_V50.ips** directement à la ROM anglaise
originale, sans cumuler les patches. Taille : 7 340 032 octets sans en-tête.
SHA-256 source : `eb07eed483f8f79ab64309c50ad0ef19560946b8e28fbd695470552ba68e356e`.
Le dépôt ne distribue ni ROM, ni sauvegarde d'état, ni noyau d'émulateur.

## Construction

```bash
python tools/build_v50.py /chemin/original.sfc --rom-out /chemin/fr_v50.sfc
python tools/verify_font.py /chemin/original.sfc
python tools/verify_storage.py /chemin/original.sfc --version V50 --built-rom /chemin/fr_v50.sfc --build-report verification/build_report.json
```

Python 3 et Pillow. Quarante-quatre lots JSON, corrections_v20.json et startup_text.py.
Les fichiers bilingues JSON/TSV et lecture_v50.txt sont produits localement.
Le constructeur refuse d'écraser une ancienne entrée lors de l'ajout du lot 44.
Il contrôle encodage, ordre des commandes et pauses, lignes de 216 pixels,
pointeurs, allocation, checksum et aller-retour IPS. Les chaînes de tous les
blocs intégrés sont relues par les routines originales 65816.

## Essais et limites

5 644 lectures natives, 16 contrôles de police, 14 de placement ; 300 rendus
ciblés et 582 captures de dialogue relues. Démarrage, navigation et A/reset/B
validés ; 85 captures fixes identiques à V49. 154 blocs sur place,
34 relocalisés, 71600 octets libres.
Voir COMPTE_RENDU_V50.md et emulation_report_v50.json.
Progression des services, choix, variables réelles, change, lettres, calendrier,
élevage hors tension et synchronisation musicale non validés. Tous les différés
restants sont préservés. Noms nouveaux provisoires ; menus et états partiels.
Naissance détaillée : preuves V35. Snes9x 1.60 et matériel réel non testés.

## Reproduire

Construire V49 avec build_v49.py pour produire ROM et fichiers bilingues.
SHA-256 V49 : `e13a8bcdee8cac7d53e33fb9092de5ec5d84d5613ef83ff5836cd70b6c2af396`.
Référence : rejeu V49 final49 conservé, de cette ROM exacte. Pour le recréer,
run_scenario.py vers runs/fr_v49_final49 puis run_navigation.py vers
runs/v49_navigation_final49. Construire ensuite V50 pour actualiser build_report.json.

```bash
python verification/reproduction/run_version_checks.py --version v50 --tag corrected50 --render-workers 4 --compact-render --source /chemin/original.sfc --emulator-root /chemin/emulator
python verification/reproduction/collect_evidence.py --version v50 --previous v49 --tag corrected50 --previous-tag final49 --runs /chemin/emulator/runs --cases 300 --preview /chemin/contact --source /chemin/original.sfc --rom /chemin/emulator/fr_v50.sfc
python tools/audit_v50.py /chemin/original.sfc /chemin/emulator/fr_v49.sfc /chemin/emulator/fr_v50.sfc
```

Noyaux standard/diagnostic compilés localement : Snes9x 1.63,
commit 1bcc369e89f08243e0a462882fb1f3e42e51de3a.
Chaque rendu possède un dossier isolé, un état initial de la ROM exacte et
un contrôle du terminateur. Le collecteur laisse la relecture en attente :
inspecter les captures avant validation. --compact-render ne conserve que la dernière
image de chaque page après réussite du cas ; équivalence vérifiée dans
compact_render_check_v50.json. Les dossiers d'essais existants sont
refusés ; utiliser un nouveau tag pour rejouer.
