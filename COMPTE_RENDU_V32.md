# V32 — Double-Chance, Akamaru et marché en plein air

134 entrées ajoutées : 133 textes modifiés et une entrée vide conservée.
Total : 2 885. Les 2 751 entrées de V31 gardent leur texte et leur disposition.
Les accès 226/227 partagent les textes du cache-cache.

Le lot traduit la vie à Double-Chance, la tromperie d'Akamaru, l'arrivée
de Subaru, l'envol du Mahamayuri et les boutiques du marché en plein air.
Les deux variantes du thé rouge gardent leurs effets déclarés : poison
pour l'eau de pluie, restauration de santé/technique pour le gingembre mariné.
Les horaires des boutiques, les auberges à 100/50 ryo, les trente pour cent
de commission, les directions et les six cents ans du Mahamayuri sont conservés.

## Validation

3 675 lectures natives, 16 contrôles de police et 14 de placement réussis.
114 blocs sur place, 31 relocalisés ; 80848 octets libres.
A : COMPLETE / ALL OK ; B : les deux BACKUP OK.

Voir verification/build_report.json, verification/emulation_report_v32.json
et verification/scenes_v32/render_report.json. Cinquante-quatre cas de rendu
couvrent les principales variantes, les longs récits et les panneaux.
Le lanceur commun run_version_checks.py produit des parcours neufs avec
la ROM exacte et refuse de réutiliser un dossier de preuves existant.

Les essais de rendu redirigent un dialogue : ils ne valident pas la
progression naturelle, les choix, les combats, le recrutement effectif,
les effets du thé, les paiements, achats, horaires réels ou le vol.
47 messages sont différés, dont les six nouveaux B225-S012, B229-S012 et
B231-S010/S013/S029/S032. Le journal 210 reste à traiter ; les blocs
132 et 183 restent inchangés.

Appliquer Tengai_Makyou_Zero_FR_V32.ips directement à la ROM anglaise
originale, sans cumuler les patches.
