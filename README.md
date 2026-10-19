# Tengai Makyou Zero — Traduction française V45

**72 vrais nouveaux textes : 3 797 entrées intégrées.**
Lot 39 : Marina, sa maison et le salon du pays du Paon (235/236).
Les 3 725 entrées V44 et les 32 modifications françaises des écrans initiaux
sont conservées. La traduction reste partielle : dialogues et événements
encore à traiter, avant les menus.

## Installation

Appliquer **Tengai_Makyou_Zero_FR_V45.ips** directement à la ROM anglaise
originale, sans cumuler les patches. Taille : 7 340 032 octets sans en-tête.
SHA-256 : `eb07eed483f8f79ab64309c50ad0ef19560946b8e28fbd695470552ba68e356e`.
Le dépôt ne distribue ni ROM, ni sauvegarde d'état, ni noyau d'émulateur.

## Construction

```bash
python tools/build_v45.py /chemin/original.sfc --rom-out /chemin/fr_v45.sfc
python tools/verify_font.py /chemin/original.sfc
python tools/verify_storage.py /chemin/original.sfc --version V45 --built-rom /chemin/fr_v45.sfc --build-report verification/build_report.json
```

Python 3 et Pillow. Sources : trente-neuf lots JSON, corrections_v20.json
et startup_text.py. Les fichiers bilingues JSON/TSV et lecture_v45.txt sont
produits localement. Le constructeur refuse de remplacer une ancienne entrée
en fusionnant le lot 39. Encodage, balises et pauses, largeurs de 216 pixels,
pointeurs, allocation, checksum et aller-retour IPS contrôlés.
4719 lectures par les routines originales 65816, 16 contrôles de police,
14 de placement. Budget : 500 000 instructions par sélection.
142 blocs sur place, 34 relocalisés, 77312 octets libres.

## Essais et limites

Snes9x 1.63, commit 1bcc369e89f08243e0a462882fb1f3e42e51de3a.
Démarrage neuf, parcours initial, navigation, A puis reset puis B prolongé.
A affiche TERMINE / TOUT OK ; B affiche SAUV. RTC et SAUV. SRAM OK.
Les contrôles mémoire/SPC7110/SRAM/RTC, A/B/reset, naissance et horloge restent
en français. Les 32 modifications sont identiques à V44 ; signatures internes
intactes. La saisie détaillée de naissance reste documentée par V35.

72 cas ciblés atteignent leur terminateur exact ; 135 captures relues.
85 captures fixes identiques à V44, 0 différentes.
Navigation : navigation_comparison_v44_v45.json. Captures et empreintes :
verification/scenes_v45. Les pauses peuvent produire des images partielles
répétées d'une même page.

Le rendu ciblé ne valide pas naturellement les visites sur quatre jours, achats,
cadeaux, repos, effets d'objets ou issues des choix. Conditions d'échec, toutes les limites
de calendrier, Snes9x 1.60 et matériel réel non testés. Le choix d'achat de
maison B235-S008 et tous les différés antérieurs restent intacts. Voir
deferred_reasons_v45.json, deferred_texts_v45.json, unprocessed_inventory_v45.json.
Les dialogues et événements ne sont pas complets.

## Reproduire

Construire V44 avec build_v44.py si la ROM ou les fichiers bilingues manquent.
Vérifier son empreinte publiée :
`d860c12c0040a7f857312427c8446f380df4d260be122dc905432359fcaaa37c`.
Rejouer run_scenario.py vers runs/fr_v44_reference45, puis run_navigation.py
vers runs/v44_navigation_reference45. Construire ensuite V45 pour que le
build_report.json corresponde à la ROM testée. Noyaux compilés localement :
snes9x_libretro_standard.so / snes9x_libretro_diagnostic.so dans emulator.

```bash
python verification/reproduction/run_version_checks.py --version v45 --tag corrected45 --render-workers 3 --source /chemin/original.sfc --emulator-root /chemin/emulator
python verification/reproduction/collect_evidence.py --version v45 --previous v44 --tag corrected45 --previous-tag reference45 --runs /chemin/emulator/runs --cases 72 --preview /chemin/contact --source /chemin/original.sfc --rom /chemin/emulator/fr_v45.sfc
```

Les rendus parallèles ont des dossiers isolés, le même état initial propre à
cette ROM et un terminateur exact par cas. Les dossiers existants sont refusés.
Le collecteur laisse la relecture en attente : inspecter les captures de la ROM
exacte avant validation. Voir COMPTE_RENDU_V45.md et emulation_report_v45.json.
