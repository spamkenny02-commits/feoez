# Tengai Makyou Zero — Traduction française V38

**88 textes supplémentaires et un grognement conservé : 3 376 entrées intégrées.**
Lot 32 : village du Mont de Glace gelé puis libéré (67/68), ermites du Vent,
de la Vue et du Jet (73), statues de Kingin (80). Les 3 287 entrées précédentes
et les 32 occurrences initiales sont conservées.

Les écrans SPC7110/SRAM/RTC, naissance et horloge restent en français.
Les signatures internes de sauvegarde restent intactes. La traduction est
partielle : B080-S021 attend la commande d'effet 0A ; le formatage différé,
les blocs 235/236 et d'autres lacunes restent à traiter. Consulter
verification/unprocessed_inventory_v38.json et deferred_texts_v38.json.
56 messages et quatre invites de débogage restent différés dans les blocs traités.

## Installation

Appliquer **Tengai_Makyou_Zero_FR_V38.ips** directement à une copie de la ROM
anglaise originale, sans cumuler les versions.

- Taille source : 7 340 032 octets, sans en-tête de copieur.
- SHA-256 : `eb07eed483f8f79ab64309c50ad0ef19560946b8e28fbd695470552ba68e356e`.

Le dépôt ne contient ni ROM, ni sauvegarde d'état, ni noyau binaire d'émulateur.

## Construction

```bash
python tools/build_v38.py /chemin/original.sfc --rom-out /chemin/v38.sfc
python tools/verify_font.py /chemin/original.sfc
python tools/verify_storage.py /chemin/original.sfc --version V38 --built-rom /chemin/v38.sfc --build-report verification/build_report.json
```

Python 3 et Pillow. Les trente-deux lots JSON, corrections_v20.json et
startup_text.py sont les sources. Les fichiers bilingues JSON/TSV et
lecture_v38.txt sont produits localement. Le générateur contrôle les balises,
les largeurs jusqu'à 216 pixels, les pointeurs, le checksum, l'encodage,
l'aller-retour IPS et les chaînes par les routines originales 65816.
Le banc conserve le budget de 500 000 instructions par sélection.
4 191 lectures natives, 16 contrôles de police et 14 contrôles de placement
passent. 132 blocs restent sur place, 34 sont relocalisés ; 77 312 octets
restent libres. Les comptes sont dans verification/build_report.json.

## Essais dans Snes9x

Noyau standard Snes9x 1.63, commit 1bcc369e89f08243e0a462882fb1f3e42e51de3a.
Démarrage neuf, parcours du début, contrôles A puis reset puis B prolongé
à 60 000 images. A affiche TERMINE / TOUT OK ; B affiche SAUV. RTC OK et
SAUV. SRAM OK. Aucun bandeau de fin B n'est annoncé.

Les 89 nouvelles entrées sont rendues, y compris le grognement conservé,
avec vérification du terminateur exact. Les 151 captures relues figurent dans
verification/scenes_v38. Les 85 captures fixes communes du début et les
trois écrans de navigation sont identiques à V37. Le menu B073-S004 conserve ses deux colonnes
à un pixel au plus de leur position anglaise (columns_v38.json).
Le cœur de B067-S015 conserve sa séquence de commande, sans modifier l'effet.
Les essais redirigent une demande de dialogue ; ils ne valident pas les
événements, achats, soins, fusions, combats ou récompenses en progression naturelle.

Les 32 occurrences initiales sont comparées octet par octet à V37.
La saisie approfondie de naissance reste documentée dans verification/startup_v35
et startup_numeric_comparison_v35.json. V38 rejoue le démarrage et les contrôles A/B.
Snes9x 1.60, les conditions d'échec, toutes les limites de calendrier et le
matériel réel ne sont pas testés. Voir COMPTE_RENDU_V38.md et
verification/emulation_report_v38.json pour les résultats et leurs limites.

## Reproduire les essais

Avec les noyaux standard et diagnostic compilés localement et nommés
snes9x_libretro_standard.so et snes9x_libretro_diagnostic.so dans le dossier
emulator, ainsi que la ROM reconstruite fr_v38.sfc :

La comparaison demande aussi une référence V37. La reconstruire avant V38,
puis lancer run_scenario.py vers runs/fr_v37_reference38 et run_navigation.py
vers runs/v37_navigation_reference38 avec cette ROM et le noyau standard.
Reconstruire ensuite V38 pour que build_report.json corresponde à la ROM testée.

```bash
python verification/reproduction/run_version_checks.py --version v38 --tag final --source /chemin/original.sfc --emulator-root /chemin/emulator
python verification/reproduction/collect_evidence.py --version v38 --previous v37 --tag final --previous-tag reference38 --runs /chemin/emulator/runs --cases 89 --preview /chemin/contact --source /chemin/original.sfc --rom /chemin/emulator/fr_v38.sfc
```

Le script refuse les dossiers de parcours existants : choisir un nouveau tag
pour de nouveaux essais. Le collecteur laisse la relecture visuelle en attente ;
elle doit être effectuée sur les captures sélectionnées avant validation.
Le patch diagnostic est documenté dans verification/reproduction ; aucun
état ni noyau n'est distribué. Les scripts de saisie détaillée V35 et leurs
commandes restent dans ce même dossier.
