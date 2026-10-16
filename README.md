# Tengai Makyou Zero — Traduction française V29

198 entrées ajoutées : 194 textes modifiés, trois entrées vides et une réponse
neutre conservées. **2 563 entrées intégrées avec accents**.
Énigmes de Juri, roi de la Forêt, Tortue divine, Mitsuko et son coffret,
auberges et liaisons maritimes. Les 2 365 entrées de V28 sont inchangées.
Variantes et répétitions sont comptées séparément. Premier jet à relire depuis
l'anglais fourni ; noms provisoires au glossaire.

Les accès 206/207 aux énigmes partagent une traduction unique. Les portes
T/F gardent leurs lettres, avec une explication française. DOG et GOD restent
en anglais pour conserver l'inversion des lettres ; leurs sens, chien et dieu,
sont expliqués. La formulation « un et un ensemble » conserve l'ambiguïté
entre 2 et 11. Le récit de la course conserve sa question sur le début.
Les prix et durées restent ceux du script, notamment les 100 ryo du bateau,
les nuits à 1 et 60 ryo et les centaines d'années de Tenjin et Mizuki.
Parmi les blocs traités, 40 messages sont différés. Le bloc 210 (journal) n'est
pas traité dans ce lot ; le bloc 132 et le débogage 183 restent inchangés.

Après relecture, cinq répliques ont été raccourcies pour éviter des fins de
page isolées : B206-S001, B208-S013, B209-S025, B211-S005/S010.
Les preuves finales proviennent de la ROM reconstruite après ces corrections.

## Installation

Appliquer **Tengai_Makyou_Zero_FR_V29.ips** directement à une copie de la ROM
anglaise originale, sans cumuler les versions.

- Taille source : 7 340 032 octets, sans en-tête de copieur.
- SHA-256 : `eb07eed483f8f79ab64309c50ad0ef19560946b8e28fbd695470552ba68e356e`.

Le dépôt ne contient ni ROM, ni sauvegarde d'état, ni noyau binaire d'émulateur.

## Construction

```bash
python tools/build_v29.py /chemin/original.sfc --rom-out /chemin/v29.sfc
python tools/verify_font.py /chemin/original.sfc
python tools/verify_storage.py /chemin/original.sfc --version V29 --built-rom /chemin/v29.sfc --build-report verification/build_report.json
```

Python 3 et Pillow. Les vingt-quatre lots JSON et corrections_v20.json sont les sources.
Le générateur produit les fichiers bilingues JSON/TSV et lecture_v29.txt localement.
3 316 lectures dans les routines originales 65816 passent, avec les chaînes
inchangées et les alias. Balises, largeur maximale de 216 pixels, pointeurs,
checksum, encodage et aller-retour IPS sont contrôlés. Les 16 contrôles de police
et 14 contrôles du placement passent. 98 blocs sur place, 30 relocalisés,
81 152 octets libres ; le fichier anglais d'entrée n'est pas modifié.

## Essais dans Snes9x

Noyau standard Snes9x 1.63, commit 1bcc369e89f08243e0a462882fb1f3e42e51de3a.
Démarrage neuf et parcours du début. Contrôles A puis reset puis B prolongé
à 60 000 images : COMPLETE / ALL OK (scenario_checks_v29.json).
Les 85 captures communes avec V28 sont identiques. Menus et carte accessibles.
La version 1.60, le jeu complet et le matériel réel ne sont pas testés ici.

Trente-six essais ciblés contrôlent les énigmes et leur alias, DOG/GOD,
les réponses contradictoires de Juri, la course des fruits, la Tortue divine,
les six pierres, le miroir de l'Arche, le coffret de Mitsuko, les récits d'Agni,
les tarifs des auberges, les directions et les correspondances maritimes.
Ils utilisent la ROM finale inchangée et un noyau de diagnostic séparé qui
redirige une seule demande de dialogue vers le bloc et le message testés.
Les routines de lookup, sélection, lecture et rendu restent celles du jeu.
Le curseur doit atteindre le terminateur exact, puis les captures sont relues.

**Ces essais valident les textes et leur pagination, pas la progression naturelle,
les réponses effectivement choisies aux portes, les combats, les paiements,
les soins, les trajets du bateau, les récompenses ou la maturation du coffret.** Les arrière-plans appartiennent au banc de test.
Rapport et images : verification/scenes_v29.

## Reproduire les essais ciblés

Compiler le noyau standard depuis https://github.com/snes9xgit/snes9x au commit
ci-dessus. NumPy et Pillow sont nécessaires pour le frontend. Le constructeur
de diagnostic restaure le code source et le noyau standard après compilation.

```bash
python verification/reproduction/build_diagnostic_core.py --source /chemin/snes9x --out /chemin/diagnostic.so
python verification/reproduction/prepare_dialogue_state.py --core /chemin/standard.so --rom /chemin/v29.sfc --out /chemin/etat_v29
python verification/reproduction/run_targeted_dialogues.py --core /chemin/diagnostic.so --rom /chemin/v29.sfc --state /chemin/etat_v29/dialogue_entry.state --out /chemin/essais_v29 --cases verification/reproduction/cases_v29.json
```

Créer l'état avec la ROM exacte à tester. Ne pas réutiliser un état d'une autre
version. Le noyau de diagnostic ne sert pas aux essais de progression.
