# V41 — Sennin, Basara, karaoké et mine

43 textes supplémentaires du bloc 96. Total : 3 483 entrées intégrées.
Les 3 440 entrées V40 et les 32 occurrences initiales sont conservées :
analyses mémoire/SRAM/RTC, naissance et horloge.

Basara indique son sanctuaire au-delà du ravin au nord du château d’Or.
Sennin enseigne la Lame de Sennin après une épreuve : 1 000 ryo à chacune
des sept femmes ou fillettes en difficulté. Donner à un homme ou quitter
la ville oblige à recommencer après lui avoir reparlé. Le coup frappe tous
les ennemis et consomme de la vitalité. Les répliques sur l’alcool conservent
la limite de vingt ans propre au dialogue du jeu et le refus de servir Higan.

Le karaoké coûte 100 ryo par chanson. Les titres Néons éteints et Justice
pour tous sont provisoires dans les dialogues. B096-S020 conserve son menu
anglais en attendant le traitement des colonnes. S023 à S042 restent tous
intacts : paroles, prélude et pauses synchronisées doivent être traités
ensemble, notamment avec la commande 0A et le glyphe CC. Aucun support
nouveau de cet effet n’est revendiqué.

La mine conserve les nids d’insectes mange-or, les bons d’or, les échanges,
le coffre verrouillé, les bourses à 20 000 ryo et la limite de deux blocs
sans risque contre dix en forçant. Le risque de perdre tout l’or reste indiqué.

Les essais ciblés redirigent une demande vers chaque texte avec les routines
natives. Ils vérifient pages et terminateur exact, pas les achats, dons,
échanges, chants ou réussite de l’épreuve en progression naturelle.
Snes9x 1.63 est utilisé ; 1.60 et le matériel réel ne sont pas testés.
Les preuves approfondies de saisie de naissance restent celles de V35.
Les essais V41 utilisent corrected ; la référence V40 utilise reference41.
Les captures intermédiaires de pause peuvent répéter un texte partiel.

Appliquer le patch IPS directement à la ROM anglaise originale, sans cumul.
Les résultats définitifs sont dans verification/emulation_report_v41.json.

Construction : 4 323 lectures natives réussies. 135 blocs sur place,
34 relocalisés, 77 312 octets libres. 16 contrôles de police et
14 contrôles de placement réussis. Les 3 440 entrées antérieures
sont identiques (texte français, texte mis en page et bytes source).

Après relecture, les fins de pages B096-S008/S018/S048 ont été
regroupées pour éviter les mots isolés et conserver les consignes complètes.
Les séquences de pauses restent identiques à la source.

Résultats finaux : 43 cas ciblés, 78 captures relues. Les 85 captures fixes
du début et les trois écrans de navigation sont identiques à V40.
Les 32 occurrences initiales et les signatures internes sont identiques
octet par octet. 105 lectures des différés conservent leurs bytes source.
