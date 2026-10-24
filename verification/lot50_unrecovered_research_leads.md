# Pistes conservées après perte du poste de travail

Ce document conserve des indications du résumé de conversation, sans remplacer les sources, captures ou rapports perdus. Aucune preuve nouvelle de ROM n’est fournie. Le compteur demeure 50, sans livraison du lot.

La recherche perdue portait sur six variantes anciennes de la roue de combat : Attack/Defend/Scrolls/Skills/Items/Flee vers Attaq./Garder/Parch./Arts/Obj./Fuir. Toutes sont exclues des nouveaux textes. Ne pas modifier la forme de sort B007-S030 « Adieu » pour cette variante de commande Fuir.

Piste de format à revérifier : graphismes OBJ 4bpp, compression SPC7110 mode2, répertoire ROM429000, entrées hex42..4D, douze capacités de128octets entre505D00 et506300. Descripteur DF2404/ROM2F2404, préparation C01605/C02D00, DMA C00320. Le projet d’encodeur et ses vérifications n’ont pas été transférés avant la perte ; il faut les réimplémenter et les retester contre le décodeur natif, sans réutiliser leurs anciennes conclusions.

Piste de classification à revérifier : FD8A, vecteur C30DB9 vers C09C01, charge le catalogue21+argument. C09D10..C09D3F calcule le masque d’un drapeau ; C09C3B modifie7E2000+index. Les608 libellés anglais paraissent être ceux de l’éditeur de drapeaux. La preuve native détaillée a été perdue. Ni cette piste ni l’absence de racines d’événements ne prouvent l’absence d’autres usages calculés. Ne pas traduire du debug pour remplir le lot.

Restes à examiner : menus de parchemins/fusion/séparation, Singles Tea House, message Delete the broken file?, branches de calendrier, synchronisation des chansons et vrais consommateurs des textes de repli. Les trois phases restent ouvertes.
