# Police française — V07 (police conservée de V06)

La police proportionnelle du moteur anglais se trouve à l'offset fichier
`0x2F5200`, avec ses avances à `0x2F7200`. Les routines de rendu de la ROM
lisent respectivement `DF:5200 + caractère × 32` et `DF:7200 + caractère`.
La fenêtre D du SPC7110 pointe normalement sur cette partie de la ROM.

Chaque caractère occupe 32 octets : 16 lignes, deux octets monochromes
adjacents par ligne, soit une cellule maximale de 16 × 16 pixels. Ce n'est
pas une tuile SNES 2bpp : le second octet contient les pixels de droite.
Cela compte notamment pour les ligatures larges telles que Œ.

## Caractères natifs réutilisés

La ROM fournie contient déjà :

```
à â ä é è ê ë î ï ô ö ù û ü ç
À Â Ä É È Ê Ë Î Ï Ô Ö Ù Û Ü Ç
œ Œ æ Æ
```

Ces glyphes et leurs avances sont conservés exactement. Leur prise en charge
manquait dans l'encodeur initial : la V05 avait volontairement retiré les
accents de son aperçu. La V06 étend l'encodage et supprime cette conversion.
`table_fr.json` et `fr.tbl` donnent la correspondance entre Unicode et octets.

## Deux glyphes ajoutés

| Lettre | Code | Base native | Avance |
|---|---|---|---|
| Ÿ | 75 | Y, code 48 | 6 pixels |
| ÿ | 85 | y, code 68 | 5 pixels |

Les lettres Y et y sont copiées pixel pour pixel. Seuls deux points sont
ajoutés au-dessus, à des hauteurs utilisées par les trémas natifs. La ligne
de base, la descente du y, l'épaisseur et l'avance restent celles de la police.
L'atlas `alphabet_fr.png` est rendu depuis les octets de la ROM modifiée,
sans interpolation ; le cadre vert indique les deux nouvelles lettres.

Ces codes remplacent **Ā et ā**, les variantes de A avec macron. Nous n'avons
pas ajouté de nouveau mécanisme de commande ni agrandi la table. Dans le
pool de texte principal de la ROM anglaise, les six occurrences brutes de
75 et 85 appartiennent toutes aux tables de pointeurs : aucune chaîne
anglaise de ce pool ne les emploie comme caractères. Le générateur vérifie
ce point avant de construire le patch.

La réaffectation de ces deux caractères est volontaire pour l'alphabet
français. Une ancienne donnée personnalisée contenant Ā ou ā dans un nom
utilisant cette police les afficherait désormais comme Ÿ ou ÿ. Les autres
caractères natifs, y compris les accents étrangers non concernés, restent
inchangés. Les commandes du moteur et les codes de dictionnaire E0 et suivants
ne sont pas réaffectés.

## Mise en page et vérifications

Les lignes de la scène française sont mesurées avec les avances réelles de
la ROM, avec une limite prudente de 216 pixels. Les pauses et balises 0C/0D
n'occupent pas de pixels. Les espaces françaises avant la ponctuation restent
présentes et sont liées au mot précédent lors de la coupure des lignes.

La scène de test de la V06 affichait les 32 lettres françaises accentuées
et les quatre ligatures. La V07 conserve exactement cette police. Les tests
de la V07 portent sur l’intégration de nouvelles chaînes et la progression.

Le rendu des dialogues est le périmètre vérifié. Les textes anglais dessinés
dans des images et les autres jeux de tuiles ne deviennent pas français en
appliquant ce patch de police. Le générateur ne prétend pas gérer les codes
de contrôle inconnus des autres dialogues.
