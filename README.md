# Tengai Makyou Zero — Traduction française V21

117 entrées ajoutées, dont 116 textes modifiés et une réponse neutre conservée.
**1 559 entrées intégrées avec accents**. Affrontement avec Sara, charrettes,
ermites et techniques, portes des Enfers, Shiranui et épée d'Agni.
Les 1 442 entrées antérieures sont inchangées, y compris la correction de
pagination de la Grue introduite en V20. Les variantes et répétitions sont
comptées séparément. B153-S031 (douze points) reste identique.

Les choix Combattre/Quitter et Tuer/Pardonner gardent leur ordre et leurs colonnes
(écart d'un pixel pour Quitter, aucun pour Pardonner). Leurs effets de quête
restent à vérifier en progression normale. Deux chansons du bloc 149 restent
en anglais, avec leurs commandes 0A/CB conservées. Le glossaire note les noms
provisoires des techniques ; premier jet depuis l'anglais fourni.

## Installation

Appliquer **Tengai_Makyou_Zero_FR_V21.ips** directement à une copie de la ROM
anglaise originale, sans cumuler les versions.

- Taille source : 7 340 032 octets, sans en-tête de copieur.
- SHA-256 : `eb07eed483f8f79ab64309c50ad0ef19560946b8e28fbd695470552ba68e356e`.

Le dépôt ne contient ni ROM, ni sauvegarde d'état, ni noyau binaire d'émulateur.

## Construction

```bash
python tools/build_v21.py /chemin/original.sfc --rom-out /chemin/v21.sfc
python tools/verify_font.py /chemin/original.sfc
python tools/verify_storage.py /chemin/original.sfc --version V21 --built-rom /chemin/v21.sfc --build-report verification/build_report.json
```

Python 3 et Pillow. Les seize lots JSON et corrections_v20.json sont les sources.
Le générateur produit les fichiers bilingues JSON/TSV et lecture_v21.txt localement.
2 045 lectures dans les routines originales 65816 passent, avec les chaînes
inchangées et les alias. Balises, largeur maximale de 216 pixels, pointeurs,
checksum, encodage et aller-retour IPS sont contrôlés. Les 16 contrôles de police
et 14 contrôles du placement passent. 60 blocs sur place, 21 relocalisés,
95 312 octets libres ; le fichier anglais d'entrée n'est pas modifié.

## Essais dans Snes9x

Noyau standard Snes9x 1.63, commit 1bcc369e89f08243e0a462882fb1f3e42e51de3a.
Démarrage neuf : A, vérification, reset, B, vérification, reset. Autotests ALL OK.
Les 85 captures communes avec V20 sont identiques. Menus et carte accessibles.
La version 1.60, le jeu complet et le matériel réel ne sont pas testés ici.

Neuf essais ciblés contrôlent aussi les nouveaux dialogues à l'écran :
fontaine et alias, forme de combat de Sara, location de charrette,
Apaisement, libellés des choix de duel et de pardon, Lame du Dragon et épée d'Agni.
Ils utilisent la ROM finale inchangée et un noyau de diagnostic séparé qui
redirige une seule demande de dialogue vers le bloc et le message testés.
Les routines de lookup, sélection, lecture et rendu restent celles du jeu.
Le curseur doit atteindre le terminateur exact, puis les captures sont relues.

**Ces essais valident les textes et leur pagination, pas la progression naturelle,
les positions des PNJ, les choix de quête, les récompenses ou le recrutement.**
Les arrière-plans de ces captures sont ceux du banc de test. Rapport et images :
verification/scenes_v21. Les messages différés et le bloc 132 restent en anglais.

## Reproduire les essais ciblés

Compiler le noyau standard depuis https://github.com/snes9xgit/snes9x au commit
ci-dessus. NumPy et Pillow sont nécessaires pour le frontend. Le constructeur
de diagnostic restaure le code source et le noyau standard après compilation.

```bash
python verification/reproduction/build_diagnostic_core.py --source /chemin/snes9x --out /chemin/diagnostic.so
python verification/reproduction/prepare_dialogue_state.py --core /chemin/standard.so --rom /chemin/v21.sfc --out /chemin/etat_v21
python verification/reproduction/run_targeted_dialogues.py --core /chemin/diagnostic.so --rom /chemin/v21.sfc --state /chemin/etat_v21/dialogue_entry.state --out /chemin/essais_v21 --cases verification/reproduction/cases_v21.json
```

Créer l'état avec la ROM exacte à tester. Ne pas réutiliser un état d'une autre
version. Le noyau de diagnostic ne sert pas aux essais de progression.
