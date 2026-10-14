# Compte rendu V18

86 nouvelles entrées modifiées, soit 1 269 intégrées au total.
Les 1 183 anciennes entrées sont identiques à la V17 en français,
mise en page et octets source. Les variantes et répétitions comptent séparément.

Lot 13 : sanctuaire de la Grue avant et après sa libération, habitants,
Mai et Chitose, remise de la robe de la Grue, fêtes du calendrier et
indications vers le village du Saké. Cinq blocs 130, 131, 133, 134, 135 :
21, 13, 31, 11 et 10 nouvelles entrées. Les titres du Courrier de la Grue
gardent trois lignes distinctes, sans repli automatique : 121/114/115 pixels.
Les divergences entre les dates et noms des fêtes sont conservées comme
elles apparaissent dans les répliques anglaises.

1 725 lectures dans les routines originales 65816, 16 contrôles de police
et 14 contrôles du placement réussis. Les chaînes inchangées et les alias
sont également contrôlés. Balises, limite de 216 pixels, encodage,
pointeurs, checksum, aller-retour IPS et conservation de la ROM source vérifiés.
48 blocs sur place, 19 relocalisés ; fin du pool à 0x6B8A60,
95 648 octets libres. Les cinq nouveaux blocs tiennent sur place.

B130-S019 reste en anglais, ainsi que le bloc 132 non traité dans ce lot.
Les onze messages différés du bloc 97 et B125-S003 restent aussi inchangés.
Un contrôle séparé relit les treize messages différés avec les routines natives
et compare le bloc 132 entier à l'original : tous leurs octets sont préservés.

Snes9x 1.63 : état neuf, autotests A/B ALL OK et resets, introduction,
dialogues du début et terrain. Les 85 captures communes avec V17 sont identiques.
Navigation à appuis de 12 images : menu principal, réglages et carte identiques.
Le rapport lie les hashes de la ROM et du patch à ce parcours.
Capture de contrôle incluse.

Les 86 nouveaux textes et le menu du journal restent à observer dans leurs scènes.
Premier jet depuis l'anglais, sans comparaison au script japonais.
Aucun essai du jeu complet ni de Snes9x 1.60.

Appliquer Tengai_Makyou_Zero_FR_V18.ips directement à la ROM anglaise
originale, sans cumuler les versions. Sauvegarde sur main ; aucune ROM
ni sauvegarde d'état publiée.
