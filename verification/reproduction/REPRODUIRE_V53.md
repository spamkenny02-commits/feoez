# Reproduire V53

Utiliser la source anglaise sans en-tête de7 340 032octets, SHA256
`eb07eed483f8f79ab64309c50ad0ef19560946b8e28fbd695470552ba68e356e`.
Les ROM, noyaux, états et dumps restent privés. Python3/Pillow requis.

```bash
python tools/build_v53.py /prive/source.sfc --rom-out /prive/emulator/fr_v53.sfc
python tools/verify_storage.py /prive/source.sfc --version V53 --built-rom /prive/emulator/fr_v53.sfc --build-report verification/build_report.json
python tools/verify_battle_result_lot47.py /prive/emulator/fr_v53.sfc --out verification/battle_result_lot47_checks.json
```

Sortie attendue : ROM `ba2b468c2ba2f05ba542d421213c1564861fed7e35018704b88038608dcc2f7c`,
IPS `0ac14f5583ba54ab3a7b00156a3dac61f4274b9fff14b0f9436c47713f7c9272`.
Le rapport d’exécution reste distinct du rapport de construction.

Le noyau standard doit être compilé séparément. Le noyau de diagnostic est
opt-in, à partir de la source Snes9x révision1bcc369e utilisée par les preuves :

```bash
python verification/reproduction/build_diagnostic_core.py --source /prive/snes9x51 --out /prive/emulator/snes9x_libretro_diagnostic_lot47_styles.so --enable-slot-fixtures --enable-style-slot-fixtures
python verification/reproduction/prepare_lot47_suite.py --rom /prive/emulator/fr_v53.sfc --build-report verification/build_report_lot47_checkpoint.json --diagnostic-core /prive/emulator/snes9x_libretro_diagnostic_lot47_styles.so
python verification/reproduction/run_version_checks.py --version v53 --tag reproduction53 --source /prive/source.sfc --emulator-root /prive/emulator --render-workers 4 --compact-render --auto-close-captures --diagnostic-core /prive/emulator/snes9x_libretro_diagnostic_lot47_styles.so --suite verification/reproduction/suite_lot47_400.json --build-report verification/build_report_lot47_checkpoint.json
```

Les dossiers de preuve doivent être neufs ; choisir un autre tag pour répéter.
Le noyau synthétique accepte les styles08/0A dans les slots, sans les confondre
avec des noms/nombres. Sa compilation restaure le CPP et la bibliothèque source.
Voir diagnostic_core_build_v53.json pour les empreintes de cette compilation.

`run_calendar_checkpoint.py` ouvre ensuite l’Almanach par manette depuis
`runs/fr_v53_reproduction53/field_verified.state` de cette même ROM, avec
`--full-run /prive/emulator/runs/fr_v53_reproduction53` et un `--out` neuf.
La date rejouée22/12/1995 n’est pas une validation des autres dates.

`collect_suite_evidence.py --version v53` rassemble les images compactes et
vérifie la consommation des400 fournisseurs canoniques. Pour la comparaison
V52, conserver aussi ses preuves privées lot46p400b et son empreinte exacte.
Le collecteur laisse volontairement la relecture visuelle en attente : ouvrir
et lire les captures, toutes les pages et les variables avant validation.
Les fixtures ne prouvent ni les parcours naturels, ni les vrais sélecteurs,
échéances, récompenses, champs de sauvegarde ou synchronisations musicales.

Après collecte et relecture, `pack_suite_captures.py --images verification/scenes_v53
--manifest verification/scenes_v53/contact_sheets.json` reproduit les40 planches
relues si les619 empreintes des captures correspondent exactement.
