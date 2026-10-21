# Tengai Makyou Zero — Traduction française V51

**300 nouveaux textes : 4 987 entrées intégrées.**
Lot 45 : 34 messages de dialogue/événements et 266 notices du calendrier.
Le calendrier, les dialogues et les formats spéciaux restent partiels.
Les 4 687 entrées V50 et les 32 modifications initiales sont conservées.
Les menus seront traités après les dialogues et événements.

## Installation

Appliquer **Tengai_Makyou_Zero_FR_V51.ips** directement à la ROM anglaise
originale, sans cumuler les patches. Taille : 7 340 032 octets sans en-tête.
SHA-256 source : `eb07eed483f8f79ab64309c50ad0ef19560946b8e28fbd695470552ba68e356e`.
Le dépôt ne distribue ni ROM, ni sauvegarde d'état, ni noyau d'émulateur.

## Construction

```bash
python tools/build_v51.py /chemin/original.sfc --rom-out /chemin/fr_v51.sfc
python tools/verify_font.py /chemin/original.sfc
python tools/verify_storage.py /chemin/original.sfc --version V51 --built-rom /chemin/fr_v51.sfc --build-report verification/build_report.json
```

Python 3 et Pillow. Quarante-cinq lots JSON, corrections_v20.json et startup_text.py.
Les fichiers bilingues JSON/TSV et lecture_v51.txt sont produits localement.
Le constructeur refuse d'écraser une ancienne entrée lors de l'ajout du lot 45.
Il contrôle encodage, ordre des commandes et pauses, lignes de 216 pixels,
pointeurs, allocation, checksum et aller-retour IPS. Les chaînes de tous les
blocs intégrés sont relues par les routines originales 65816.

## Essais et limites

6028 lectures natives, 16 contrôles de police, 14 de placement ; 300 rendus
ciblés et 303 captures de texte relues. Démarrage, navigation et A/reset/B
validés ; 85 captures fixes identiques à V50. 154 blocs sur place,
36 relocalisés, 55536 octets libres.
Voir COMPTE_RENDU_V51.md et emulation_report_v51.json.
Accès naturel aux événements et vues du calendrier non validés par les rendus ciblés.
Les anecdotes et dates du calendrier sont traduites selon la source, sans révision
historique. Variables réelles, services, élevage, musique et menus restent partiels.
Naissance détaillée : preuves V35. Snes9x 1.60 et matériel réel non testés.

## Reproduire

Construire V50 avec build_v50.py pour produire ROM et fichiers bilingues.
SHA-256 V50 : `e94f7f4dab0ac39e01de7c640d676f674a0d8a81e8e2ed5bc6d3f926950c9603`.
Référence : rejeu V50 corrected50 conservé, de cette ROM exacte.
Construire ensuite V51 pour actualiser build_report.json.

```bash
python tools/build_v51.py /chemin/original.sfc --rom-out /chemin/emulator/fr_v51.sfc
python verification/reproduction/build_diagnostic_core.py --source /chemin/snes9x --out /chemin/emulator/snes9x_libretro_diagnostic_v51.so
python verification/reproduction/run_version_checks.py --version v51 --tag final51 --render-workers 4 --compact-render --auto-close-captures --diagnostic-core /chemin/emulator/snes9x_libretro_diagnostic_v51.so --source /chemin/original.sfc --emulator-root /chemin/emulator
python verification/reproduction/collect_evidence.py --version v51 --previous v50 --tag final51 --previous-tag corrected50 --runs /chemin/emulator/runs --cases 300 --preview /chemin/contact --source /chemin/original.sfc --rom /chemin/emulator/fr_v51.sfc
python tools/audit_v51.py /chemin/original.sfc /chemin/emulator/fr_v50.sfc /chemin/emulator/fr_v51.sfc
```

Noyaux standard/diagnostic compilés localement : Snes9x 1.63,
commit 1bcc369e89f08243e0a462882fb1f3e42e51de3a.
Chaque rendu utilise un dossier isolé et un état de la ROM exacte.
Le collecteur laisse la relecture en attente : inspecter les captures avant validation.
--compact-render avec --auto-close-captures conserve la dernière image contenant
du texte sur chaque page, avant fermeture automatique ; les PNG restent inchangés.
La lecture de fin x5 est observée à 4D:3D8D : voir inline_terminator_check_v51.json.
Le mode compact V50 reste disponible sans cette option et son équivalence est
vérifiée dans compact_render_check_v50.json.
Utiliser un nouveau tag pour chaque rejeu.
