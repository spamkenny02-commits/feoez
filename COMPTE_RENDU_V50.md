# V50 — Services communs, lettres et élevage

**300 nouveaux textes ; 4 687 entrées intégrées.**
Lot 44 : voyance et change, lettres de Momoko, coffres et fêtes,
Maison du Choix des Princesses, Pavillon des Geishas, élevage,
quelques fragments du karaoké et textes différés des régions précédentes.
Les noms d'espèces ont huit occurrences traduites ; aucun texte vide,
diagnostic ou texte anglais inchangé ne complète le compteur.

Les prédictions restent les propos du voyant. Les lettres conservent leur
progression affective, leurs menaces et leur fin sombre, sans ajout.
L'article sur Chitose reste une rumeur du journal. Dates, prix et quantités
restent ceux de la source. Élevage : 45–60 minutes, cible de 50 minutes,
limite de sept créatures, un point de santé perdu par heure même console éteinte,
quatre repas, chrysalide 40–50 heures et oeuf perdu après plus de 60 heures.
Les textes précisant plus de 500 heures et les 255 points de Manto sont conservés.

Les colonnes des choix sont mesurées avec la police native et placées
à un pixel près de leurs positions anglaises. Leur première ligne et le nombre
de lignes précédant les choix sont identiques à la source ; la relecture a
permis de corriger une pagination décalée. Les commandes, coeurs,
pauses et substitutions 04 restent dans l'ordre source ; 96 pixels sont
réservés aux substitutions. Les autres variables et formats restent partiels.

## Vérifications

ROM anglaise originale épinglée ; référence V49 conforme à son empreinte publiée.
5 644 lectures natives, 16 contrôles de police et 14 de placement réussis.
Encodage, balises, pauses, largeur de 216 pixels, pointeurs, allocation,
checksum et aller-retour IPS vérifiés. 154 blocs sur place,
34 relocalisés ; 71600 octets libres.
Snes9x 1.63, tag corrected50 : démarrage neuf, navigation, A/reset/B prolongé.
300 terminateurs exacts, 582 captures de dialogue et cinq captures système relues.
85 captures fixes et trois vues de navigation identiques à V49.
Les 4 387 anciennes entrées gardent français, mise en page et octets source.
32 modifications initiales et marqueurs SPC7110 intacts ; 288 lectures de différés.
A et B : TERMINE / TOUT OK ; B confirme SAUV. RTC et SAUV. SRAM OK.
Les pauses peuvent produire des captures partielles ou répétées ; certaines
fins de page contiennent peu de mots. La lecture complète est vérifiée séparément.
ROM : `e94f7f4dab0ac39e01de7c640d676f674a0d8a81e8e2ed5bc6d3f926950c9603`.
IPS : `d7a19c970367384f2d7b36ac2a020efe7feceb17efe60a43fdce152c5b0992bd`.
Voir emulation_report_v50.json et scenes_v50/render_report.json.

Les captures intermédiaires sont nettoyées après chaque cas réussi ;
les images sélectionnées restent identiques au mode non compacté
(voir compact_render_check_v50.json).

## Limites

Les rendus ciblés contrôlent le texte, sa pagination et son terminateur ;
ils ne valident pas le déroulement naturel des services, les branches des choix,
les variables remplies par leurs événements réels, le calendrier, le change,
les lettres envoyées, l'élevage hors tension ou la synchronisation musicale.
Le contexte stagé remplit parfois 04 avec Higan : ces captures contrôlent
le placement, pas le vrai taux de change ou le minuteur PLGS.
Cinq fragments du karaoké sont traduits ; les autres gardent leurs octets.
Les substitutions 05–07 et les commandes particulières non traitées restent
différées. Les états d'animaux et les menus restent partiels.
Le bloc 183 de debug est intact ; le bloc 42 hors zone bornée est exclu.
Noms d'espèces et objets nouveaux : provisoires, à harmoniser avec les menus.
Naissance détaillée : preuves V35. Snes9x 1.60 et matériel réel non testés.
Les dialogues et événements ne sont pas complets.

Appliquer Tengai_Makyou_Zero_FR_V50.ips à la ROM anglaise originale, sans cumul.
Aucune ROM, sauvegarde d'état ou noyau d'émulateur n'est publié.
