# V35 — Contrôles mémoire, naissance et horloge

32 occurrences de texte ou de bannière traduites. Les 3 160 entrées de
dialogue de V34 sont inchangées ; aucun nouveau dialogue n'est compté.
Les textes couvrent l'avertissement de sauvegarde initiale, les touches A/B,
les libellés SPC7110/SRAM/RTC, la fin du contrôle et la réinitialisation,
puis les questions, instructions et confirmations de naissance et d'horloge.
« ALL OK » devient « TOUT OK » avec la petite police technique existante.
Les sigles et opérations techniques utiles restent SPC7110, SRAM, RTC,
MUL, DIV et B+O+S. Les capitales de diagnostic n'ont pas d'accents.
Les accents de la police du jeu sont conservés dans les menus.

## Intégration

Les textes sont remplacés dans leurs espaces vérifiés, sans déplacer les
pointeurs ni modifier les instructions exécutables. « Non » utilise un
ancien octet FF de remplissage, avec le terminateur de liste suivant intact.
Le flux graphique du résultat utilise les caractères existants de la petite
police, avec son terminateur natif. Ni la taille ROM ni la police ne changent.
Le checksum est recalculé et l'aller-retour IPS est vérifié.

Les deux marqueurs internes « SPC7110 CHECK OK » restent strictement
identiques. Ils servent au protocole de sauvegarde/démarrage et ne sont pas
des libellés affichés. Le module refuse désormais de les modifier.
La ROM finale ne diffère de V34 que dans les 32 zones auditées et le checksum.

Le format numérique reste mois–jour–année, explicitement annoncé à l'écran.
L'horloge conserve son format de 12 heures AM/PM. Aucune conversion du
calendrier ou des données enregistrées n'est introduite.

## Vérification

- 3 968 lectures natives 65816, 16 contrôles de police et 14 de placement passent.
- Démarrage neuf : avertissement français, contrôle A terminé avec « TOUT OK »,
  reset puis contrôle B avec sauvegardes RTC/SRAM OK, puis accès au jeu.
  Le B prolongé à 60 000 images montre les deux sauvegardes OK ; ne pas lui
  attribuer une bannière de fin absente de cette capture.
- 43 captures de saisie relues : déplacements, changements de mois/jour/année,
  heures et minutes, Oui/Non et retour aux champs.
- Naissance : passage de 12-22-1995 à 01-21-1996, refus de cette date future,
  correction à 01-21-1994, puis validation et démarrage du jeu.
- Horloge : saisie de 01-23-1996 à 01:01 PM, refus, nouvelle confirmation,
  puis accès à la saisie de naissance.
- 38 comparaisons des chiffres rendus correspondent exactement à V34 avec
  les mêmes commandes, chacune depuis ses propres états frais.
- Huit essais de dialogues antérieurs atteignent leur terminateur exact ;
  leurs 13 captures sont relues. Menus d'articles et variantes Tenjin/Mizuki
  figurent parmi ces contrôles.

Snes9x 1.63 (1bcc369) est utilisé. Les trois écrans finaux de navigation sont
identiques à V34. Le parcours à images fixes compte 30 captures identiques
et 55 différentes : il comprend les traductions des écrans initiaux et des
écarts de phase dans les scènes/animations ultérieures. Les 20 paires
modifiées hors écrans initiaux ont été inspectées sans texte visiblement
corrompu. Cela ne prouve pas une équivalence temporelle complète.

Les branches matérielles d'échec ne sont pas provoquées ; leur libellé KO
est validé par l'audit binaire. Toutes les limites de dates, l'arrêt/reprise
avec sauvegarde hôte, Snes9x 1.60 et le matériel réel ne sont pas testés.
Le reste de la traduction reste partiel : journal 210, blocs 235/236,
244/245 et 253, entre autres ressources non traitées et messages différés.

Rapports : verification/startup_text_v35.json, startup_v35/render_report.json,
startup_numeric_comparison_v35.json et emulation_report_v35.json.

Appliquer Tengai_Makyou_Zero_FR_V35.ips à la ROM anglaise originale,
sans cumuler les patches.
