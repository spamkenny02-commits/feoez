# Tengai Makyou Zero — Traduction française V52

**Lot 46 complet : 400 nouveaux textes distincts, phase 1.**
393 sources bornées (394 occurrences, dont un alias non recompté), plus
7 libellés natifs de l’Almanach. Les 4 987 entrées V51 sont conservées ;
5 381 occurrences bornées sont intégrées. Dialogues, calendrier et formats
spéciaux restent partiels ; recherche exhaustive et relecture globale à venir.

## Installation

Appliquer **Tengai_Makyou_Zero_FR_V52.ips** directement à la ROM anglaise
originale, sans cumuler les patches. Taille : 7 340 032 octets sans en-tête.
SHA-256 source : `eb07eed483f8f79ab64309c50ad0ef19560946b8e28fbd695470552ba68e356e`.
Le dépôt ne distribue ni ROM, ni noyau, ni état, ni dump mémoire.

## Construction

```bash
python tools/build_v52.py /chemin/original.sfc --rom-out /chemin/emulator/fr_v52.sfc
python tools/verify_font.py /chemin/original.sfc
python tools/verify_lot46_checkpoint.py /chemin/original.sfc /chemin/emulator/fr_v52.sfc
python tools/verify_storage.py /chemin/original.sfc --version V52 --built-rom /chemin/emulator/fr_v52.sfc --build-report verification/build_report.json
```

Python 3 et Pillow. Le constructeur produit les fichiers bilingues JSON/TSV
et lecture_v52.txt à partir des sources des 46 lots. Il préserve V51 et les
32 modifications initiales. Encodage, commandes, pointeurs, alias, placement,
réserves, collisions, marqueurs SPC7110, checksum et aller-retour IPS vérifiés.
Les noms, nombres et prédictions ont des contrats de largeur distincts.

## Essais et limites

6 365 lectures natives du constructeur ; 788 lectures source/sortie des ajouts.
488 rendus ciblés frais, 561 captures de texte distinctes relues, cinq vues
système relues. Démarrage neuf, navigation et A/reset/B exécutés ; 85 captures
fixes et sept vues de navigation identiques à V51. Almanach réel observé au
22/12/1995 avec ses sept libellés français et sa notice B018-S182 française.
Voir [COMPTE_RENDU_V52.md](COMPTE_RENDU_V52.md),
[preuves](verification/emulation_report_v52.json) et
[couverture](verification/coverage_v52.json).

Les fixtures de substitution sont synthétiques : elles ne prouvent pas les
producteurs naturels, vrais sélecteurs, dates, récompenses, musique ou effets.
Les variantes de menu des catalogues restent à harmoniser. La phase 1 continue,
puis viennent la recherche complète des oublis et la relecture globale.
L’inventaire borné exclut notamment le bloc 42 non borné et les graphismes ;
son compteur ne prouve pas la couverture du jeu. Snes9x 1.60 et matériel réel
non testés. Anecdotes historiques traduites selon la source, sans révision inventée.

## Reproduire

Noyaux standard/diagnostic compilés localement : Snes9x 1.63,
commit 1bcc369e89f08243e0a462882fb1f3e42e51de3a.
La suite décrit les noyaux attendus et vérifie leurs empreintes.

```bash
python verification/reproduction/build_diagnostic_core.py --help
python verification/reproduction/run_version_checks.py --version v52 --tag lot46p400b --render-workers 4 --compact-render --auto-close-captures --diagnostic-core /chemin/emulator/snes9x_libretro_diagnostic_v51.so --source /chemin/original.sfc --emulator-root /chemin/emulator --build-report verification/build_report.json --suite verification/reproduction/suite_lot46_400.json
python verification/reproduction/run_calendar_checkpoint.py --core /chemin/emulator/snes9x_libretro_standard.so --rom /chemin/emulator/fr_v52.sfc --full-run /chemin/emulator/runs/fr_v52_lot46p400b --out /chemin/emulator/runs/v52_calendar_lot46p400b
python verification/reproduction/collect_suite_evidence.py --runs /chemin/emulator/runs --rom /chemin/emulator/fr_v52.sfc --tag lot46p400b --suite verification/reproduction/suite_lot46_400.json
```

Chaque rejeu utilise un nouveau tag et un état préparé sur la ROM exacte.
La collecte laisse la relecture en attente : lire les captures avant validation.
La suite contient 105 cas simples, 128 profils numériques, 12 prédictions et
243 substitutions de noms ; ces scénarios ne sont pas des ajouts au compteur.
L’option de slots doit être explicitement activée lors de la compilation du
noyau diagnostique ; voir son script de construction et les empreintes de suite.
Les rapports checkpoint/lot46p83 sont historiques ; ils ne valident pas V52.
