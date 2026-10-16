# V34 — Gardiens, Akamaru, Ninigi et couronnement

123 textes ajoutés dans les blocs 241, 242, 243, 246, 247, 249 et 252.
Total : 3 160 entrées. Les 3 037 entrées de V33 sont conservées.
Le lot couvre les statues des gardiens, les scènes d'Akamaru et Doki,
les menaces de Ninigi, ses échanges avec Atramentous Alabaster et Shiranui,
puis les retrouvailles et les discours du couronnement.
Les variantes Tenjin/Mizuki, les répétitions et les pauses sont conservées.
Les alias 248 et 250/251 utilisent leurs blocs communs traduits.

Les blocs 235/236 restent intacts : leurs nombreux effets de voix attendent
une prise en charge dédiée. Les menus 244/245 et le bloc 253 restent également
à traiter. B252-S018/S019 sont différés pour le même effet de voix ; les
invites de débogage B252-S098 à S101 restent en anglais. Les autres textes
auparavant différés sont inchangés, comme les blocs 132, 183 et le journal 210.

## Validation

Les répliques B247-S005, B252-S008 et B252-S025 ont été resserrées
avant les essais. Après relecture à l’écran, B242-S003, B246-S004 et
B252-S002/S010/S014/S021/S037/S094 ont été ajustées pour regrouper leurs
fins de phrase. Les preuves finales utilisent les parcours corrected,
créés avec la ROM reconstruite après ces corrections.

Les résultats définitifs, empreintes et limites figurent dans
verification/build_report.json et verification/emulation_report_v34.json.
Les 126 cas de rendu couvrent les 123 entrées nouvelles et trois alias.
Chaque cas doit atteindre son terminateur exact ; toutes les pages retenues
font l'objet d'une inspection visuelle.

Ces essais redirigent une demande de dialogue depuis un état créé avec la
ROM exacte. Ils ne valident pas les combats, le vol en Mahamayuri, les choix,
la progression naturelle jusqu'au dénouement ni le couronnement jouable.
L'arrière-plan vient du banc de test. Le noyau standard sert au démarrage,
aux contrôles A/B et à la navigation ; le noyau de diagnostic sert au rendu.
Snes9x 1.60 et le matériel réel ne sont pas testés.

Appliquer Tengai_Makyou_Zero_FR_V34.ips directement à la ROM anglaise
originale, sans cumuler les patches.

3968 lectures natives, 16 contrôles de police et 14 de placement réussis.
125 blocs sur place, 33 relocalisés ; 80656 octets libres.
A : COMPLETE / ALL OK ; B : RTC BACKUP et S-RAM BACKUP OK.
Comparaison V33/V34 : 85 captures fixes identiques, 0 différentes.
