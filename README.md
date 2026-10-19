# Tengai Makyou Zero — Traduction française V42

**59 vrais nouveaux textes : 3 542 entrées intégrées.**
Lot 36 : village des Paillettes d'Or (91, alias 92), Basara (99), ermites (102).
Les 3 483 entrées V41 et les 32 modifications françaises des écrans initiaux
sont conservées. La traduction reste partielle : dialogues et événements
encore à traiter, avant les menus.

## Installation

Appliquer **Tengai_Makyou_Zero_FR_V42.ips** directement à la ROM anglaise
originale, sans cumuler les patches. Taille : 7 340 032 octets sans en-tête.
SHA-256 : `eb07eed483f8f79ab64309c50ad0ef19560946b8e28fbd695470552ba68e356e`.
Le dépôt ne distribue ni ROM, ni sauvegarde d'état, ni noyau d'émulateur.

## Construction

```bash
python tools/build_v42.py /chemin/original.sfc --rom-out /chemin/fr_v42.sfc
python tools/verify_font.py /chemin/original.sfc
python tools/verify_storage.py /chemin/original.sfc --version V42 --built-rom /chemin/fr_v42.sfc --build-report verification/build_report.json
```

Python 3 et Pillow. Sources : les trente-six lots JSON, corrections_v20.json
et startup_text.py. Les fichiers bilingues JSON/TSV et lecture_v42.txt sont
produits localement. Encodage, balises et pauses, largeurs jusqu'à 216 pixels,
pointeurs, allocation, checksum et aller-retour IPS sont contrôlés.
4 433 lectures par les routines originales 65816, 16 contrôles de police
et 14 de placement réussissent. Budget : 500 000 instructions par sélection.
138 blocs sur place, 34 relocalisés, 77,312 octets libres.

## Essais et limites

Snes9x 1.63, commit 1bcc369e89f08243e0a462882fb1f3e42e51de3a.
Démarrage neuf, parcours initial, navigation, A puis reset puis B prolongé
à 60 000 images : A affiche TERMINE / TOUT OK, B SAUV. RTC et SAUV. SRAM OK.
Les contrôles mémoire/SPC7110/SRAM/RTC, A/B/reset, naissance et horloge
restent en français ; les signatures internes de sauvegarde restent intactes.
La saisie détaillée de naissance reste documentée par V35 ; V42 compare les
32 modifications octet par octet à V41 et rejoue le démarrage standard.

59 cas ciblés atteignent chacun leur terminateur exact ; 137 captures finales
relues. 85 captures fixes du début identiques à V41, 0 différentes.
Navigation : voir navigation_comparison_v41_v42.json. Les captures et leurs
empreintes sont dans verification/scenes_v42. Les pauses peuvent produire
plusieurs captures partielles d'une même page.

Le rendu ciblé redirige une demande de dialogue : il ne valide pas les quêtes
naturelles, achats, échanges, duels, récompenses ou effets en combat. Le choix
Combattre/Partir garde la ligne d'origine et sa seconde colonne à un pixel près ;
sa sélection effective n'est pas testée. Conditions d'échec, toutes les limites
de calendrier, Snes9x 1.60 et matériel réel ne sont pas testés.

B091-S001/002/026/035, B099-S001/002/003/011/S014-S019 et B102-S001/003
restent intacts : prix, fragments horaires, chant ou questions à colonnes.
Les différés antérieurs sont conservés. Motifs : deferred_reasons_v42.json.
Inventaires : unprocessed_inventory_v42.json et deferred_texts_v42.json.

## Reproduire

Reconstruire d'abord V41 avec build_v41.py et rejouer run_scenario.py vers
runs/fr_v41_reference42, puis run_navigation.py vers runs/v41_navigation_reference42.
La V41 reconstruite doit retrouver l'empreinte publiée
`fa4d3de52f6abfc2dd08c5afc5186dbb23f536dff34af5308b562623d87a3dcf`.
Reconstruire ensuite V42 afin que build_report.json corresponde à cette ROM.
Les noyaux standard et diagnostic doivent être compilés localement et nommés
snes9x_libretro_standard.so / snes9x_libretro_diagnostic.so dans emulator.

```bash
python verification/reproduction/run_version_checks.py --version v42 --tag corrected42 --source /chemin/original.sfc --emulator-root /chemin/emulator
python verification/reproduction/collect_evidence.py --version v42 --previous v41 --tag corrected42 --previous-tag reference42 --runs /chemin/emulator/runs --cases 59 --preview /chemin/contact --source /chemin/original.sfc --rom /chemin/emulator/fr_v42.sfc
```

Les dossiers de parcours existants sont refusés : choisir un nouveau tag pour
un nouvel essai. Le collecteur laisse la relecture visuelle en attente ; elle
doit être effectuée sur les captures de la ROM exacte avant validation.
Voir COMPTE_RENDU_V42.md et verification/emulation_report_v42.json.
