# Tengai Makyou Zero — Traduction française V40

**41 textes supplémentaires : 3 440 entrées intégrées.**
Lot 34 : Omine, insignes d’or et habitants de la ville du Grand Tigre (86).
Les 3 399 entrées précédentes et les 32 occurrences initiales sont conservées.

Les écrans SPC7110/SRAM/RTC, naissance et horloge restent en français.
Les signatures internes restent intactes. B086-S007/008/009 attendent les
commandes de noms variables 05/06/07. Les différés antérieurs et les
lacunes figurent dans verification/unprocessed_inventory_v40.json
et deferred_texts_v40.json : 60 messages et quatre invites de débogage
différés dans les blocs traités.

## Installation

Appliquer **Tengai_Makyou_Zero_FR_V40.ips** directement à une copie de la ROM
anglaise originale, sans cumuler les versions.

- Taille source : 7 340 032 octets, sans en-tête de copieur.
- SHA-256 : `eb07eed483f8f79ab64309c50ad0ef19560946b8e28fbd695470552ba68e356e`.

Le dépôt ne contient ni ROM, ni sauvegarde d'état, ni noyau binaire d'émulateur.

## Construction

```bash
python tools/build_v40.py /chemin/original.sfc --rom-out /chemin/v40.sfc
python tools/verify_font.py /chemin/original.sfc
python tools/verify_storage.py /chemin/original.sfc --version V40 --built-rom /chemin/v40.sfc --build-report verification/build_report.json
```

Python 3 et Pillow. Les trente-quatre lots JSON, corrections_v20.json et
startup_text.py sont les sources. Les fichiers bilingues JSON/TSV et
lecture_v40.txt sont produits localement. Le générateur contrôle les balises,
les largeurs jusqu'à 216 pixels, les pointeurs, le checksum, l'encodage,
l'aller-retour IPS et les chaînes par les routines originales 65816.
Le banc conserve le budget de 500 000 instructions par sélection.
4 259 lectures natives, 16 contrôles de police et 14 contrôles de placement
réussissent. 134 blocs restent sur place, 34 sont relocalisés et
77 312 octets restent libres. Voir verification/build_report.json.

## Essais dans Snes9x

Noyau standard Snes9x 1.63, commit 1bcc369e89f08243e0a462882fb1f3e42e51de3a.
Démarrage neuf, parcours du début, contrôles A puis reset puis B prolongé
à 60 000 images. A affiche TERMINE / TOUT OK ; B affiche SAUV. RTC OK et
SAUV. SRAM OK. Aucun bandeau de fin B n'est annoncé.

Les 41 nouvelles entrées sont rendues avec vérification du terminateur exact.
Les captures relues figurent dans verification/scenes_v40 ; les comptes et
comparaisons sont dans verification/emulation_report_v40.json.
Les essais redirigent une demande de dialogue ; ils ne valident pas les
achats, dons, effets des insignes ou événements en progression naturelle.

Les 32 occurrences initiales sont comparées octet par octet à V39.
La saisie approfondie de naissance reste documentée dans verification/startup_v35
et startup_numeric_comparison_v35.json. V40 rejoue le démarrage et les contrôles A/B.
Snes9x 1.60, les conditions d'échec, toutes les limites de calendrier et le
matériel réel ne sont pas testés. Voir COMPTE_RENDU_V40.md et
verification/emulation_report_v40.json pour les résultats et leurs limites.

## Reproduire les essais

Avec les noyaux standard et diagnostic compilés localement et nommés
snes9x_libretro_standard.so et snes9x_libretro_diagnostic.so dans le dossier
emulator, ainsi que la ROM reconstruite fr_v40.sfc :

La comparaison demande aussi une référence V39. La reconstruire avant V40,
puis lancer run_scenario.py vers runs/fr_v39_reference40 et run_navigation.py
vers runs/v39_navigation_reference40 avec cette ROM et le noyau standard.
Reconstruire ensuite V40 pour que build_report.json corresponde à la ROM testée.

```bash
python verification/reproduction/run_version_checks.py --version v40 --tag final --source /chemin/original.sfc --emulator-root /chemin/emulator
python verification/reproduction/collect_evidence.py --version v40 --previous v39 --tag final --previous-tag reference40 --runs /chemin/emulator/runs --cases 41 --preview /chemin/contact --source /chemin/original.sfc --rom /chemin/emulator/fr_v40.sfc
```

Le script refuse les dossiers de parcours existants : choisir un nouveau tag
pour de nouveaux essais. Le collecteur laisse la relecture visuelle en attente ;
elle doit être effectuée sur les captures sélectionnées avant validation.
Le patch diagnostic est documenté dans verification/reproduction ; aucun
état ni noyau n'est distribué. Les scripts de saisie détaillée V35 et leurs
commandes restent dans ce même dossier.
