# Tengai Makyou Zero — Traduction française V54

**Lot 48 complet : 400 nouveaux textes distincts, phase 1.**
233 aides/libellés et 167 intitulés d’actions de combat, sur 573 occurrences.
Les 5 961 entrées V53 sont préservées. Total : 6 534 occurrences bornées.
Les variantes partagées, noms inchangés, vides et diagnostics ne sont pas
recomptés. Six retouches du nouveau brouillon ne sont pas des ajouts.

## Installation

Appliquer **Tengai_Makyou_Zero_FR_V54.ips** directement à la ROM anglaise
originale, sans cumuler les patches. Taille : 7 340 032 octets sans en-tête.
SHA-256 source : `eb07eed483f8f79ab64309c50ad0ef19560946b8e28fbd695470552ba68e356e`.
SHA-256 ROM V54 : `5b0a5430eab8b35ff8920952a8794a6e4828f0da8c5921d804aedf0f447c6ff7`.
Le dépôt ne distribue ni ROM, ni noyau, ni état, ni dump mémoire.

## Construction

```bash
python tools/build_v54.py /chemin/original.sfc --rom-out /chemin/emulator/fr_v54.sfc
python tools/verify_storage.py /chemin/original.sfc --version V54 --built-rom /chemin/emulator/fr_v54.sfc --build-report verification/build_report.json
python tools/audit_new_sources_lot48.py
```

Python 3 et Pillow. Le constructeur génère les bases précédentes si nécessaire,
puis le JSON bilingue V54 et l’IPS autonome. Les commandes, pointeurs, alias,
modifications initiales, marqueurs SPC7110 et données hors périmètre sont
contrôlés. Aides, sauvegardes et bandeaux de combat ont des contrats natifs
séparés ; aucune règle de dialogue n’est appliquée à tous ces formats.

[Commandes de reproduction des essais](verification/reproduction/REPRODUIRE_V54.md).

## Essais et limites

7 363 lectures natives, 14 contrôles de stockage, encodage, allocation,
checksum et aller-retour IPS. 573 copies et largeurs natives : 385 aides,
3 libellés de sauvegarde et 185 bandeaux FD8B. 758 rendus ciblés au total,
avec 694 captures distinctes réellement relues sur 44 planches compactes ;
les pixels des fenêtres sont conservés exactement.

Démarrage neuf, A/reset/B et navigation : 85 + 7 captures identiques à V53.
Un parcours continu sur noyau standard, par la manette, atteint le mont Lointain,
la jonction des amis, la mine, le premier combat et ses gains/butin. L’Almanach
réel au 22/12/1995 et l’aide d’inventaire « Katana de bois » sont relus.

Les rendus d’actions sont des fixtures dans le vrai bandeau de combat : ils
ne prouvent pas le déclenchement naturel de chaque attaque. Les lieux de fin
et erreurs réelles de sauvegarde, les autres dates et sélecteurs restent à
parcourir. Menus fixes, graphismes anglais, noms d’ennemis, fins/générique,
bloc 42 et relecture globale restent notamment à traiter. Phase 1 ouverte ;
phases 2 et 3 à poursuivre.

Voir [compte rendu](COMPTE_RENDU_V54.md),
[preuves](verification/emulation_report_v54.json),
[couverture](verification/coverage_v54.json) et
[relecture](verification/relecture_v54.json).
Le compteur borné inclut menus/debug et exclut notamment le bloc 42 non borné :
il ne constitue pas un pourcentage de traduction du jeu.
