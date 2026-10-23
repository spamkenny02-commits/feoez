# Reproduire V55 — lot49

Source privée anglaise sans en-tête :7340032 octets, SHA256
`eb07eed483f8f79ab64309c50ad0ef19560946b8e28fbd695470552ba68e356e`.
ROM attendue :`2631d90bd0f2b0ed927055143117525517d06f15f29511439d6e76acdc371e4c`.
Les ROM, noyaux, états et dumps restent privés. Python3, Pillow, NumPy,
compilateur C++/make pour Snes9x sont nécessaires.

## Construction et contrôles natifs

```bash
python tools/build_v55.py "$SOURCE" --rom-out "$EM/fr_v55.sfc"
python tools/verify_storage.py "$SOURCE" --version V55 --built-rom "$EM/fr_v55.sfc" --build-report verification/build_report.json
python tools/audit_new_sources_lot49.py
python tools/audit_prior_sources_lot49.py
python tools/verify_battle_banner_lot49.py "$SOURCE" --candidate "$EM/fr_v55.sfc" --out "$EM/native_banners.json"
python tools/verify_native_credits_lot49.py "$EM/fr_v55.sfc" --out "$EM/native_credits.json"
python tools/verify_credits_line_start_lot49.py "$EM/fr_v55.sfc" --out "$EM/native_credit_base.json"
python tools/verify_scroll_menu_lot49.py "$EM/fr_v55.sfc" --out "$EM/native_scroll.json"
```

Le constructeur régénère les JSON bilingues des versions précédentes s’ils
manquent. Le rapport V54 épinglé fournit l’ordre d’allocation. Les6534 textes
précédents restent inchangés ;235 nouvelles occurrences bornées sont ajoutées.
Le manifeste canonique contient400 sources :231 bornées,114 crédits,
51 textes graphiques et4 textes natifs. Les alias et fragments sont exclus.

## Noyaux privés

Utiliser les sources Snes9x au commit
`1bcc369e89f08243e0a462882fb1f3e42e51de3a`, fichier cpuexec.cpp original
SHA256 `37b2f4ece0ff797b616fbeee6084c42a6198d477a08eb1837b5445abacd2c56b`.
Construire le noyau standard avec `make -C "$SNES/libretro" -j4`, puis le
copier dans `$EM/snes9x_libretro_standard.so`. Le binaire standard reconstruit
pour ces essais a l’empreinte `f15fbd2724a62c5f9df0327cb41f07a1b111dfe966c65b27e0f21c06ad3e05b6`.
Les constructeurs de diagnostic restaurent les sources, objets et binaire standard.

```bash
python verification/reproduction/build_diagnostic_core.py --source "$SNES" --out "$EM/snes9x_libretro_diagnostic_lot49_styles.so" --enable-slot-fixtures --enable-style-slot-fixtures
python verification/reproduction/build_diagnostic_core.py --source "$SNES" --out "$EM/snes9x_libretro_diagnostic_lot49_battle.so" --trigger-block 20
python verification/reproduction/build_lot49_diagnostic_core.py --source "$SNES" --out "$EM/snes9x_libretro_diagnostic_lot49_context.so"
```

Les empreintes des trois noyaux figurent dans emulation_report_v55.json.
Les fixtures ne prouvent pas la progression naturelle ni toutes les branches.

## Essais frais sur une seule ROM

Les répertoires de sortie doivent être nouveaux ; changer le tag en cas de
reprise. Les états d’une autre ROM sont interdits.

```bash
python verification/reproduction/run_version_checks.py --version v55 --tag recoveryf --source "$SOURCE" --emulator-root "$EM" --render-workers 4 --compact-render --auto-close-captures --diagnostic-core "$EM/snes9x_libretro_diagnostic_lot49_styles.so" --suite verification/reproduction/suite_lot49_400.json --build-report verification/build_report_lot49_checkpoint.json
python verification/reproduction/render_battle_captions_lot49.py --rom "$EM/fr_v55.sfc" --standard-core "$EM/snes9x_libretro_standard.so" --diagnostic-core "$EM/snes9x_libretro_diagnostic_lot49_battle.so" --full-run "$EM/runs/fr_v55_recoveryf" --out "$EM/runs/v55_banners_recoveryf" --workers 4
python verification/reproduction/render_ui_lot49.py --rom "$EM/fr_v55.sfc" --core "$EM/snes9x_libretro_standard.so" --grid-core "$EM/snes9x_libretro_diagnostic_lot49_context.so" --state "$EM/runs/fr_v55_recoveryf/field_verified.state" --out "$EM/runs/v55_ui_recoveryf_final"
python verification/reproduction/render_credits_lot49.py --rom "$EM/fr_v55.sfc" --core "$EM/snes9x_libretro_diagnostic_lot49_context.so" --state "$EM/runs/v55_dialogue_recoveryf/dialogue_entry.state" --out "$EM/runs/v55_credits_recoveryf_clean"
python verification/reproduction/collect_credits_lot49.py --source "$SOURCE" --rom "$EM/fr_v55.sfc" --images "$EM/runs/v55_credits_recoveryf_clean" --out "$EM/review_credits"
python verification/reproduction/run_controller_replay.py --core "$EM/snes9x_libretro_standard.so" --rom "$EM/fr_v55.sfc" --full-run "$EM/runs/fr_v55_recoveryf" --commands verification/reproduction/commands_lot48_natural_combat.json --out "$EM/runs/v55_natural_recoveryf"
python verification/reproduction/run_calendar_checkpoint.py --core "$EM/snes9x_libretro_standard.so" --rom "$EM/fr_v55.sfc" --full-run "$EM/runs/fr_v55_recoveryf" --out "$EM/runs/v55_calendar_recoveryf"
```

Le générique suit les629 enregistrements jusqu’à4D668C ;122 occurrences
traduites sont comparées aux masques complets de la police native dans les
captures PPU. La fixture établit explicitement le contexte d’écran via FD-A2 ;
elle ne parcourt ni le dernier boss ni la fin naturelle. Le correctif propre au
générique vide le glyphe partiel avant de mémoriser1C91 et efface27 colonnes.

Les bandeaux FD8B utilisent une redirection diagnostique du nom cible B020.
Les235 cas n’établissent pas que chaque action ou ennemi a été rencontré.
Les36 noms courts ont leur cache24px ; les formes complètes B004/B006 restent
intactes. Trois grilles emploient des identifiants appris synthétiques.

La comparaison V54 nécessite de reconstruire sa ROM exacte, puis de relancer
run_scenario.py et run_navigation.py avec le tag de référence `recoveryref`.
collect_suite_evidence.py accepte --reference-version v54,
--reference-tag recoveryref et l’empreinte V54 épinglée. Les85+7 comparaisons
ne représentent jamais une identité pixel ou une couverture globale du jeu.
Les planches ne deviennent relues qu’après inspection effective.
