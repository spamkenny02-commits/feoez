# Tengai Makyou Zero — Traduction française V55

**Lot49 complet :400 nouveaux textes distincts, phase1.**
231 sources bornées,114 du générique,51 graphiques et4 natives.
Les6534 occurrences V54 sont préservées ;total6769 occurrences bornées.
25 abréviations d’affichage corrigées, sans recompter les noms complets.

## Installation

Appliquer **Tengai_Makyou_Zero_FR_V55.ips** directement à la ROM anglaise
originale sans en-tête,7340032 octets, sans cumuler les patches.
SHA256 source :`eb07eed483f8f79ab64309c50ad0ef19560946b8e28fbd695470552ba68e356e`.
SHA256 ROM V55 :`2631d90bd0f2b0ed927055143117525517d06f15f29511439d6e76acdc371e4c`.
Ni ROM, ni noyau, ni état, ni dump mémoire ne sont distribués.

## Construction et essais

```bash
python tools/build_v55.py /chemin/original.sfc --rom-out /chemin/emulator/fr_v55.sfc
python tools/verify_storage.py /chemin/original.sfc --version V55 --built-rom /chemin/emulator/fr_v55.sfc --build-report verification/build_report.json
python tools/audit_new_sources_lot49.py
python tools/audit_prior_sources_lot49.py
```

[Reproduction des essais](verification/reproduction/REPRODUIRE_V55.md).
7602 lectures natives,235 copies/largeurs de bandeaux,629 copies du générique,
24 cas du nettoyage de glyphes et36 paires de noms abrégés/complets.
Démarrage A/reset/B et navigation ;235+235 rendus ciblés,466 captures relues
sur30 planches. Générique complet en fixture :122 occurrences traduites
comparées aux pixels natifs et relues sur8 planches. Menus réels, grilles
synthétiques, premier combat naturel et Almanach22/12/1995 contrôlés.

## Couverture et limites

**La traduction complète du jeu n’est pas achevée.** Phase1 reste ouverte ;
recherche exhaustive des oublis et relecture globale restent à faire.
Le compteur borné comprend menus, vides et debug ;il ne mesure pas le jeu.
Des commandes de Stratégie et noms d’objets anglais restent visibles.
Le bloc42 non borné, les autres graphismes, fins/branches/dates, sélecteurs et
synchronisation des chansons restent à contrôler. Les fixtures n’établissent
ni la fin naturelle ni tous les déclenchements de combat.

[Suivi](SUIVI_FEOE.md) · [Bilan V55](COMPTE_RENDU_V55.md) ·
[Glossaire](glossaire_et_style.md) · [Couverture](verification/coverage_v55.json)
