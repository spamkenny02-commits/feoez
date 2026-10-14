# Tengai Makyou Zero — Traduction française V23

137 entrées ajoutées, dont 135 textes modifiés et deux réponses neutres conservées.
**1 719 entrées intégrées avec accents**. Héritage de Shiranui, révélations du
Dragon, six pierres, Arche des Cieux, villages et boutiques du royaume du Dragon.
Les 1 582 entrées de V22 sont inchangées. Variantes et répétitions sont comptées
séparément. B159-S036/S053 gardent leurs trois points et leurs pauses d'origine.

Premier jet depuis l'anglais fourni ; noms provisoires dans le glossaire.
Les variantes Tenjin/Mizuki, les cent jours de guerre, les six cents ans,
les directions, la remise de cinquante pour cent et les 200 ryo sont conservés.
18 messages différés et le bloc 132 restent inchangés en anglais.

## Installation

Appliquer **Tengai_Makyou_Zero_FR_V23.ips** directement à une copie de la ROM
anglaise originale, sans cumuler les versions.

- Taille source : 7 340 032 octets, sans en-tête de copieur.
- SHA-256 : `eb07eed483f8f79ab64309c50ad0ef19560946b8e28fbd695470552ba68e356e`.

Le dépôt ne contient ni ROM, ni sauvegarde d'état, ni noyau binaire d'émulateur.

## Construction

```bash
python tools/build_v23.py /chemin/original.sfc --rom-out /chemin/v23.sfc
python tools/verify_font.py /chemin/original.sfc
python tools/verify_storage.py /chemin/original.sfc --version V23 --built-rom /chemin/v23.sfc --build-report verification/build_report.json
```

Python 3 et Pillow. Les dix-huit lots JSON et corrections_v20.json sont les sources.
Le générateur produit les fichiers bilingues JSON/TSV et lecture_v23.txt localement.
2 217 lectures dans les routines originales 65816 passent, avec les chaînes
inchangées et les alias. Balises, largeur maximale de 216 pixels, pointeurs,
checksum, encodage et aller-retour IPS sont contrôlés. Les 16 contrôles de police
et 14 contrôles du placement passent. 63 blocs sur place, 25 relocalisés,
87 968 octets libres ; le fichier anglais d'entrée n'est pas modifié.

## Essais dans Snes9x

Noyau standard Snes9x 1.63, commit 1bcc369e89f08243e0a462882fb1f3e42e51de3a.
Démarrage neuf et parcours du début. Contrôles A puis reset puis B prolongé
à 60 000 images : COMPLETE / ALL OK (scenario_checks_v23.json).
Sur 85 captures communes avec V22, 82 sont identiques ; 3 présentent
seulement une minute différente sur l'horloge. Menus et carte accessibles.
La version 1.60, le jeu complet et le matériel réel ne sont pas testés ici.

Quatorze essais ciblés contrôlent les nouveaux dialogues à l'écran : héritage
et épée des ténèbres, guerre d'Agni, Arche scellée, Dragon gardien, six pierres,
Mizuki, miroir de l'Arche, barrière de Ninigi, routes vers le château,
remise de 50 %, auberge à 200 ryo et possession du prince.
Ils utilisent la ROM finale inchangée et un noyau de diagnostic séparé qui
redirige une seule demande de dialogue vers le bloc et le message testés.
Les routines de lookup, sélection, lecture et rendu restent celles du jeu.
Le curseur doit atteindre le terminateur exact, puis les captures sont relues.
Les commandes 0E des récits de guerre et de l'Arche sont également conservées.

**Ces essais valident les textes et leur pagination, pas la progression naturelle,
l'héritage d'objets, l'ouverture de la barrière, le voyage de l'Arche, les achats
ou l'application de la remise.** Les arrière-plans appartiennent au banc de test.
Rapport et images : verification/scenes_v23.

## Reproduire les essais ciblés

Compiler le noyau standard depuis https://github.com/snes9xgit/snes9x au commit
ci-dessus. NumPy et Pillow sont nécessaires pour le frontend. Le constructeur
de diagnostic restaure le code source et le noyau standard après compilation.

```bash
python verification/reproduction/build_diagnostic_core.py --source /chemin/snes9x --out /chemin/diagnostic.so
python verification/reproduction/prepare_dialogue_state.py --core /chemin/standard.so --rom /chemin/v23.sfc --out /chemin/etat_v23
python verification/reproduction/run_targeted_dialogues.py --core /chemin/diagnostic.so --rom /chemin/v23.sfc --state /chemin/etat_v23/dialogue_entry.state --out /chemin/essais_v23 --cases verification/reproduction/cases_v23.json
```

Créer l'état avec la ROM exacte à tester. Ne pas réutiliser un état d'une autre
version. Le noyau de diagnostic ne sert pas aux essais de progression.
