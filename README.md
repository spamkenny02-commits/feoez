# Tengai Makyou Zero — Traduction française V44

**58 vrais nouveaux textes : 3 725 entrées intégrées.**
Lot 38 : Cercle Fleuri, salons, boutiques et presse du Grand Tigre (88/95 partiels).
Les 3 667 entrées V43 et les 32 modifications françaises des écrans initiaux
sont conservées. La traduction reste partielle : dialogues et événements
encore à traiter, avant les menus.

## Installation

Appliquer **Tengai_Makyou_Zero_FR_V44.ips** directement à la ROM anglaise
originale, sans cumuler les patches. Taille : 7 340 032 octets sans en-tête.
SHA-256 : `eb07eed483f8f79ab64309c50ad0ef19560946b8e28fbd695470552ba68e356e`.
Le dépôt ne distribue ni ROM, ni sauvegarde d'état, ni noyau d'émulateur.

## Construction

```bash
python tools/build_v44.py /chemin/original.sfc --rom-out /chemin/fr_v44.sfc
python tools/verify_font.py /chemin/original.sfc
python tools/verify_storage.py /chemin/original.sfc --version V44 --built-rom /chemin/fr_v44.sfc --build-report verification/build_report.json
```

Python 3 et Pillow. Sources : trente-huit lots JSON, corrections_v20.json
et startup_text.py. Les fichiers bilingues JSON/TSV et lecture_v44.txt sont
produits localement. Le constructeur refuse de remplacer une ancienne entrée
en fusionnant le lot 38. Encodage, balises et pauses, largeurs de 216 pixels,
pointeurs, allocation, checksum et aller-retour IPS contrôlés.
4646 lectures par les routines originales 65816, 16 contrôles de police,
14 de placement. Budget : 500 000 instructions par sélection.
140 blocs sur place, 34 relocalisés, 77312 octets libres.

## Essais et limites

Snes9x 1.63, commit 1bcc369e89f08243e0a462882fb1f3e42e51de3a.
Démarrage neuf, parcours initial, navigation, A puis reset puis B prolongé.
A affiche TERMINE / TOUT OK ; B affiche SAUV. RTC et SAUV. SRAM OK.
Les contrôles mémoire/SPC7110/SRAM/RTC, A/B/reset, naissance et horloge restent
en français. Les 32 modifications sont identiques à V43 ; signatures internes
intactes. La saisie détaillée de naissance reste documentée par V35.

58 cas ciblés atteignent leur terminateur exact ; 115 captures relues.
85 captures fixes identiques à V43, 0 différentes.
Navigation : navigation_comparison_v43_v44.json. Captures et empreintes :
verification/scenes_v44. Les pauses peuvent produire des images partielles
répétées d'une même page.

Le rendu ciblé ne valide pas naturellement les quêtes, achats, issues des choix,
délais, récompenses ou effets en combat. Conditions d'échec, toutes les limites
de calendrier, Snes9x 1.60 et matériel réel non testés. Effets 0A/CB, choix du
journal, horaires de Miho et autres différés restent intacts. Voir
deferred_reasons_v44.json, deferred_texts_v44.json, unprocessed_inventory_v44.json.
Les dialogues et événements ne sont pas complets.

## Reproduire

Construire V43 avec build_v43.py si la ROM ou les fichiers bilingues manquent.
Vérifier son empreinte publiée :
`4693478e747d1be3138464db6c7cf0c4aef0a5a6113fde6dc00315b3a07b660f`.
Rejouer run_scenario.py vers runs/fr_v43_reference44, puis run_navigation.py
vers runs/v43_navigation_reference44. Construire ensuite V44 pour que le
build_report.json corresponde à la ROM testée. Noyaux compilés localement :
snes9x_libretro_standard.so / snes9x_libretro_diagnostic.so dans emulator.

```bash
python verification/reproduction/run_version_checks.py --version v44 --tag final44 --render-workers 3 --source /chemin/original.sfc --emulator-root /chemin/emulator
python verification/reproduction/collect_evidence.py --version v44 --previous v43 --tag final44 --previous-tag reference44 --runs /chemin/emulator/runs --cases 58 --preview /chemin/contact --source /chemin/original.sfc --rom /chemin/emulator/fr_v44.sfc
```

Les rendus parallèles ont des dossiers isolés, le même état initial propre à
cette ROM et un terminateur exact par cas. Les dossiers existants sont refusés.
Le collecteur laisse la relecture en attente : inspecter les captures de la ROM
exacte avant validation. Voir COMPTE_RENDU_V44.md et emulation_report_v44.json.
