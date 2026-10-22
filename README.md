# Tengai Makyou Zero — Traduction française V53

**Lot 47 complet : 400 nouveaux textes distincts, phase 1.**
388 sources bornées et 12 mois natifs ; 580 occurrences intégrées, sans
recompter les variantes partagées. Les 5 381 entrées V52 sont préservées.
Total : 5 961 occurrences bornées. La phase 1 continue ; recherche exhaustive
et relecture globale restent à effectuer.

## Installation

Appliquer **Tengai_Makyou_Zero_FR_V53.ips** directement à la ROM anglaise
originale, sans cumuler les patches. Taille : 7 340 032 octets sans en-tête.
SHA-256 source : `eb07eed483f8f79ab64309c50ad0ef19560946b8e28fbd695470552ba68e356e`.
Le dépôt ne distribue ni ROM, ni noyau, ni état, ni dump mémoire.

## Construction

```bash
python tools/build_v53.py /chemin/original.sfc --rom-out /chemin/emulator/fr_v53.sfc
python tools/verify_storage.py /chemin/original.sfc --version V53 --built-rom /chemin/emulator/fr_v53.sfc --build-report verification/build_report.json
python tools/verify_battle_result_lot47.py /chemin/emulator/fr_v53.sfc --out verification/battle_result_lot47_checks.json
```

Python 3 et Pillow. Le constructeur utilise les sources des lots précédents,
génère la base V52 si nécessaire, puis produit le JSON bilingue V53 et l’IPS.
Il préserve les traductions précédentes, commandes, pointeurs, alias, modifications
initiales, marqueurs SPC7110 et données hors périmètre. Les contrats de noms,
nombres, styles et lecteurs de résultat sont distincts.

[Commandes de reproduction des essais](verification/reproduction/REPRODUIRE_V53.md).

## Essais et limites

6 756 lectures natives ; 14 contrôles de stockage ; reproduction exacte du
patch autonome. Démarrage neuf, A/reset/B, navigation et 722 rendus ciblés
sur la ROM finale. Les 619 captures de texte distinctes ont été réellement
relues. Carte réelle : « Pays de l’Ours de Feu », boussole « O + E ».
Almanach réel ouvert au 22/12/1995 ; cela ne valide pas les autres dates.

Les fixtures sont synthétiques : elles ne prouvent ni les parcours naturels,
ni les vrais choix, valeurs, récompenses, échéances ou effets musicaux.
Les graphismes anglais et les menus généraux restent notamment à traiter.
Les comparaisons de régression comportent des écarts d’animation et de PNJ
relus ; elles ne sont pas toutes identiques au pixel près.

Voir [compte rendu](COMPTE_RENDU_V53.md),
[preuves](verification/emulation_report_v53.json),
[couverture](verification/coverage_v53.json) et
[relecture](verification/relecture_v53.json).
Le compteur borné, qui inclut menus et debug et exclut notamment le bloc 42
non borné, ne constitue pas un pourcentage de traduction du jeu.

Les619 captures de texte relues sont regroupées en40 planches compactes,
avec empreintes et coordonnées par cas dans scenes_v53/render_report.json.
Les pixels des fenêtres de texte sont conservés exactement, à échelle2.
