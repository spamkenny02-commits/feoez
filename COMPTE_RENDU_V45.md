# V45 — Marina, sa maison et le salon du pays du Paon

72 vrais nouveaux textes, non vides et modifiés ; **3 797 entrées intégrées**.
Lot 39 : bloc 235, sauf le choix d'achat S008 ; bloc 236 entier.
Marina, Chihiro, Riho, Sayaka et Kumiko ; visites, maison, futon et cadeaux
tricotés. Cet ensemble est cohérent sans ajout de textes pour atteindre un quota.
Les 3 725 entrées V44 restent identiques en français, mise en page et octets source.
Les commandes, pauses, alias et 32 modifications françaises initiales sont conservés.
Les signatures internes de sauvegarde restent intactes.

Les textes gardent quatre jours consécutifs, manju acheté sur place à 100 ryo,
demande de Kumiko à 1 000 ryo, futon de plumes au pays de l'Ours de Feu.
La réplique S032 conserve le « aujourd'hui et après-demain » de la source,
sans le corriger en « demain ». Les cadeaux non finis restent en cours de tricot.

## Vérifications

ROM anglaise originale épinglée, IPS autonome. Encodage, ordre des balises et
pauses, largeurs de 216 pixels, pointeurs, allocation, checksum, aller-retour IPS
vérifiés. 4719 lectures natives 65816, 16 contrôles de police et 14 de placement.
142 blocs sur place, 34 relocalisés, 77312 octets libres.
Référence V44 : empreinte publiée retrouvée, rejeu reference45.
Preuves V45 : tag corrected45, ROM `1fcb5d6ddab647de9a72550b6720af7c9a48dee2db2439de9d85a5e8c5819425`.

Snes9x 1.63 : démarrage neuf, navigation, A/reset/B prolongé. A : TERMINE /
TOUT OK ; B : SAUV. RTC et SAUV. SRAM OK. 72 terminateurs exacts,
135 captures finales relues. 85 captures fixes identiques à V44,
0 différentes ; navigation_comparison_v44_v45.json détaille les vues.
Les images partielles dues aux pauses peuvent répéter une page avant sa fin.

## Limites

B235-S008 garde ses octets et ses choix à colonnes. Tous les différés antérieurs
sont préservés : deferred_texts_v45.json et deferred_reasons_v45.json.
L'inventaire des blocs non traités reste explicite ; bloc 42 sans borne de fin validée.
Les dialogues et événements ne sont pas encore complets.

Les rendus redirigés ne prouvent ni visites naturelles sur quatre jours,
ni achat de maison, cadeaux, repos, effets d'objets ou issues des choix.
La saisie détaillée de naissance reste documentée par V35 ; le démarrage est
rejoué et les 32 modifications sont comparées à V44. Conditions d'échec,
limites de calendrier, Snes9x 1.60 et matériel réel non testés.

Appliquer Tengai_Makyou_Zero_FR_V45.ips à la ROM anglaise originale, sans cumul.
Aucune ROM, sauvegarde d'état ou noyau d'émulateur n'est publié.
