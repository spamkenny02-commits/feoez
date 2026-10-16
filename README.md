# Tengai Makyou Zero — Traduction française V31

150 entrées ajoutées : 149 textes modifiés et une entrée de ponctuation
conservée. **2 751 entrées intégrées avec accents**. Les 2 601 entrées de V30
sont inchangées. Variantes et répétitions sont comptées séparément.
Premier jet à relire depuis l'anglais fourni ; noms provisoires au glossaire.

Le lot couvre les dialogues de fin, les ermites du pays du Paon, les indices
de l'ermite Bouddhiste, le Temple de la Pluie et Double-Chance. L'ordre des
fusions, les directions, les durées et les commandes sont conservés.
Les accès 217/218 partagent leurs textes. Parmi les blocs traités, 41 messages
restent différés, dont B221-S022 et son fragment x5. Le journal 210 reste à
traiter ; les blocs 132 et 183 demeurent inchangés.

## Installation

Appliquer **Tengai_Makyou_Zero_FR_V31.ips** directement à une copie de la ROM
anglaise originale, sans cumuler les versions.

- Taille source : 7 340 032 octets, sans en-tête de copieur.
- SHA-256 : `eb07eed483f8f79ab64309c50ad0ef19560946b8e28fbd695470552ba68e356e`.

Le dépôt ne contient ni ROM, ni sauvegarde d'état, ni noyau binaire d'émulateur.

## Construction

```bash
python tools/build_v31.py /chemin/original.sfc --rom-out /chemin/v31.sfc
python tools/verify_font.py /chemin/original.sfc
python tools/verify_storage.py /chemin/original.sfc --version V31 --built-rom /chemin/v31.sfc --build-report verification/build_report.json
```

Python 3 et Pillow. Les vingt-six lots JSON et corrections_v20.json sont les sources.
Le générateur produit les fichiers bilingues JSON/TSV et lecture_v31.txt localement.
3 532 lectures dans les routines originales 65816 passent, avec les chaînes
inchangées et les alias. Balises, largeur maximale de 216 pixels, pointeurs,
checksum, encodage et aller-retour IPS sont contrôlés. Le banc permet
500 000 instructions par sélection : certains indices anglais dépassent
l'ancien plafond de 100 000 (selection_checks_v31.json). Les 16 contrôles de police
et 14 contrôles du placement passent. 107 blocs sur place, 31 relocalisés,
80 848 octets libres ; le fichier anglais d'entrée n'est pas modifié.

## Essais dans Snes9x

Noyau standard Snes9x 1.63, commit 1bcc369e89f08243e0a462882fb1f3e42e51de3a.
Démarrage neuf et parcours du début. Contrôles A puis reset puis B prolongé
à 60 000 images : A affiche COMPLETE / ALL OK ; B indique OK pour
RTC BACKUP et S-RAM BACKUP (scenario_checks_v31.json).
Sur 85 captures communes avec V30 : 85 identiques,
0 avec une différence limitée à l'horloge. Menus et carte accessibles.
La version 1.60, le jeu complet et le matériel réel ne sont pas testés ici.

Soixante essais ciblés couvrent les fins, le choix Oui/Non et son alias,
les panneaux, la bague de Hisui, les fusions, les indices, les ermites,
la larme du Paon, les tarifs, la pluie rouge et les pousses de massette.
Ils utilisent la ROM finale inchangée et un noyau de diagnostic séparé qui
redirige une seule demande de dialogue vers le bloc et le message testés.
Les routines de lookup, sélection, lecture et rendu restent celles du jeu.
Le curseur doit atteindre le terminateur exact, puis les captures sont relues.

**Ces essais valident les textes et leur pagination, pas la progression naturelle,
les choix effectifs de fin, les combats, les effets des sorts,
les paiements, les récompenses ou le vol du Mahamayuri.** Les arrière-plans appartiennent au banc de test.
Rapport et images : verification/scenes_v31.

## Reproduire les essais ciblés

Compiler le noyau standard depuis https://github.com/snes9xgit/snes9x au commit
ci-dessus. NumPy et Pillow sont nécessaires pour le frontend. Le constructeur
de diagnostic restaure le code source et le noyau standard après compilation.

```bash
python verification/reproduction/build_diagnostic_core.py --source /chemin/snes9x --out /chemin/diagnostic.so
python verification/reproduction/prepare_dialogue_state.py --core /chemin/standard.so --rom /chemin/v31.sfc --out /chemin/etat_v31
python verification/reproduction/run_targeted_dialogues.py --core /chemin/diagnostic.so --rom /chemin/v31.sfc --state /chemin/etat_v31/dialogue_entry.state --out /chemin/essais_v31 --cases verification/reproduction/cases_v31.json
```

Créer l'état avec la ROM exacte à tester. Ne pas réutiliser un état d'une autre
version. Le noyau de diagnostic ne sert pas aux essais de progression.
