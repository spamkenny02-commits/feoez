# Lot 46 en cours — 83 / 400

Phase 1. V51 (`70b3524cea1a0dc36d6d4da67a98a20313987195`) reste la
version publiée sur main. L'identifiant `v52` sert uniquement aux essais de ce
checkpoint. Aucun lot de 400 ni nouvelle version finale n'est revendiqué.

52 notices distinctes nouvellement traduites du bloc 18 ; aucune correction
comptée comme ajout. Les 4 987 entrées antérieures gardent leur source,
traduction éditoriale et disposition en jeu. Total du checkpoint : 5 039.
Les deux lignes, y compris celles vides, et les marqueurs sont conservés.
La fin des notices non vides des blocs 17 et 18 est traitée ; cela ne prouve
pas la couverture des autres écrans du calendrier ni des dates naturelles.

Reprendre exactement ce lot au compteur inscrit dans
`verification/lot46_progress.json`. Ne pas recréer lot45, ne pas remettre le
compteur à zéro et ne pas utiliser debug/vides pour atteindre 400.
Les variables 05–07, producteurs, effets, chansons et formats spéciaux restent
à traiter avant la recherche d'oublis et la relecture générale.

La sonde `probe_substitution_slots.py` exécute les quatre routines natives
feuilles des commandes 04–07 et vérifie statiquement le lecteur. Elle prouve
les emplacements 0–3, l'espacement de 32 octets et le remappage des chiffres.
Elle ne prouve ni la longueur maximale des producteurs, ni la largeur, ni
l'affichage des valeurs des événements. Aucune réserve de 96 pixels pour
05–07 n'en est déduite.

## Reproduction privée

Utiliser les ressources privées épinglées par leurs empreintes dans les
rapports ; elles ne sont pas distribuées. Depuis la racine du dépôt :

```bash
python tools/build_lot46_checkpoint.py "$SOURCE" --rom-out "$EMU/fr_v52.sfc"
python tools/verify_lot46_checkpoint.py "$SOURCE" "$EMU/fr_v52.sfc"
python tools/probe_substitution_slots.py "$SOURCE" --out verification/substitution_slots_lot46.json
python verification/reproduction/run_version_checks.py --version v52 --tag lot46p52 --source "$SOURCE" --emulator-root "$EMU" --render-workers 4 --compact-render --auto-close-captures --diagnostic-core "$EMU/snes9x_libretro_diagnostic_v51.so" --build-report verification/build_report_lot46_checkpoint.json
```

Choisir un nouveau tag si les dossiers d'essai existent déjà. Le constructeur
produit un IPS autonome de checkpoint ; cet IPS n'est pas une version finale.
Les états, ROM, noyaux et dumps restent privés.

Les validations réellement terminées et leurs limites sont consignées dans
`verification/lot46_progress.json` et les rapports associés.

## Résultats du checkpoint

52 rendus ciblés et 52 captures de texte relues ; démarrage, A/reset/B,
navigation, 14 contrôles de stockage et 16 de police passés. Les 85 captures
de démarrage et les trois vues de navigation sont identiques à V51.
319 lectures natives de textes différés sont inchangées.

L’Almanach réel au 22/12/1995 affiche correctement B018-S182 en français.
Cette preuve ne couvre aucune autre date. « Winter Solstice » et des libellés
anglais y restent visibles : voir `verification/calendar_lot46_checkpoint/`.
Les 52 notices sont relues ; la relecture globale reste à faire.

## Reprise à 83 / 400

31 textes numériques ajoutés (montants, durées et scores). Total : 5 070
entrées, dont les 5 039 du checkpoint précédent inchangées. Aucun texte partagé,
profil de test ou correction n'est compté comme traduction supplémentaire.

Les commandes 05–07 sont admises uniquement par une liste de 31 contrats
numériques explicites : huit chiffres, réserve native de 56 pixels. Le lecteur
et la conversion d'origine sont conservés. 2 140 exécutions d'une sonde restreinte
couvrent les quatre emplacements et des valeurs limites ; la multiplication
matérielle y est modélisée sans prétention de timing. Les producteurs réels des
événements ne sont pas encore liés à chaque texte : aucune généralisation aux
noms, objets, dates/ordinaux, choix ou effets.

124 rendus natifs sur noyau diagnostique distinct : zéro, un, 16 777 215 et
10 000 000. Les valeurs injectées sont aussi vérifiées à leur consommation.
196 captures sont couvertes par 155 PNG distincts tous relus. Le profil un
révèle des accords au singulier à corriger avant une publication validée : voir
`verification/relecture_lot46_points.json`. Il s'agit d'un checkpoint de travail,
pas d'un lot de 400 validé ni d'une publication finale sur main.

Les 52 notices et la notice réelle du 22/12/1995 ont été rendues et relues à
nouveau sur cette ROM. Démarrage, A/reset/B et navigation passent ; 85 captures
et trois vues sont identiques à V51. Main reste V51.

Pour reproduire les profils, construire un noyau privé avec
`build_diagnostic_core.py --enable-slot-fixtures`, puis exécuter
`run_targeted_dialogues.py` avec `--cases cases_lot46_numeric.json` et
`--slot-fixtures slot_fixtures_lot46_numeric.json` (fichiers dans
`verification/reproduction/`). Utiliser un état frais de la même ROM et un
nouveau dossier de sortie. Sans le drapeau de construction et ces options,
les parcours habituels ne reçoivent aucune valeur synthétique.
