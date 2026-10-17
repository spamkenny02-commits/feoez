# V36 — Manto, trois boutons et chambre du prince

43 entrées traduites dans lot30_fr.json : bloc 167 (32), bloc 244 (1,
partagé avec 245) et bloc 253 (10). Total : 3 203 entrées de dialogue.
Les 3 160 entrées antérieures et les 32 modifications des écrans de démarrage,
de naissance et d'horloge sont conservées.

Manto raconte comment il a dupé les crabes, reconnaît les objets du conte
Le Combat du Singe et du Crabe et devient l'animal de Subaru. Les pauses,
répétitions, effets connus et grossièretés sont maintenus. Le jeu anglais
Hey/Hay devient « Hé / quel foin / du foin pour les chevaux ». Le nom
Horsies 'n Deerses Skill devient « technique des Dadas et des Cerfs ».
Les noms d'objets nouveaux restent provisoires jusqu'au travail sur l'inventaire.

Le menu d'Akamaru garde trois colonnes Gauche/Centre/Droite ; les deuxième
et troisième colonnes sont à un pixel des positions anglaises. L'alias 245
est testé séparément. Le bloc 253 conserve les deux récits des princes,
Ninigi, la Flamme éternelle, les portes des Enfers et les huit variantes
d'œufs. Les doublons restent des entrées distinctes.

## Vérification et limites

Les essais ciblés redirigent une demande de dialogue vers une chaîne donnée
avec les routines natives du jeu. Ils vérifient le rendu, les pages et le
terminateur exact ; ils ne valident pas les événements, les conséquences
des trois boutons ou l'éclosion en progression naturelle. Le fond provient
du banc de test. Noyau Snes9x 1.63, pas de test Snes9x 1.60 ou matériel réel.

Les résultats sont liés à la ROM par leur empreinte dans build_report.json,
emulation_report_v36.json et scenes_v36/render_report.json. Les preuves
approfondies de saisie de naissance restent celles de V35 ; V36 conserve
leurs zones auditées et rejoue le parcours de démarrage et les contrôles A/B.
Les conditions d'échec des analyses ne sont pas injectées.

Le journal 210, les blocs 235/236 et les autres lacunes répertoriées restent
à traiter. Les 50 messages différés et quatre invites de débogage des blocs
antérieurs restent inchangés. Aucun pourcentage de traduction complète
n'est déduit du seul nombre d'entrées intégrées.

Appliquer Tengai_Makyou_Zero_FR_V36.ips à la ROM anglaise originale,
sans cumuler les patches.

Pagination B167-S029 : un saut de paragraphe retiré pour éviter une
troisième page presque vide. Les essais finaux utilisent corrected ;
la comparaison V35 utilise final.

Résultats finaux : 4 012 lectures natives, 16 contrôles de police et
14 contrôles de placement réussis. 44 cas ciblés complets, 58 captures
finales relues. Les 85 captures fixes communes du début sont identiques
à V35, comme les trois écrans de navigation. Les 74 lectures des messages
différés (54 messages uniques, dont quatre de débogage) restent identiques
à la source anglaise. 127 blocs sur place, 34 relocalisés, 77 312 octets libres.
