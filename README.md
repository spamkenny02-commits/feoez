# Tengai Makyou Zero — Traduction française V47

**142 nouveaux textes : 3 970 entrées intégrées.**
Lot 41 : sanctuaire de la Grue, boutiques et auberges, lettres de Momoko,
Yumi, Arisa, Seiko et Courrier de la Grue (bloc 132 partiel).
Les 3 828 entrées V46 et les 32 modifications françaises des écrans initiaux
sont conservées. Les dialogues et événements restent partiels ; les menus
seront traités ensuite.

## Installation

Appliquer **Tengai_Makyou_Zero_FR_V47.ips** directement à la ROM anglaise
originale, sans cumuler les patches. Taille : 7 340 032 octets sans en-tête.
SHA-256 source : `eb07eed483f8f79ab64309c50ad0ef19560946b8e28fbd695470552ba68e356e`.
Le dépôt ne distribue ni ROM, ni sauvegarde d'état, ni noyau d'émulateur.

## Construction

```bash
python tools/build_v47.py /chemin/original.sfc --rom-out /chemin/fr_v47.sfc
python tools/verify_font.py /chemin/original.sfc
python tools/verify_storage.py /chemin/original.sfc --version V47 --built-rom /chemin/fr_v47.sfc --build-report verification/build_report.json
```

Python 3 et Pillow. Quarante et un lots JSON, corrections_v20.json et startup_text.py.
Les fichiers bilingues JSON/TSV et lecture_v47.txt sont produits localement.
Le constructeur refuse d'écraser une ancienne entrée lors de l'ajout du lot 41.
Il contrôle encodage, ordre des commandes et pauses, lignes de 216 pixels,
pointeurs, allocation, checksum et aller-retour IPS. Les chaînes de tous les
blocs intégrés sont relues par les routines originales 65816.

## Essais et limites

4 899 lectures natives, 16 contrôles de police, 14 de placement ; 142 rendus
ciblés et 286 captures de dialogue relues. Démarrage, navigation et A/reset/B
validés ; 85 captures fixes identiques à V46. 143 blocs sur place, 35 relocalisés,
56,608 octets libres. Voir COMPTE_RENDU_V47.md et emulation_report_v47.json.
Les rendus ciblés ne valident pas les parcours naturels, paiements, cadeaux,
choix, effets d'objets, réception et échéance des lettres ou Saint-Valentin.
Les six différés du bloc 132 et les différés antérieurs gardent leurs octets source.
Les tests de naissance détaillés restent documentés par V35. Conditions d'échec,
limites de calendrier, Snes9x 1.60 et matériel réel non testés.

## Reproduire

Construire V46 avec build_v46.py pour générer la ROM et les fichiers bilingues.
Empreinte ROM V46 :
`3c7b27e6a171877b10f8cc000daeb376505b3ce12aec4ab00881d39908403eb5`.
La référence publiée utilise le rejeu V46 final46 conservé, de cette ROM exacte.
Pour recréer cette référence, rejouer run_scenario.py vers runs/fr_v46_final46
puis run_navigation.py vers runs/v46_navigation_final46. Construire ensuite
V47 pour que build_report.json corresponde à la ROM testée.

```bash
python verification/reproduction/run_version_checks.py --version v47 --tag final47 --render-workers 3 --source /chemin/original.sfc --emulator-root /chemin/emulator
python verification/reproduction/collect_evidence.py --version v47 --previous v46 --tag final47 --previous-tag final46 --runs /chemin/emulator/runs --cases 142 --preview /chemin/contact --source /chemin/original.sfc --rom /chemin/emulator/fr_v47.sfc
python tools/audit_v47.py /chemin/original.sfc /chemin/emulator/fr_v46.sfc /chemin/emulator/fr_v47.sfc
```

Les noyaux standard/diagnostic sont compilés localement (Snes9x 1.63,
commit 1bcc369e89f08243e0a462882fb1f3e42e51de3a).
Chaque rendu possède un dossier isolé, un état initial de la ROM exacte
et un contrôle du terminateur. Le collecteur laisse la relecture en attente :
inspecter les captures avant validation. Les dossiers d'essais existants
sont refusés par run_version_checks.py ; utiliser un nouveau tag pour rejouer.
