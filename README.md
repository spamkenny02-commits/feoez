# Tengai Makyou Zero — Traduction française V37

**80 textes supplémentaires et quatre entrées vides conservées : 3 287 dialogues intégrés.**
Lot 31 : récit des crabes, restaurants, spectacles, transports et journal
au pays de la Tortue (bloc 210). Les 3 203 entrées précédentes et les
32 occurrences des écrans de démarrage, de naissance et d'horloge sont conservées.

Les contrôles SPC7110/SRAM/RTC, les instructions A/B/reset et les confirmations
restent en français. Les signatures internes de sauvegarde sont conservées.
La traduction reste partielle : cinq entrées du bloc 210 attendent un traitement
du formatage ; les blocs 235/236 et d'autres lacunes figurent dans
verification/unprocessed_inventory_v37.json. Dans les blocs traités,
55 messages et quatre invites de débogage restent différés.

## Installation

Appliquer **Tengai_Makyou_Zero_FR_V37.ips** directement à une copie de la ROM
anglaise originale, sans cumuler les versions.

- Taille source : 7 340 032 octets, sans en-tête de copieur.
- SHA-256 : `eb07eed483f8f79ab64309c50ad0ef19560946b8e28fbd695470552ba68e356e`.

Le dépôt ne contient ni ROM, ni sauvegarde d'état, ni noyau binaire d'émulateur.

## Construction

```bash
python tools/build_v37.py /chemin/original.sfc --rom-out /chemin/v37.sfc
python tools/verify_font.py /chemin/original.sfc
python tools/verify_storage.py /chemin/original.sfc --version V37 --built-rom /chemin/v37.sfc --build-report verification/build_report.json
```

Python 3 et Pillow. Les trente et un lots JSON, corrections_v20.json et
startup_text.py sont les sources. Les fichiers bilingues JSON/TSV et
lecture_v37.txt sont produits localement. Le générateur contrôle les balises,
les largeurs jusqu'à 216 pixels, les pointeurs, le checksum, l'encodage,
l'aller-retour IPS et les chaînes par les routines originales 65816.
Le banc conserve le budget de 500 000 instructions par sélection.
4 101 lectures natives, 16 contrôles de police et 14 contrôles de placement
passent. 128 blocs restent sur place, 34 sont relocalisés ; 77 312 octets
restent libres. Les comptes sont dans verification/build_report.json.

## Essais dans Snes9x

Noyau standard Snes9x 1.63, commit 1bcc369e89f08243e0a462882fb1f3e42e51de3a.
Démarrage neuf, parcours du début, contrôles A puis reset puis B prolongé
à 60 000 images. A affiche TERMINE / TOUT OK ; B affiche SAUV. RTC OK et
SAUV. SRAM OK. Aucun bandeau de fin B n'est annoncé.

Les 80 textes modifiés sont rendus avec vérification du terminateur exact.
Les quatre entrées vides sont préservées et contrôlées nativement. Les 134 captures
relues figurent dans verification/scenes_v37. Les 85 captures fixes du début
et les trois écrans de navigation sont identiques à V36. Les colonnes des trois menus
restent à un pixel au plus de leur position anglaise (columns_v37.json).
La commande 04 de B210-S060 garde la valeur issue de l'état de test ;
le menu naturel d'articles n'est pas validé par cette substitution.
Les essais redirigent une demande de dialogue vers une chaîne donnée ;
ils ne valident pas les achats, spectacles, récompenses, trajets, horaires
ou événements en progression naturelle.

Les 32 modifications initiales V35 sont vérifiées octet par octet contre V36.
Ses preuves approfondies de naissance restent dans verification/startup_v35
et startup_numeric_comparison_v35.json. V37 rejoue le parcours de démarrage.
Snes9x 1.60, les conditions d'échec, toutes les limites de calendrier et le
matériel réel ne sont pas testés. Voir COMPTE_RENDU_V37.md et
verification/emulation_report_v37.json pour les résultats et leurs limites.

## Reproduire les essais

Avec les noyaux standard et diagnostic compilés localement et nommés
snes9x_libretro_standard.so et snes9x_libretro_diagnostic.so dans le dossier
emulator, ainsi que la ROM reconstruite fr_v37.sfc :

La comparaison demande aussi une référence V36. La reconstruire avant V37,
puis lancer run_scenario.py vers runs/fr_v36_reference37 et run_navigation.py
vers runs/v36_navigation_reference37 avec cette ROM et le noyau standard.
Reconstruire ensuite V37 pour que build_report.json corresponde à la ROM testée.

```bash
python verification/reproduction/run_version_checks.py --version v37 --tag final --source /chemin/original.sfc --emulator-root /chemin/emulator
python verification/reproduction/collect_evidence.py --version v37 --previous v36 --tag final --previous-tag reference37 --runs /chemin/emulator/runs --cases 80 --preview /chemin/contact --source /chemin/original.sfc --rom /chemin/emulator/fr_v37.sfc
```

Le script refuse les dossiers de parcours existants : choisir un nouveau tag
pour de nouveaux essais. Le collecteur laisse la relecture visuelle en attente ;
elle doit être effectuée sur les captures sélectionnées avant validation.
Le patch diagnostic est documenté dans verification/reproduction ; aucun
état ni noyau n'est distribué. Les scripts de saisie détaillée V35 et leurs
commandes restent dans ce même dossier.
