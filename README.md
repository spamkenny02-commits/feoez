# Tengai Makyou Zero — Traduction française V33

152 entrées ajoutées : 151 textes modifiés et une entrée vide conservée.
**3 037 entrées intégrées avec accents**. Les 2 885 entrées de V32 sont
inchangées. Variantes et répétitions sont comptées séparément. Premier jet
à relire depuis l'anglais fourni ; noms provisoires au glossaire.

Le lot couvre le sanctuaire du Paon, les fêtes, les articles de la Presse
du Paon et la vallée de Pierre. Les menus d'articles gardent leurs colonnes
et lignes. Les articles conservent leurs rumeurs et affirmations farfelues.
Parmi les blocs traités, 48 messages restent différés. Le journal 210 et
les blocs 235/236 restent à traiter ; les blocs 132 et 183 sont inchangés.

## Installation

Appliquer **Tengai_Makyou_Zero_FR_V33.ips** directement à une copie de la ROM
anglaise originale, sans cumuler les versions.

- Taille source : 7 340 032 octets, sans en-tête de copieur.
- SHA-256 : `eb07eed483f8f79ab64309c50ad0ef19560946b8e28fbd695470552ba68e356e`.

Le dépôt ne contient ni ROM, ni sauvegarde d'état, ni noyau binaire d'émulateur.

## Construction

```bash
python tools/build_v33.py /chemin/original.sfc --rom-out /chemin/v33.sfc
python tools/verify_font.py /chemin/original.sfc
python tools/verify_storage.py /chemin/original.sfc --version V33 --built-rom /chemin/v33.sfc --build-report verification/build_report.json
```

Python 3 et Pillow. Les vingt-huit lots JSON et corrections_v20.json sont les sources.
Le générateur produit les fichiers bilingues JSON/TSV et lecture_v33.txt localement.
3 828 lectures dans les routines originales 65816 passent, avec les chaînes
inchangées et les alias. Balises, largeur maximale de 216 pixels, pointeurs,
checksum, encodage et aller-retour IPS sont contrôlés. Le banc permet
500 000 instructions par sélection : certains indices anglais dépassent
l'ancien plafond de 100 000 (selection_checks_v31.json). Les 16 contrôles de police
et 14 contrôles du placement passent. 120 blocs sur place, 31 relocalisés,
80 848 octets libres ; le fichier anglais d'entrée n'est pas modifié.

## Essais dans Snes9x

Noyau standard Snes9x 1.63, commit 1bcc369e89f08243e0a462882fb1f3e42e51de3a.
Démarrage neuf et parcours du début. Contrôles A puis reset puis B prolongé
à 60 000 images : A affiche COMPLETE / ALL OK ; B indique OK pour
RTC BACKUP et S-RAM BACKUP (scenario_checks_v33.json).
Sur 85 captures communes avec V32 : 59 identiques,
26 avec des écarts de phase d’animation ou de dialogue ; cause non établie
(comparison_v32_v33.json). Les trois écrans finaux de navigation sont identiques.
Menus et carte accessibles.
La version 1.60, le jeu complet et le matériel réel ne sont pas testés ici.

Soixante-trois essais ciblés couvrent les fêtes, les menus et articles,
les variantes du sanctuaire, les indices, les récompenses annoncées,
la pierre du Paon, les six ermites et la vallée de Pierre.
Ils utilisent la ROM finale inchangée et un noyau de diagnostic séparé qui
redirige une seule demande de dialogue vers le bloc et le message testés.
Les routines de lookup, sélection, lecture et rendu restent celles du jeu.
Le curseur doit atteindre le terminateur exact, puis les captures sont relues.

**Ces essais valident les textes et leur pagination, pas la progression naturelle,
la sélection effective des articles, les combats, les récompenses,
les effets du thé ou de la pierre, les paiements et le calendrier.** Les arrière-plans appartiennent au banc de test.
Rapport et images : verification/scenes_v33.

## Reproduire les essais ciblés

Compiler le noyau standard depuis https://github.com/snes9xgit/snes9x au commit
ci-dessus. NumPy et Pillow sont nécessaires pour le frontend. Le constructeur
de diagnostic restaure le code source et le noyau standard après compilation.

```bash
python verification/reproduction/build_diagnostic_core.py --source /chemin/snes9x --out /chemin/diagnostic.so
python verification/reproduction/prepare_dialogue_state.py --core /chemin/standard.so --rom /chemin/v33.sfc --out /chemin/etat_v33
python verification/reproduction/run_targeted_dialogues.py --core /chemin/diagnostic.so --rom /chemin/v33.sfc --state /chemin/etat_v33/dialogue_entry.state --out /chemin/essais_v33 --cases verification/reproduction/cases_v33.json
```

Créer l'état avec la ROM exacte à tester. Ne pas réutiliser un état d'une autre
version. Le noyau de diagnostic ne sert pas aux essais de progression.

Le lanceur commun refuse de réutiliser un répertoire de parcours existant :

```bash
python verification/reproduction/run_version_checks.py --version v33 --tag final --source /chemin/original.sfc --emulator-root /chemin/emulator
```

Ce dossier emulator contient fr_v33.sfc, les noyaux standard et de diagnostic
nommés comme dans SUIVI_FEOE.md, puis reçoit les parcours et journaux locaux.
Relire les captures avant de considérer les essais de rendu comme vérifiés.
