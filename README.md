# Tengai Makyou Zero — Traduction française V41

**43 textes supplémentaires : 3 483 entrées intégrées.**
Lot 35 : Sennin, Basara, karaoké et mine (96).
Les 3 440 entrées précédentes et les 32 occurrences initiales sont conservées.

Les écrans SPC7110/SRAM/RTC, naissance et horloge restent en français.
Les signatures internes restent intactes. B096-S020 et S023-S042 attendent
le traitement des colonnes et des paroles synchronisées. Les différés
antérieurs restent intacts. Consulter verification/unprocessed_inventory_v41.json
et deferred_texts_v41.json : 81 messages et quatre invites de débogage
différés dans les blocs traités.

## Installation

Appliquer **Tengai_Makyou_Zero_FR_V41.ips** directement à une copie de la ROM
anglaise originale, sans cumuler les versions.

- Taille source : 7 340 032 octets, sans en-tête de copieur.
- SHA-256 : `eb07eed483f8f79ab64309c50ad0ef19560946b8e28fbd695470552ba68e356e`.

Le dépôt ne contient ni ROM, ni sauvegarde d'état, ni noyau binaire d'émulateur.

## Construction

```bash
python tools/build_v41.py /chemin/original.sfc --rom-out /chemin/v41.sfc
python tools/verify_font.py /chemin/original.sfc
python tools/verify_storage.py /chemin/original.sfc --version V41 --built-rom /chemin/v41.sfc --build-report verification/build_report.json
```

Python 3 et Pillow. Les trente-cinq lots JSON, corrections_v20.json et
startup_text.py sont les sources. Les fichiers bilingues JSON/TSV et
lecture_v41.txt sont produits localement. Le générateur contrôle les balises,
les largeurs jusqu'à 216 pixels, les pointeurs, le checksum, l'encodage,
l'aller-retour IPS et les chaînes par les routines originales 65816.
Le banc conserve le budget de 500 000 instructions par sélection.
4 323 lectures natives, 16 contrôles de police et 14 contrôles de placement
réussissent. 135 blocs restent sur place, 34 sont relocalisés et
77 312 octets restent libres. Voir verification/build_report.json.

## Essais dans Snes9x

Noyau standard Snes9x 1.63, commit 1bcc369e89f08243e0a462882fb1f3e42e51de3a.
Démarrage neuf, parcours du début, contrôles A puis reset puis B prolongé
à 60 000 images. A affiche TERMINE / TOUT OK ; B affiche SAUV. RTC OK et
SAUV. SRAM OK. Aucun bandeau de fin B n'est annoncé.

Les 43 nouvelles entrées sont rendues avec vérification du terminateur exact.
Les captures relues figurent dans verification/scenes_v41 ; les comptes et
comparaisons sont dans verification/emulation_report_v41.json.
Les essais redirigent une demande de dialogue ; ils ne valident pas les
achats, dons, chants, échanges ou événements en progression naturelle.

Les 32 occurrences initiales sont comparées octet par octet à V40.
La saisie approfondie de naissance reste documentée dans verification/startup_v35
et startup_numeric_comparison_v35.json. V41 rejoue le démarrage et les contrôles A/B.
Snes9x 1.60, les conditions d'échec, toutes les limites de calendrier et le
matériel réel ne sont pas testés. Voir COMPTE_RENDU_V41.md et
verification/emulation_report_v41.json pour les résultats et leurs limites.

## Reproduire les essais

Avec les noyaux standard et diagnostic compilés localement et nommés
snes9x_libretro_standard.so et snes9x_libretro_diagnostic.so dans le dossier
emulator, ainsi que la ROM reconstruite fr_v41.sfc :

La comparaison demande aussi une référence V40. La reconstruire avant V41,
puis lancer run_scenario.py vers runs/fr_v40_reference41 et run_navigation.py
vers runs/v40_navigation_reference41 avec cette ROM et le noyau standard.
Reconstruire ensuite V41 pour que build_report.json corresponde à la ROM testée.

```bash
python verification/reproduction/run_version_checks.py --version v41 --tag corrected --source /chemin/original.sfc --emulator-root /chemin/emulator
python verification/reproduction/collect_evidence.py --version v41 --previous v40 --tag corrected --previous-tag reference41 --runs /chemin/emulator/runs --cases 43 --preview /chemin/contact --source /chemin/original.sfc --rom /chemin/emulator/fr_v41.sfc
```

Le script refuse les dossiers de parcours existants : choisir un nouveau tag
pour de nouveaux essais. Le collecteur laisse la relecture visuelle en attente ;
elle doit être effectuée sur les captures sélectionnées avant validation.
Le patch diagnostic est documenté dans verification/reproduction ; aucun
état ni noyau n'est distribué. Les scripts de saisie détaillée V35 et leurs
commandes restent dans ce même dossier.
