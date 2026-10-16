# Tengai Makyou Zero — Traduction française V32

134 entrées ajoutées : 133 textes modifiés et une entrée vide conservée.
**2 885 entrées intégrées avec accents**. Les 2 751 entrées de V31 sont
inchangées. Variantes et répétitions sont comptées séparément. Premier jet
à relire depuis l'anglais fourni ; noms provisoires au glossaire.

Le lot couvre Double-Chance, Akamaru, l'arrivée de Subaru, le Mahamayuri
et le marché en plein air. Les variantes du thé rouge, les horaires, les
prix et la commission sont conservés. Les accès 226/227 partagent leurs
textes. Parmi les blocs traités, 47 messages restent différés. Le journal
210 reste à traiter ; les blocs 132 et 183 demeurent inchangés.

## Installation

Appliquer **Tengai_Makyou_Zero_FR_V32.ips** directement à une copie de la ROM
anglaise originale, sans cumuler les versions.

- Taille source : 7 340 032 octets, sans en-tête de copieur.
- SHA-256 : `eb07eed483f8f79ab64309c50ad0ef19560946b8e28fbd695470552ba68e356e`.

Le dépôt ne contient ni ROM, ni sauvegarde d'état, ni noyau binaire d'émulateur.

## Construction

```bash
python tools/build_v32.py /chemin/original.sfc --rom-out /chemin/v32.sfc
python tools/verify_font.py /chemin/original.sfc
python tools/verify_storage.py /chemin/original.sfc --version V32 --built-rom /chemin/v32.sfc --build-report verification/build_report.json
```

Python 3 et Pillow. Les vingt-sept lots JSON et corrections_v20.json sont les sources.
Le générateur produit les fichiers bilingues JSON/TSV et lecture_v32.txt localement.
3 675 lectures dans les routines originales 65816 passent, avec les chaînes
inchangées et les alias. Balises, largeur maximale de 216 pixels, pointeurs,
checksum, encodage et aller-retour IPS sont contrôlés. Le banc permet
500 000 instructions par sélection : certains indices anglais dépassent
l'ancien plafond de 100 000 (selection_checks_v31.json). Les 16 contrôles de police
et 14 contrôles du placement passent. 114 blocs sur place, 31 relocalisés,
80 848 octets libres ; le fichier anglais d'entrée n'est pas modifié.

## Essais dans Snes9x

Noyau standard Snes9x 1.63, commit 1bcc369e89f08243e0a462882fb1f3e42e51de3a.
Démarrage neuf et parcours du début. Contrôles A puis reset puis B prolongé
à 60 000 images : A affiche COMPLETE / ALL OK ; B indique OK pour
RTC BACKUP et S-RAM BACKUP (scenario_checks_v32.json).
Les 85 captures communes avec V31 sont identiques (comparison_v31_v32.json).
Menus et carte accessibles.
La version 1.60, le jeu complet et le matériel réel ne sont pas testés ici.

Cinquante-quatre essais ciblés couvrent le thé rouge, les indices, Akamaru,
Subaru, le cache-cache et son alias, le Mahamayuri, les panneaux et les
horaires de chaque boutique, les tarifs et les directions.
Ils utilisent la ROM finale inchangée et un noyau de diagnostic séparé qui
redirige une seule demande de dialogue vers le bloc et le message testés.
Les routines de lookup, sélection, lecture et rendu restent celles du jeu.
Le curseur doit atteindre le terminateur exact, puis les captures sont relues.

**Ces essais valident les textes et leur pagination, pas la progression naturelle,
les choix effectifs, les combats, les changements de groupe, les effets
du thé, les paiements, les achats, le calendrier ou le vol du Mahamayuri.** Les arrière-plans appartiennent au banc de test.
Rapport et images : verification/scenes_v32.

## Reproduire les essais ciblés

Compiler le noyau standard depuis https://github.com/snes9xgit/snes9x au commit
ci-dessus. NumPy et Pillow sont nécessaires pour le frontend. Le constructeur
de diagnostic restaure le code source et le noyau standard après compilation.

```bash
python verification/reproduction/build_diagnostic_core.py --source /chemin/snes9x --out /chemin/diagnostic.so
python verification/reproduction/prepare_dialogue_state.py --core /chemin/standard.so --rom /chemin/v32.sfc --out /chemin/etat_v32
python verification/reproduction/run_targeted_dialogues.py --core /chemin/diagnostic.so --rom /chemin/v32.sfc --state /chemin/etat_v32/dialogue_entry.state --out /chemin/essais_v32 --cases verification/reproduction/cases_v32.json
```

Créer l'état avec la ROM exacte à tester. Ne pas réutiliser un état d'une autre
version. Le noyau de diagnostic ne sert pas aux essais de progression.

Le lanceur commun refuse de réutiliser un répertoire de parcours existant :

```bash
python verification/reproduction/run_version_checks.py --version v32 --tag final --source /chemin/original.sfc --emulator-root /chemin/emulator
```

Ce dossier emulator contient fr_v32.sfc, les noyaux standard et de diagnostic
nommés comme dans SUIVI_FEOE.md, puis reçoit les parcours et journaux locaux.
Relire les captures avant de considérer les essais de rendu comme vérifiés.
