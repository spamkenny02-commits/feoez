# Tengai Makyou Zero — Traduction française V43

**125 vrais nouveaux textes : 3 667 entrées intégrées.**
Lot 37 : Grand Tigre, Miho et retrouvailles de Rie/Shigenobu (bloc 95 partiel).
Les 3 542 entrées V42 et les 32 modifications françaises des écrans initiaux
sont conservées. La traduction reste partielle : dialogues et événements
encore à traiter, avant les menus.

## Installation

Appliquer **Tengai_Makyou_Zero_FR_V43.ips** directement à la ROM anglaise
originale, sans cumuler les patches. Taille : 7 340 032 octets sans en-tête.
SHA-256 : `eb07eed483f8f79ab64309c50ad0ef19560946b8e28fbd695470552ba68e356e`.
Le dépôt ne distribue ni ROM, ni sauvegarde d'état, ni noyau d'émulateur.

## Construction

```bash
python tools/build_v43.py /chemin/original.sfc --rom-out /chemin/fr_v43.sfc
python tools/verify_font.py /chemin/original.sfc
python tools/verify_storage.py /chemin/original.sfc --version V43 --built-rom /chemin/fr_v43.sfc --build-report verification/build_report.json
```

Python 3 et Pillow. Sources : trente-sept lots JSON, corrections_v20.json
et startup_text.py. Les fichiers bilingues JSON/TSV et lecture_v43.txt sont
produits localement. Encodage, balises et pauses, largeurs jusqu'à 216 pixels,
pointeurs, allocation, checksum et aller-retour IPS sont contrôlés.
4637 lectures par les routines originales 65816, 16 contrôles de
police et 14 de placement réussissent. Budget : 500 000 instructions par sélection.

## Essais et limites

Snes9x 1.63, commit 1bcc369e89f08243e0a462882fb1f3e42e51de3a.
Démarrage neuf, parcours initial, navigation, A puis reset puis B prolongé.
Les contrôles mémoire/SPC7110/SRAM/RTC, A/B/reset, naissance et horloge restent
en français. Les 32 modifications initiales sont identiques à V42 ; signatures
internes de sauvegarde intactes. La saisie détaillée de naissance reste celle de V35.

125 cas ciblés atteignent leur terminateur exact ; 172 captures relues.
85 captures fixes identiques à V42,
0 différentes. Navigation : navigation_comparison_v42_v43.json.
Captures et empreintes : verification/scenes_v43. Les pauses peuvent produire
plusieurs captures partielles d'une même page.

Le rendu ciblé redirige un dialogue : il ne valide pas naturellement les quêtes,
achats, cadeaux, affection, délais, choix effectifs ou effets en combat.
Conditions d'échec, toutes les limites de calendrier, Snes9x 1.60 et matériel
réel non testés. Horaires de Miho, noms dynamiques, x5, choix de maison,
autres chambres et fin du bloc 95 restent à reprendre. Les différés antérieurs
restent intacts. Voir deferred_reasons_v43.json, deferred_texts_v43.json et
unprocessed_inventory_v43.json. Les dialogues/événements ne sont pas complets.

## Reproduire

Construire V42 avec build_v42.py si la ROM ou les fichiers bilingues manquent.
Vérifier son empreinte publiée :
`5ccb91d0908b6b198f37687f61e7ea537c4f92ecfa3816f77d756ad985065bbe`.
Rejouer run_scenario.py vers runs/fr_v42_reference43, puis run_navigation.py
vers runs/v42_navigation_reference43. Construire ensuite V43 pour que
build_report.json corresponde à la ROM testée.
Noyaux standard et diagnostic compilés localement sous les noms
snes9x_libretro_standard.so / snes9x_libretro_diagnostic.so dans emulator.

```bash
python verification/reproduction/run_version_checks.py --version v43 --tag corrected43 --render-workers 3 --source /chemin/original.sfc --emulator-root /chemin/emulator
python verification/reproduction/collect_evidence.py --version v43 --previous v42 --tag corrected43 --previous-tag reference43 --runs /chemin/emulator/runs --cases 125 --preview /chemin/contact --source /chemin/original.sfc --rom /chemin/emulator/fr_v43.sfc
```

Le rendu peut utiliser trois processus isolés (--render-workers 3) ; chaque cas
conserve son état initial de la même ROM, son dossier et son terminateur exact.
Les dossiers de parcours existants sont refusés : choisir un nouveau tag.
Le collecteur laisse la relecture visuelle en attente ; la faire sur les captures
de la ROM exacte avant validation. Voir COMPTE_RENDU_V43.md et emulation_report_v43.json.
