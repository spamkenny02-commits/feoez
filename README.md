# Tengai Makyou Zero — Traduction française V48

**117 nouveaux textes : 4 087 entrées intégrées.**
Lot 42 : pays de l'Ours de Feu, boutiques, auberge, Akina et salons,
six articles du Clairon de l'Ours (bloc 66 partiel).
Les 3 970 entrées V47 et les 32 modifications initiales sont conservées.
Dialogues et événements restent partiels ; les menus seront traités ensuite.

## Installation

Appliquer **Tengai_Makyou_Zero_FR_V48.ips** directement à la ROM anglaise
originale, sans cumuler les patches. Taille : 7 340 032 octets sans en-tête.
SHA-256 source : `eb07eed483f8f79ab64309c50ad0ef19560946b8e28fbd695470552ba68e356e`.
Le dépôt ne distribue ni ROM, ni sauvegarde d'état, ni noyau d'émulateur.

## Construction

```bash
python tools/build_v48.py /chemin/original.sfc --rom-out /chemin/fr_v48.sfc
python tools/verify_font.py /chemin/original.sfc
python tools/verify_storage.py /chemin/original.sfc --version V48 --built-rom /chemin/fr_v48.sfc --build-report verification/build_report.json
```

Python 3 et Pillow. Quarante-deux lots JSON, corrections_v20.json et startup_text.py.
Les fichiers bilingues JSON/TSV et lecture_v48.txt sont produits localement.
Le constructeur refuse d'écraser une ancienne entrée lors de l'ajout du lot 42.
Il contrôle encodage, ordre des commandes et pauses, lignes de 216 pixels,
pointeurs, allocation, checksum et aller-retour IPS. Les chaînes de tous les
blocs intégrés sont relues par les routines originales 65816.

## Essais et limites

5 031 lectures natives, 16 contrôles de police, 14 de placement ; 117 rendus
ciblés et 254 captures de dialogue relues. Démarrage, navigation et A/reset/B
validés ; 85 captures fixes identiques à V47. 144 blocs sur place,
35 relocalisés, 56608 octets libres.
Voir COMPTE_RENDU_V48.md et emulation_report_v48.json.
Parcours naturels, paiements, cadeaux, choix, effets des remèdes, repos,
Saint-Valentin, ouverture PLGS et calendrier non validés. Quinze différés du bloc 66
et différés antérieurs préservent leurs octets. Remèdes à harmoniser avec les menus.
Naissance détaillée : preuves V35. Conditions d'échec, limites de calendrier,
Snes9x 1.60 et matériel réel non testés.

## Reproduire

Construire V47 avec build_v47.py pour produire ROM et fichiers bilingues.
SHA-256 V47 : `b121123906aaa00d9a15412dfaa3dc44a8902ea42ff98622458187a55e63b879`.
Référence : rejeu V47 final47 conservé, de cette ROM exacte. Pour le recréer,
run_scenario.py vers runs/fr_v47_final47 puis run_navigation.py vers
runs/v47_navigation_final47. Construire ensuite V48 pour actualiser build_report.json.

```bash
python verification/reproduction/run_version_checks.py --version v48 --tag corrected48 --render-workers 3 --source /chemin/original.sfc --emulator-root /chemin/emulator
python verification/reproduction/collect_evidence.py --version v48 --previous v47 --tag corrected48 --previous-tag final47 --runs /chemin/emulator/runs --cases 117 --preview /chemin/contact --source /chemin/original.sfc --rom /chemin/emulator/fr_v48.sfc
python tools/audit_v48.py /chemin/original.sfc /chemin/emulator/fr_v47.sfc /chemin/emulator/fr_v48.sfc
```

Noyaux standard/diagnostic compilés localement : Snes9x 1.63,
commit 1bcc369e89f08243e0a462882fb1f3e42e51de3a.
Chaque rendu possède un dossier isolé, un état initial de la ROM exacte et
un contrôle du terminateur. Le collecteur laisse la relecture en attente :
inspecter les captures avant validation. Les dossiers d'essais existants sont
refusés ; utiliser un nouveau tag pour rejouer.
