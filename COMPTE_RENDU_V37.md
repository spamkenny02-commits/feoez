# V37 — Crabes et nouvelles du pays de la Tortue

84 entrées du bloc 210 ajoutées : 80 textes modifiés et quatre entrées
vides/espacées conservées (12/59/62/64). Total : 3 287 dialogues.
Les 3 203 entrées précédentes et les 32 occurrences initiales sont conservées.
Le lot31_fr.json complète le récit de Manto du lot précédent.

Le récit explique les graines de kaki, les huîtres portant le même nom,
les fruits cultivés, l'expulsion des crabes et le casque familial.
La soupe à 10 000 ryo, les spectacles à 5 000 ryo, la nuit à 120 ryo et
les trajets à 100 ryo conservent leurs prix. La destination change toutes
les cinq minutes. Le journal coûte dix ryo ; sa récompense pour la capture
d'un homme-arbre vivant est d'un million de ryo.

Le Bavard de la Tortue rapporte les rumeurs et accusations du texte anglais ;
les affirmations sur Mitsuko et Higan restent celles de ce journal fictif.
Cinq quasi-collisions et trois manœuvres de recul sont conservées, sans
inventer trois navires distincts. Les bas prix sont annoncés de vingt à
trente minutes après l'heure, la hausse à quarante minutes : les imprécisions
de la source ne sont pas réécrites.

Les colonnes des trois menus restent à un pixel des positions anglaises.
B210-S060 garde la commande 04 ; sa valeur héritée de l'état de test
ne valide pas le fonctionnement naturel du menu d'articles.

## Vérification et limites

S036/S065/S075/S076/S077 restent intacts : formatage non pris en charge,
notamment les marqueurs horaires x2/x3. Les autres textes différés restent
conservés. Les blocs 235/236 et d'autres lacunes restent à traiter.

Les essais ciblés redirigent une demande vers une chaîne choisie en utilisant
les routines natives. Ils vérifient rendu, pagination et terminateur exact ;
ils ne valident pas achats, spectacles, récompenses, traversées, horaires
ou événements en progression naturelle. Le fond provient du banc de test.
Les captures vides finales héritées des sauts de ligne de la source ne
signifient pas qu'un texte manque.

Snes9x 1.63 est utilisé ; 1.60 et le matériel réel ne sont pas testés.
Les conditions d'échec des analyses ne sont pas injectées. Les preuves
détaillées de naissance restent celles de V35. Les 32 occurrences initiales
sont comparées à V36 et le démarrage est rejoué avec V37.

Pagination : S034/S043/S087 resserrés avant les premiers essais ; S071/S087
ajustés après la relecture précédente pour éviter des mots seuls en dernière
page. Cette reconstruction regroupe les deux corrections. Les preuves
finales utilisent final et une référence V36 fraîche au tag reference37.
Les rapports et captures sont liés à la ROM par leur empreinte SHA-256.

Appliquer Tengai_Makyou_Zero_FR_V37.ips directement à la ROM anglaise
originale, sans cumuler les patches.

Résultats : 4 101 lectures natives, 16 contrôles de police et 14 contrôles
de placement réussis. 80 cas de rendu complets, 134 captures finales relues.
Les 85 captures fixes du début et les trois écrans de navigation sont
identiques à V36. 79 lectures des textes différés (59 messages uniques)
restent identiques à la source. 128 blocs sur place, 34 relocalisés,
77 312 octets libres. Les 3 203 entrées précédentes sont conservées.
