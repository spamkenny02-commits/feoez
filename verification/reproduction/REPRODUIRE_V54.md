# Reproduire V54 / lot 48

Utiliser la source anglaise privée sans en-tête, 7 340 032 octets, SHA256
`eb07eed483f8f79ab64309c50ad0ef19560946b8e28fbd695470552ba68e356e`.
Les ROMs, noyaux, états et dumps restent dans un répertoire privé.

## Construction et contrôles

```bash
python tools/build_v54.py /prive/source.sfc --rom-out /prive/emulator/fr_v54.sfc
python tools/verify_storage.py /prive/source.sfc --version V54 --built-rom /prive/emulator/fr_v54.sfc --build-report verification/build_report.json
python tools/audit_new_sources_lot48.py
python tools/verify_menu_help_lot48.py /prive/source.sfc --candidate /prive/emulator/fr_v54.sfc --out verification/native_menu_help_lot48.json
python tools/verify_save_labels_lot48.py /prive/source.sfc --candidate /prive/emulator/fr_v54.sfc --out verification/native_save_labels_lot48.json
python tools/verify_battle_banner_lot48.py /prive/source.sfc --candidate /prive/emulator/fr_v54.sfc --out verification/native_battle_banner_lot48.json
```

La reconstruction finale doit produire la ROM SHA256
`5b0a5430eab8b35ff8920952a8794a6e4828f0da8c5921d804aedf0f447c6ff7`
et l’IPS SHA256
`7442194a8404d490f1a3f8bf10999492df10ab91d6ecaf8cd902558acb3eec72`.
Le contrôle de préservation prend le rapport V53 épinglé, pas un rapport global
qui pourrait déjà être celui de V54. Les fichiers bilingues sont générés localement.

## Démarrage, navigation et rendus ciblés

Le noyau standard privé reste celui de V53 ; le noyau de dialogue/styles est
`snes9x_libretro_diagnostic_lot47_styles.so`, SHA256
`d4aef73ad947c6eb201708d1104f762e7b3374fc45a1de7001db9fdfbc74a394`.

```bash
python verification/reproduction/run_version_checks.py --version v54 --tag lot48p400c --source /prive/source.sfc --emulator-root /prive/emulator --render-workers 4 --compact-render --auto-close-captures --diagnostic-core /prive/emulator/snes9x_libretro_diagnostic_lot47_styles.so --suite verification/reproduction/suite_lot48_400.json --build-report verification/build_report_lot48_checkpoint.json
python verification/reproduction/collect_suite_evidence.py --runs /prive/emulator/runs --rom /prive/emulator/fr_v54.sfc --tag lot48p400c --suite verification/reproduction/suite_lot48_400.json --version v54 --build-report verification/build_report_lot48_checkpoint.json --reference-version v53 --reference-tag lot47p400d --reference-rom-sha256 ba2b468c2ba2f05ba542d421213c1564861fed7e35018704b88038608dcc2f7c
python verification/reproduction/make_suite_contact_sheets.py --images verification/scenes_v54
```

Les collecteurs ont un manifeste de provenance ; relire réellement les images
avant de marquer les rapports. `pack_suite_captures.py` contrôle les pixels et
empreintes des 510 fenêtres natives avant de retirer leurs copies publiques
redondantes. Les originaux complets restent privés. Les 32 planches V54 ont été
relues ; leur statut ne valide pas une autre ROM ou un autre rendu.

## Parcours naturel et Almanach

```bash
python verification/reproduction/run_controller_replay.py --core /prive/emulator/snes9x_libretro_standard.so --rom /prive/emulator/fr_v54.sfc --full-run /prive/emulator/runs/fr_v54_lot48p400c --commands verification/reproduction/commands_lot48_natural_combat.json --out /prive/emulator/runs/lot48_natural_combat_replay
python verification/reproduction/run_calendar_checkpoint.py --core /prive/emulator/snes9x_libretro_standard.so --rom /prive/emulator/fr_v54.sfc --full-run /prive/emulator/runs/fr_v54_lot48p400c --out /prive/emulator/runs/lot48_calendar_replay
python verification/reproduction/run_controller_replay.py --core /prive/emulator/snes9x_libretro_standard.so --rom /prive/emulator/fr_v54.sfc --full-run /prive/emulator/runs/fr_v54_lot48p400c --commands verification/reproduction/commands_lot48_menus.json --out /prive/emulator/runs/lot48_menus_replay
```

Ces séquences refusent un état de terrain d’une autre ROM. Le parcours standard
continu a été exécuté : 789 commandes, 26 953 frames, jusqu’à Woody #1, 6 ryo,
3 de vertu, kusa dango et retour terrain. Ses 397 captures comparées sont
identiques aux étapes exploratoires sur cette ROM et les scènes retenues ont
été relues. Cela ne valide pas chaque ennemi, événement, date ou fin du jeu.

## Vrai bandeau FD8B, fixtures explicitement synthétiques

Le script ordinaire `0x653c1` pousse le catalogue 19 et le sélecteur RAM43BB
vers FD8B. Son chemin adjacent catalogue 20 est observé dans le vrai combat.
Le vecteur FD8B (`C30DBC`) appelle C07722 ; C077AF copie avec X0, calcule la
largeur à 4D2C00 et centre dans 28 tuiles. Les aides utilisent X24 ; les libellés
de sauvegarde utilisent X27. Ne pas appliquer la même réserve aux trois formats.

```bash
python verification/reproduction/build_diagnostic_core.py --source /prive/snes9x --out /prive/emulator/snes9x_libretro_diagnostic_lot48_battle.so --trigger-block 20
python verification/reproduction/render_battle_captions_lot48.py --rom /prive/emulator/fr_v54.sfc --standard-core /prive/emulator/snes9x_libretro_standard.so --diagnostic-core /prive/emulator/snes9x_libretro_diagnostic_lot48_battle.so --full-run /prive/emulator/runs/fr_v54_lot48p400c --out /prive/emulator/runs/lot48_battle_captions_replay
python verification/reproduction/pack_battle_caption_captures.py --report /prive/emulator/runs/lot48_battle_captions_replay/report.json --out verification/battle_captions_lot48
```

Le noyau privé de cette fixture a le SHA256
`ee68469a9f9c3def4e138b3cdde41e1e9b85f4645fce2ffb214a7adc910fa658`.
Il redirige uniquement les arguments d’un nom de cible B020 vers B019. Les
185 cas passent le lecteur natif, le terminateur, le calcul de largeur et le
PPU ; les 184 bandeaux distincts ont été relus sur 12 planches. Cela ne prouve
pas que les 185 attaques ont été déclenchées naturellement.

`build_text_read_observer.py` est un observateur séparé, sans redirection,
activé par `FEOE_OBSERVE_TEXT_READS`. Son compilateur restaure aussi le cache
d’objets et le noyau d’origine ; les octets de ROM et de WRAM ne sont jamais
modifiés. Toujours fusionner stderr/stdout pour conserver les traces natives.
Les noyaux d’observation et de diagnostic ne sont pas distribués.
