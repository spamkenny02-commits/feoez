# Tengai Makyou Zero — Traduction française V36

**43 textes supplémentaires, soit 3 203 entrées de dialogue intégrées.**
Lot 30 : scènes de Manto (167), choix des trois boutons (244/245), chambre
du prince et variantes des œufs (253). Les 3 160 entrées précédentes et les
32 occurrences des écrans de démarrage, de naissance et d'horloge sont conservées.

Les contrôles SPC7110/SRAM/RTC, les instructions A/B/reset et les confirmations
restent en français. Les signatures internes de sauvegarde sont conservées.
La traduction reste partielle : journal 210, blocs 235/236 et autres lacunes
répertoriées dans verification/unprocessed_inventory_v36.json ; 50 messages
différés et quatre invites de débogage dans les blocs déjà traités.

## Installation

Appliquer **Tengai_Makyou_Zero_FR_V36.ips** directement à une copie de la ROM
anglaise originale, sans cumuler les versions.

- Taille source : 7 340 032 octets, sans en-tête de copieur.
- SHA-256 : `eb07eed483f8f79ab64309c50ad0ef19560946b8e28fbd695470552ba68e356e`.

Le dépôt ne contient ni ROM, ni sauvegarde d'état, ni noyau binaire d'émulateur.

## Construction

```bash
python tools/build_v36.py /chemin/original.sfc --rom-out /chemin/v36.sfc
python tools/verify_font.py /chemin/original.sfc
python tools/verify_storage.py /chemin/original.sfc --version V36 --built-rom /chemin/v36.sfc --build-report verification/build_report.json
```

Python 3 et Pillow. Les trente lots JSON, corrections_v20.json et
startup_text.py sont les sources. Les fichiers bilingues JSON/TSV et
lecture_v36.txt sont produits localement. Le générateur contrôle les balises,
les largeurs jusqu'à 216 pixels, les pointeurs, le checksum, l'encodage,
l'aller-retour IPS et les chaînes par les routines originales 65816.
Le banc conserve le budget de 500 000 instructions par sélection.
4 012 lectures natives, 16 contrôles de police et 14 contrôles de placement
passent. 127 blocs restent sur place, 34 sont relocalisés ; 77 312 octets
restent libres. Les comptes sont dans verification/build_report.json.

## Essais dans Snes9x

Noyau standard Snes9x 1.63, commit 1bcc369e89f08243e0a462882fb1f3e42e51de3a.
Démarrage neuf, parcours du début, contrôles A puis reset puis B prolongé
à 60 000 images. A affiche TERMINE / TOUT OK ; B affiche SAUV. RTC OK et
SAUV. SRAM OK. Aucun bandeau de fin B n'est annoncé.

Les 43 textes modifiés et l'alias 245 sont rendus avec vérification du
terminateur exact. Les 58 captures relues figurent dans verification/scenes_v36.
Les 85 captures fixes communes du début et les trois écrans de navigation
sont identiques à V35.
Les trois colonnes du choix Gauche/Centre/Droite restent à un pixel au plus
de leur position anglaise (columns_v36.json). Les essais redirigent une
demande de dialogue vers une chaîne donnée ; ils ne valident pas les
événements, les conséquences des boutons ou l'éclosion en progression naturelle.

Les 32 modifications initiales V35 sont vérifiées octet par octet. Ses preuves
approfondies de saisie de naissance restent dans verification/startup_v35 et
startup_numeric_comparison_v35.json ; V36 rejoue le parcours de démarrage.
Snes9x 1.60, les conditions d'échec, toutes les limites de calendrier et le
matériel réel ne sont pas testés. Voir COMPTE_RENDU_V36.md et
verification/emulation_report_v36.json pour les résultats et leurs limites.

## Reproduire les essais

Avec les noyaux standard et diagnostic compilés localement et nommés
snes9x_libretro_standard.so et snes9x_libretro_diagnostic.so dans le dossier
emulator, ainsi que la ROM reconstruite fr_v36.sfc :

```bash
python verification/reproduction/run_version_checks.py --version v36 --tag corrected --source /chemin/original.sfc --emulator-root /chemin/emulator
python verification/reproduction/collect_evidence.py --version v36 --previous v35 --tag corrected --previous-tag final --runs /chemin/emulator/runs --cases 44 --preview /chemin/contact --source /chemin/original.sfc --rom /chemin/emulator/fr_v36.sfc
```

Le script refuse les dossiers de parcours existants : choisir un nouveau tag
pour de nouveaux essais. Le collecteur laisse la relecture visuelle en attente ;
elle doit être effectuée sur les captures sélectionnées avant validation.
Le patch diagnostic est documenté dans verification/reproduction ; aucun
état ni noyau n'est distribué. Les scripts de saisie détaillée V35 et leurs
commandes restent dans ce même dossier.
