# Tengai Makyou Zero — Traduction française V28

176 entrées ajoutées, dont 161 textes modifiés, douze entrées vides et trois
réponses neutres conservées. **2 365 entrées intégrées avec accents**.
Village du Lac bleu, labyrinthe et château de Juri, épreuves des tours et
88 coffres, Mizuki, Sara et flûte Mandala. Les 2 189 entrées de V27 sont
inchangées. Variantes et répétitions sont comptées séparément. Premier jet
à relire depuis l'anglais fourni ; noms provisoires au glossaire.

Les quatre accès 197/198/199/200 au jardin partagent une traduction, ainsi
que les deux accès 203/204 aux coffres. Les indications droite/gauche, est,
ouest et sud-est sont conservées, comme les attaques à droite et les parchemins
à gauche. Les exemples de vocabulaire de Juri sont adaptés en français ;
l'indice « à l'EST d'Éden » garde sa direction. Le château parle du « niveau 1 »
pour éviter une ambiguïté entre étage et rez-de-chaussée.
39 messages à commandes particulières ou fragments non résolus restent en
anglais, ainsi que le bloc 132 et les 35 invites de débogage du bloc 183.

## Installation

Appliquer **Tengai_Makyou_Zero_FR_V28.ips** directement à une copie de la ROM
anglaise originale, sans cumuler les versions.

- Taille source : 7 340 032 octets, sans en-tête de copieur.
- SHA-256 : `eb07eed483f8f79ab64309c50ad0ef19560946b8e28fbd695470552ba68e356e`.

Le dépôt ne contient ni ROM, ni sauvegarde d'état, ni noyau binaire d'émulateur.

## Construction

```bash
python tools/build_v28.py /chemin/original.sfc --rom-out /chemin/v28.sfc
python tools/verify_font.py /chemin/original.sfc
python tools/verify_storage.py /chemin/original.sfc --version V28 --built-rom /chemin/v28.sfc --build-report verification/build_report.json
```

Python 3 et Pillow. Les vingt-trois lots JSON et corrections_v20.json sont les sources.
Le générateur produit les fichiers bilingues JSON/TSV et lecture_v28.txt localement.
3 071 lectures dans les routines originales 65816 passent, avec les chaînes
inchangées et les alias. Balises, largeur maximale de 216 pixels, pointeurs,
checksum, encodage et aller-retour IPS sont contrôlés. Les 16 contrôles de police
et 14 contrôles du placement passent. 92 blocs sur place, 30 relocalisés,
81 152 octets libres ; le fichier anglais d'entrée n'est pas modifié.

## Essais dans Snes9x

Noyau standard Snes9x 1.63, commit 1bcc369e89f08243e0a462882fb1f3e42e51de3a.
Démarrage neuf et parcours du début. Contrôles A puis reset puis B prolongé
à 60 000 images : COMPLETE / ALL OK (scenario_checks_v28.json).
Les 85 captures communes avec V27 sont identiques. Menus et carte accessibles.
La version 1.60, le jeu complet et le matériel réel ne sont pas testés ici.

Trente essais ciblés contrôlent le bateau, le sanctuaire, le trajet gratuit,
les directions du jardin et ses quatre alias, les explications de Juri,
les règles des tours, Scission, les 88 coffres, les commandes et balises,
la clé et son alias, les révélations sur Mizuki et Sara, l'union du clan du Feu,
l'identité de Mizuki et le fonctionnement de la flûte Mandala.
Ils utilisent la ROM finale inchangée et un noyau de diagnostic séparé qui
redirige une seule demande de dialogue vers le bloc et le message testés.
Les routines de lookup, sélection, lecture et rendu restent celles du jeu.
Le test B203-S012 ne prépare pas la valeur numérique du compteur : il utilise
la valeur héritée du dialogue de départ (Higan), sans valider le numéro du coffre.
Le curseur doit atteindre le terminateur exact, puis les captures sont relues.

**Ces essais valident les textes et leur pagination, pas la progression naturelle,
les combats, les paiements, les trajets du bateau, les panneaux du labyrinthe,
les restrictions des tours, les récompenses, les coffres ou les changements
de personnage par la flûte.** Les arrière-plans appartiennent au banc de test.
Rapport et images : verification/scenes_v28.

## Reproduire les essais ciblés

Compiler le noyau standard depuis https://github.com/snes9xgit/snes9x au commit
ci-dessus. NumPy et Pillow sont nécessaires pour le frontend. Le constructeur
de diagnostic restaure le code source et le noyau standard après compilation.

```bash
python verification/reproduction/build_diagnostic_core.py --source /chemin/snes9x --out /chemin/diagnostic.so
python verification/reproduction/prepare_dialogue_state.py --core /chemin/standard.so --rom /chemin/v28.sfc --out /chemin/etat_v28
python verification/reproduction/run_targeted_dialogues.py --core /chemin/diagnostic.so --rom /chemin/v28.sfc --state /chemin/etat_v28/dialogue_entry.state --out /chemin/essais_v28 --cases verification/reproduction/cases_v28.json
```

Créer l'état avec la ROM exacte à tester. Ne pas réutiliser un état d'une autre
version. Le noyau de diagnostic ne sert pas aux essais de progression.
