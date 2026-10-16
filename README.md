# Tengai Makyou Zero — Traduction française V35

**Écrans de démarrage, naissance et horloge traduits : 32 occurrences.**
Les **3 160 entrées de dialogue** de V34 sont conservées sans modification.

Les contrôles SPC7110/SRAM/RTC, les instructions A/B/reset et les confirmations
sont en français. La naissance indique l'ordre mois–jour–année ; l'horloge
conserve le format AM/PM. Les sigles techniques restent lisibles.
Les signatures internes de sauvegarde sont conservées, distinctes des textes.

Le reste de la traduction est partiel : 50 messages différés et quatre invites
de débogage dans les blocs traités ; journal 210, blocs 235/236, menu 244/245
et bloc 253 encore à traiter. Les blocs 132 et 183 sont conservés.

## Installation

Appliquer **Tengai_Makyou_Zero_FR_V35.ips** directement à une copie de la ROM
anglaise originale, sans cumuler les versions.

- Taille source : 7 340 032 octets, sans en-tête de copieur.
- SHA-256 : `eb07eed483f8f79ab64309c50ad0ef19560946b8e28fbd695470552ba68e356e`.

Le dépôt ne contient ni ROM, ni sauvegarde d'état, ni noyau binaire d'émulateur.

## Construction

```bash
python tools/build_v35.py /chemin/original.sfc --rom-out /chemin/v35.sfc
python tools/verify_font.py /chemin/original.sfc
python tools/verify_storage.py /chemin/original.sfc --version V35 --built-rom /chemin/v35.sfc --build-report verification/build_report.json
```

Python 3 et Pillow. Les vingt-neuf lots JSON, corrections_v20.json et tools/startup_text.py sont les sources.
Le générateur produit les fichiers bilingues JSON/TSV et lecture_v35.txt localement.
3 968 lectures dans les routines originales 65816 passent, avec les chaînes
inchangées et les alias. Balises, largeur maximale de 216 pixels, pointeurs,
checksum, encodage et aller-retour IPS sont contrôlés. Le banc permet
500 000 instructions par sélection : certains indices anglais dépassent
l'ancien plafond de 100 000 (selection_checks_v31.json). Les 16 contrôles de police
et 14 contrôles du placement passent. 125 blocs sur place, 33 relocalisés,
80 656 octets libres ; le fichier anglais d'entrée n'est pas modifié.

## Essais dans Snes9x

Noyau standard Snes9x 1.63, commit 1bcc369e89f08243e0a462882fb1f3e42e51de3a.
Démarrage neuf et parcours du début. Contrôles A puis reset puis B prolongé
à 60 000 images : A affiche COMPLETE / ALL OK ; B indique OK pour
RTC BACKUP et S-RAM BACKUP (scenario_checks_v35.json).
Les 43 captures de saisie ont été relues. Le mois, le jour, l'année,
l'heure et les minutes ont été modifiés ; les choix Oui/Non, le retour aux
champs, le refus d'une naissance future et le démarrage après une date valide
ont été vérifiés. Les chiffres de 38 captures correspondent à V34 pour
les mêmes commandes, depuis des états propres à chaque ROM.

Sur 85 captures communes du parcours fixe : 30 identiques et 55 différentes,
incluant les traductions initiales et des écarts de phase ultérieurs. Les trois
écrans finaux de navigation sont identiques. Aucune équivalence temporelle
complète n'est annoncée. Voir comparison_v34_v35.json et COMPTE_RENDU_V35.md.
Snes9x 1.60, toutes les limites de dates, la sauvegarde hôte après arrêt
et le matériel réel ne sont pas testés.

Huit dialogues antérieurs sont aussi relus sur 13 captures, avec vérification
du terminateur exact. Ces essais redirigés ne valident pas la progression
naturelle du scénario. Les essais de saisie utilisent les commandes normales
du noyau standard, sans écriture en RAM.

Rapports : verification/startup_v35, verification/startup_text_v35.json,
verification/startup_numeric_comparison_v35.json et verification/scenes_v35.

## Reproduire les essais ciblés

Compiler le noyau standard depuis https://github.com/snes9xgit/snes9x au commit
ci-dessus. NumPy et Pillow sont nécessaires pour le frontend. Le constructeur
de diagnostic restaure le code source et le noyau standard après compilation.

```bash
python verification/reproduction/build_diagnostic_core.py --source /chemin/snes9x --out /chemin/diagnostic.so
python verification/reproduction/prepare_dialogue_state.py --core /chemin/standard.so --rom /chemin/v35.sfc --out /chemin/etat_v35
python verification/reproduction/run_targeted_dialogues.py --core /chemin/diagnostic.so --rom /chemin/v35.sfc --state /chemin/etat_v35/dialogue_entry.state --out /chemin/essais_v35 --cases verification/reproduction/cases_v35.json
```

Créer l'état avec la ROM exacte à tester. Ne pas réutiliser un état d'une autre
version. Le noyau de diagnostic ne sert pas aux essais de progression.

Le lanceur commun refuse de réutiliser un répertoire de parcours existant :

```bash
python verification/reproduction/run_version_checks.py --version v35 --tag final --source /chemin/original.sfc --emulator-root /chemin/emulator
```

Ce dossier emulator contient fr_v35.sfc, les noyaux standard et de diagnostic
nommés comme dans SUIVI_FEOE.md, puis reçoit les parcours et journaux locaux.
Relire les captures avant de considérer les essais de rendu comme vérifiés.

Pour reproduire les branches de saisie avec le noyau standard :

```bash
python verification/reproduction/run_startup_inputs.py --core /chemin/standard.so --rom /chemin/v35.sfc --out /chemin/saisie_v35
python verification/reproduction/compare_startup_inputs.py --before /chemin/saisie_v34 --after /chemin/saisie_v35 --out /chemin/comparaison.json
```

Créer le contrôle V34 avec le même script et sa ROM reconstruite. Chaque
parcours refuse un dossier existant et crée ses états avec sa propre ROM.
