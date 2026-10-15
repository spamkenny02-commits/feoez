# Tengai Makyou Zero — Traduction française V27

102 entrées ajoutées, dont 99 textes modifiés et trois entrées vides conservées.
**2 189 entrées intégrées avec accents**. Pays de la Tortue, princesse Mitsuko,
bateau Carapace, fêtes, village du Mont-Tête et Juri.
Les 2 087 entrées de V26 sont inchangées. Variantes et répétitions sont comptées
séparément. Premier jet depuis l'anglais fourni ; noms provisoires au glossaire.

Le bloc 184/185 reçoit une traduction partagée. Les dates du 29 avril et du
10 juin, les dimanches de janvier/juillet/octobre, le stock du vendredi,
la rotation du bateau toutes les cinq minutes et le tarif de 100 ryo sont
conservés tels qu'écrits dans le jeu. Les 35 messages de débogage du bloc 183
restent inchangés. Cinq nouveaux messages à commandes particulières sont
différés : B184-S008/S010 (également accessibles par 185), B186-S015 et
B189-S001/S002. Avec les précédents, 23 messages et le bloc 132 restent en anglais.

## Installation

Appliquer **Tengai_Makyou_Zero_FR_V27.ips** directement à une copie de la ROM
anglaise originale, sans cumuler les versions.

- Taille source : 7 340 032 octets, sans en-tête de copieur.
- SHA-256 : `eb07eed483f8f79ab64309c50ad0ef19560946b8e28fbd695470552ba68e356e`.

Le dépôt ne contient ni ROM, ni sauvegarde d'état, ni noyau binaire d'émulateur.

## Construction

```bash
python tools/build_v27.py /chemin/original.sfc --rom-out /chemin/v27.sfc
python tools/verify_font.py /chemin/original.sfc
python tools/verify_storage.py /chemin/original.sfc --version V27 --built-rom /chemin/v27.sfc --build-report verification/build_report.json
```

Python 3 et Pillow. Les vingt-deux lots JSON et corrections_v20.json sont les sources.
Le générateur produit les fichiers bilingues JSON/TSV et lecture_v27.txt localement.
2 784 lectures dans les routines originales 65816 passent, avec les chaînes
inchangées et les alias. Balises, largeur maximale de 216 pixels, pointeurs,
checksum, encodage et aller-retour IPS sont contrôlés. Les 16 contrôles de police
et 14 contrôles du placement passent. 85 blocs sur place, 28 relocalisés,
83 360 octets libres ; le fichier anglais d'entrée n'est pas modifié.

## Essais dans Snes9x

Noyau standard Snes9x 1.63, commit 1bcc369e89f08243e0a462882fb1f3e42e51de3a.
Démarrage neuf et parcours du début. Contrôles A puis reset puis B prolongé
à 60 000 images : COMPLETE / ALL OK (scenario_checks_v27.json).
Les 85 captures communes avec V26 sont identiques. Menus et carte accessibles.
La version 1.60, le jeu complet et le matériel réel ne sont pas testés ici.

Vingt-trois essais ciblés contrôlent Mitsuko et l'alias de son message, la Tortue
scellée, Juri, les permissions et tarifs du bateau, sa rotation, le calendrier,
le bassin de purification, la requête de Mitsuko, la mort de Mizuki et le deuil
de Tenjin, les indications vers le Lac bleu, le stock du vendredi, le trésor du
cerisier, les frontières et la grotte du port, ainsi que le bateau bloqué.
Ils utilisent la ROM finale inchangée et un noyau de diagnostic séparé qui
redirige une seule demande de dialogue vers le bloc et le message testés.
Les routines de lookup, sélection, lecture et rendu restent celles du jeu.
Le curseur doit atteindre le terminateur exact, puis les captures sont relues.

**Ces essais valident les textes et leur pagination, pas la progression naturelle,
les combats, les paiements, les trajets du bateau, les récompenses
ou les déclenchements du calendrier et des quêtes.** Les arrière-plans appartiennent au banc de test.
Rapport et images : verification/scenes_v27.

## Reproduire les essais ciblés

Compiler le noyau standard depuis https://github.com/snes9xgit/snes9x au commit
ci-dessus. NumPy et Pillow sont nécessaires pour le frontend. Le constructeur
de diagnostic restaure le code source et le noyau standard après compilation.

```bash
python verification/reproduction/build_diagnostic_core.py --source /chemin/snes9x --out /chemin/diagnostic.so
python verification/reproduction/prepare_dialogue_state.py --core /chemin/standard.so --rom /chemin/v27.sfc --out /chemin/etat_v27
python verification/reproduction/run_targeted_dialogues.py --core /chemin/diagnostic.so --rom /chemin/v27.sfc --state /chemin/etat_v27/dialogue_entry.state --out /chemin/essais_v27 --cases verification/reproduction/cases_v27.json
```

Créer l'état avec la ROM exacte à tester. Ne pas réutiliser un état d'une autre
version. Le noyau de diagnostic ne sert pas aux essais de progression.
